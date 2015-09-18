# coding=utf-8
import simplejson
import logging

from django.shortcuts import render, get_object_or_404
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from .models import Activity, ApplicationThrough, ActivityType, ActivityLikeThrough
from .forms import ActivityCreationForm
from .utils import get_activity_session_representation
from .tasks import send_del_notification_to_candidate
from Questionnaire.models import SingleChoiceAnswer, MultiChoiceAnswer, TextAnswer, FileAnswer
from Questionnaire.models import AnswerSheet, Questionnaire, ChoiceQuestion, NonChoiceQuestion
from Questionnaire.utils import create_questionnaire_with_json, create_answer_set_with_json
from Promotion.models import Share, ShareRecord
from Notification.signals import send_notification
from findRice.utils import choose_template_by_device
from Profile.utils import profile_active_required

# Create your views here.

# Create a logger
logger = logging.getLogger(__name__)


@require_GET
@login_required()
@profile_active_required
def check_applicant_list(request, action_id):
    activity = get_object_or_404(Activity, id=action_id, is_active=True)
    user = request.user
    if activity.host != user:
        """如果当前用户并不是这个活动的发布者，那么跳转到活动的详情页"""
        return HttpResponseRedirect("/action/%s" % action_id)

    applicant = ApplicationThrough.objects.filter(activity=activity,
                                                  activity__is_active=True,
                                                  user__profile__is_active=True,
                                                  is_active=True)

    def findall(a):
        if not AnswerSheet.objects.filter(user=a.user,
                                          questionnaire__activity=a.activity).exists():
            return {"apply": a,
                    "user": a.user,
                    }
        answer_set = []
        answer_sheet = AnswerSheet.objects.filter(user=a.user,
                                                  questionnaire__activity=a.activity)[0]
        answer_set += list(SingleChoiceAnswer.objects.filter(answer_sheet=answer_sheet))
        answer_set += list(MultiChoiceAnswer.objects.filter(answer_sheet=answer_sheet))
        answer_set += list(TextAnswer.objects.filter(answer_sheet=answer_sheet))
        answer_set += list(FileAnswer.objects.filter(answer_sheet=answer_sheet))
        data = {"apply": a,
                "user": a.user,
                "answers": answer_set}
        return data

    datas = map(findall, list(applicant))

    args = {
        "user": user,
        "data_set": datas,
        "act": activity,
    }
    args.update(csrf(request))
    return render(request, choose_template_by_device(request,
                                                     "Activity/apply-list.html",
                                                     "Activity/mobile/apply-list.html"), args)


@require_GET
def check_activity_detail(request, action_id):
    activity = get_object_or_404(Activity, id=action_id, is_active=True)
    user = request.user
    if not user.is_authenticated():
        user = None
    like = False
    share = None

    if 'code' in request.GET and user is not None:
        # Check if this code is related to the user
        share_code = request.GET.get('code')
        if Share.objects.filter(share_code=share_code, user=user).exists():
            # 如果分享CODE是由当前用户产生的，尝试获取pre_code，如果pre_code不存在的话，仍然保留原值
            share_code = request.GET.get('pre_code', share_code)
        else:
            # 如果当期CODE来自其他人，redirect以更新code，但是将现在的code以pre_code参数保留
            share = Share.objects.get_or_create(activity=activity, user=user)[0]
            return HttpResponseRedirect('/action/{0}?code={1}&pre_code={2}'.format(
                action_id, share.share_code, share_code))
    else:
        share_code = request.GET.get('code', None)

    if activity.host != request.user:
        # 增加浏览记录
        activity.viewed_times += 1
        activity.save()
        # Check if this activity is liked by the user
        if request.user.is_authenticated():
            user = request.user
            like = ActivityLikeThrough.objects.filter(activity=activity, user=user).exists()
    if share_code:
        logger.debug(u'The share code is: %s' % share_code)
    else:
        logger.debug(u'Code not found')

    if share_code and user\
            and not ApplicationThrough.objects.filter(activity=activity, user=request.user).exists():
        share = get_object_or_404(Share, share_code=share_code, activity=activity)
        obj, created = ShareRecord.objects.get_or_create(share=share, target_user=request.user)
        if created:
            logger.debug(u'分享记录创建，点进来的用户是|%s(username: %s)|，对应的活动是|%s(id: %s)|' % (
                request.user.profile.name, request.user.username, activity.name, activity.id))
    elif request.user.is_authenticated():
        share = Share.objects.get_or_create(activity=activity, user=request.user)
    else:
        share = Share.objects.get_or_create(activity=activity, user=None)
    if Questionnaire.objects.filter(activity=activity, is_active=True).exists():
        questionnaire = Questionnaire.objects.filter(activity=activity, is_active=True)[0]
        single_choice_questions = ChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                                multi_choice=False)
        multi_choice_questions = ChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                               multi_choice=True)
        text_questions = NonChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                          type=0)
        file_questions = NonChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                          type=1)
        q_if = True
        if len(single_choice_questions) + len(multi_choice_questions) + len(text_questions) + len(file_questions) == 0:
            q_if = False
        args = {
            "act": activity,
            "single_choice_questions": single_choice_questions,
            "multi_choice_questions": multi_choice_questions,
            "text_questions": text_questions,
            "file_questions": file_questions,
            "user": user,
            "like": like,
            "share": share,
            "questionnaire": q_if,
            "share_code": share_code
        }
        args.update(csrf(request))
        return render(request,
                      choose_template_by_device(request,
                                                "Activity/detail.html",
                                                "Activity/mobile/detail.html"),
                      args)
    else:
        args = {
            "act": activity,
            "user": user,
            "like": like,
            "share": share,
            "share_code": share_code
        }
        args.update(csrf(request))
        return render(request,
                      choose_template_by_device(request,
                                                "Activity/detail.html",
                                                "Activity/mobile/detail.html"),
                      args)


@require_POST
def apply_an_activity(request, action_id):
    if not request.user.is_authenticated():
        next_url = '/login?next=/action/%s' % action_id
        if 'share_code' in request.POST:
            next_url += "?code=%s" % request.POST.get("share_code")
        return JsonResponse({'success': True, 'data': {'url': next_url}}
                            , content_type='text/html')
    activity = get_object_or_404(Activity, id=action_id)
    logger.debug(u"试图报名活动，对应活动为|{0:s}|(id:{1:d}), 当前用户为|{2:s}|({3:s})"
                 .format(activity.name, activity.id, request.user.profile.name, request.user.username))
    # 2015/8/8 取消用户不得报名自己创建的活动的限制
    # if activity.host == request.user:
    #     # 如果是当前登陆用户自己创建的活动，则跳转到申请列表页
    #     # Log first
    #     logger.debug(u"报名出错，试图报名自己的活动，对应活动为|%s|(id:%s), 当前用户为|%s|(%s)"
    #                  % (activity.name, activity.id, request.user.profile.name, request.user.username))
    #     return JsonResponse({"success": False, "data": {"error": "不能报名自己的活动"}})

    # Check if there exist a valid questionnaire for this activity
    if Questionnaire.objects.filter(activity=activity, is_active=True).exists():
        # Then load the answer data and create the answer sheet
        q = Questionnaire.objects.filter(activity=activity)[0]
        json = simplejson.loads(request.POST.get("answer", ""))
        try:
            create_answer_set_with_json({"answer": json}, request, q, request.user)
        except ValidationError:
            logger.debug(u"创建答案失败，发生了Validation错误，提交的json格式为：{0:s}".format(json))
            raise ValidationError(u"创建答案失败")

    # Try to apply this activity, validations are done in this function
    application = ApplicationThrough.objects.try_to_apply(activity=activity,
                                                          user=request.user, )

    # Create the response according
    if application[1]:
        # Associate this application with the share_record
        if 'share_code' in request.POST:
            share_code = request.POST.get('share_code', '')
            try:
                share = Share.objects.get(share_code=share_code, activity=activity)
                share_record = ShareRecord.objects.get(share=share, target_user=request.user)
                share_record.application = application[0]
                share_record.save()
                logger.debug(u"申请与分享记录成功绑定, 本次报名为用户|username: %s|报名活动|id: %s|,code为%s" %
                             (request.user.username, activity.id, share_code))
            except ObjectDoesNotExist:
                # Just drop the share code if it is invalid
                logger.debug(u"申请与分享记录绑定失败, 本次报名为用户|username: %s|报名活动|id: %s|,code:%s" %
                             (request.user.username, activity.id, share_code))
        send_notification.send(sender=get_user_model(),
                               notification_type="activity_notification",
                               notification_center=activity.host.notification_center,
                               activity=activity,
                               user=request.user,
                               activity_notification_type="activity_applied")
        return JsonResponse({
            "success": True,
            "data": {
                "url": "/mine/apply"
            }
        }, content_type='text/html')
    else:
        return JsonResponse({"success": False, "data": {"id": application[2]}}, content_type='text/html')


@login_required()
@profile_active_required
def unapply_an_activity(request, action_id):
    activity = get_object_or_404(Activity, id=action_id)
    applicant = get_object_or_404(ApplicationThrough, activity=activity,
                                  user=request.user,
                                  is_active=True,
                                  status__in=["applying", "approved"])
    applicant.is_active = False
    applicant.status = "applying"
    applicant.save()
    send_notification.send(sender=get_user_model(),
                           notification_type="activity_notification",
                           notification_center=activity.host.notification_center,
                           activity=activity,
                           user=request.user,
                           activity_notification_type="cancel_apply")
    return JsonResponse({
        "success": True,
        "data": {
            "url": "/mine/apply"
        }
    }, content_type='text/html')


@require_POST
@login_required()
@profile_active_required
def stop_accepting_apply(request, action_id):
    activity = get_object_or_404(Activity, id=action_id)
    if not activity.host == request.user:
        return JsonResponse({"success": False, "data": {}}, content_type='text/html')
    activity.accept_apply = False
    activity.save()
    return JsonResponse({"success": True, "data": {}}, content_type='text/html')


@require_POST
@login_required()
@profile_active_required
def restart_accepting_apply(request, action_id):
    activity = get_object_or_404(Activity, id=action_id)
    if not activity.host == request.user:
        return JsonResponse({"success": False, "data": {}}, content_type='text/html')
    activity.accept_apply = True
    activity.save()
    return JsonResponse({"success": True, "data": {}}, content_type='text/html')


@login_required()
@profile_active_required
def create_new_activity_1(request):
    form = ActivityCreationForm(request.user, initial={"host_name": request.user.profile.name})
    if request.method == "POST":
        form = ActivityCreationForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            act = form.save()
            # request.COOKIES["activity_creation_info"] = \
            # get_activity_session_representation(act)
            # request.COOKIES.set_expiry(1800)  # 这个session只有在三十分钟内有效
            response = JsonResponse({
                "success": True,
                "data": {
                    "url": "/action/%s/create/2" % act.id
                }
            }, content_type='text/html')
            response.set_cookie("activity_creation_info", get_activity_session_representation(act),
                                max_age=1800)
            return response
        else:
            logger.debug(u"创建活动失败，失败信息为: %s" % form.errors.as_data)
            data = {}
            errors = form.errors
            if 'start_time' in errors:
                data['start_time'] = u'开始时间不能早于当前时间'
            if 'end_time' in errors:
                data['end_time'] = u'结束时间不能早于开始时间'
            if data == {}:
                data['unknown'] = u'未知错误'
            return JsonResponse({
                "success": False,
                "data": data
            }, content_type='text/html')

    args = {}
    args.update(csrf(request))
    args["form"] = form
    activity_type = ActivityType.objects.all()
    args["types"] = activity_type
    return render(request,
                  choose_template_by_device(request,
                                            "Activity/create-action-1.html",
                                            "Activity/mobile/create-action-1.html"),
                  args)


@require_GET
@login_required()
@profile_active_required
def edit_new_activity_1(request, action_id):
    """创建活动的第二步，首先检查session中的信息"""
    # 从第一步骤出来的
    activity = get_object_or_404(Activity, id=action_id, is_active=False)
    # activity = get_object_or_404(Activity, id=action_id)
    user = request.user
    if user != activity.host:
        # 如果发现试图访问这个链接的当前用户并不是当前用户的创建者，则引导其进入创建的第一步
        return HttpResponseRedirect("/action/new/create/1")
    act_info = request.session.get("activity_creation_info", "")
    if get_activity_session_representation(activity) != act_info:
        # 检查这个链接是否是由第一步转移过来的，注意这个链接只在30分钟内有效，否则视为放弃了上面的活动
        return HttpResponseRedirect("/action/new/create/1")

    if request.method == "POST":
        form = ActivityCreationForm(request.user, request.POST, request.FILES, instance=activity)
        if form.is_valid():
            act = form.save()
            # request.COOKIES["activity_creation_info"] = \
            # get_activity_session_representation(act)
            # request.COOKIES.set_expiry(1800)  # 这个session只有在三十分钟内有效
            response = JsonResponse({
                "success": True,
                "data": {
                    "url": "/action/%s/create/2" % act.id
                }
            }, content_type='text/html')
            return response
        else:
            data = {}
            logger.debug(u"编辑活动第一步失败，错误信息为%s" % form.errors.as_data)
            errors = form.errors
            if 'start_time' in errors:
                data['start_time'] = u'开始时间不能早于当前时间'
            if 'end_time' in errors:
                data['end_time'] = u'结束时间不能早于开始时间'
            if data == {}:
                data['unknown'] = u'未知错误'
            return JsonResponse({
                "success": False,
                "data": data
            }, content_type='text/html')

    form = ActivityCreationForm(instance=activity, initial={"activity_type": activity.activity_type.display_order,
                                                            "hour": activity.hour,
                                                            "day": activity.day,
                                                            "minute": activity.minute,
                                                            "reward": activity.reward})
    args = {}
    args.update(csrf(request))
    args["form"] = form
    activity_type = ActivityType.objects.all()
    args["types"] = activity_type
    if activity.is_active:
        args["action_id"] = activity.id
    response = render(request,
                      choose_template_by_device(request,
                                                "Activity/create-action-1.html",
                                                "Activity/mobile/create-action-1.html"),
                      args)
    return response


@login_required()
@profile_active_required
def create_new_activity_2(request, action_id):
    """创建活动的第二步，首先检查session中的信息"""
    # 从第一步骤出来的
    activity = get_object_or_404(Activity, id=action_id, is_active=False)
    # activity = get_object_or_404(Activity, id=action_id)
    user = request.user

    if user != activity.host or "activity_creation_info" not in request.COOKIES:
        # 如果发现试图访问这个链接的当前用户并不是当前用户的创建者，则引导其进入创建的第一步
        return HttpResponseRedirect("/action/new/create/1")

    act_info = request.COOKIES["activity_creation_info"]
    if get_activity_session_representation(activity) != act_info:
        # 检查这个链接是否是由第一步转移过来的，注意这个链接只在30分钟内有效，否则视为放弃了上面的活动
        return HttpResponseRedirect("/action/new/create/1")
    error_info = None
    if request.method == "POST":
        data = simplejson.loads(request.POST["criteria"])
        # 从POST上来的json数据中构造问卷
        try:
            create_questionnaire_with_json({"criteria": data}, activity)
            return JsonResponse({
                "success": True,
                "data": {
                    "url": "/action/%s/publish" % activity.id
                }
            }, content_type='text/html')
        except ValidationError, error:
            error_info = error.message
            logger.debug(u"创建活动第二步失败,该活动由|%s(id: %s)|创建，错误信息为: %s" % (
                user.profile.name, user.id, error_info))
            return JsonResponse({
                "success": False,
                "data": {
                    "unknown": "未知错误"
                }
            }, content_type='text/html')

    args = {}
    args.update(csrf(request))
    args["user"] = user
    args["activity"] = activity
    args["error_info"] = error_info
    return render(request,
                  choose_template_by_device(request,
                                            "Activity/create-action-2.html",
                                            "Activity/mobile/create-action-2.html"),
                  args)


@login_required()
@profile_active_required
def publish_an_activity(request, action_id):
    activity = get_object_or_404(Activity, id=action_id)
    user = request.user
    if user != activity.host:
        return HttpResponseRedirect("/action/new/create/1")
    # act_info = request.session.get("activity_creation_info", "")
    # if get_activity_session_representation(activity) != act_info:
    # return HttpResponseRedirect("/action/new/create/1")

    if request.method == "POST":
        activity.is_active = True
        activity.is_published = True
        activity.save()
        share = Share.objects.get_or_create(user=request.user, activity=activity)[0]
        return JsonResponse({
            "success": True,
            "data": {
                "url": share.get_share_link()
            }
        }, content_type='text/html')

    if Questionnaire.objects.filter(activity=activity, is_active=True).exists():
        questionnaire = Questionnaire.objects.filter(activity=activity, is_active=True)[0]
        single_choice_questions = ChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                                multi_choice=False)
        multi_choice_questions = ChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                               multi_choice=True)
        text_questions = NonChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                          type=0)
        file_questions = NonChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                          type=1)
        args = {
            "act_id": activity.id,
            "act": activity,
            "single_choice_questions": single_choice_questions,
            "multi_choice_questions": multi_choice_questions,
            "text_questions": text_questions,
            "file_questions": file_questions,
            "show_publish": True
        }
        args.update(csrf(request))
        return render(request,
                      choose_template_by_device(request,
                                                "Activity/create-action-3.html",
                                                "Activity/mobile/create-action-3.html"),
                      args)
    else:
        args = {
            "act_id": activity.id,
            "act": activity,
            "show_publish": True
        }
        args.update(csrf(request))
        return render(request,
                      choose_template_by_device(request,
                                                "Activity/create-action-3.html",
                                                "Activity/mobile/create-action-3.html"),
                      args)


@login_required()
@profile_active_required
def edit_activity_1(request, action_id):
    activity = get_object_or_404(Activity, id=action_id, is_active=True)
    if not activity.host == request.user:
        return HttpResponseForbidden()

    form = ActivityCreationForm(request.user, instance=activity,
                                initial={"activity_type": activity.activity_type.display_order,
                                         "hour": activity.hour,
                                         "day": activity.day,
                                         "minute": activity.minute,
                                         "reward": activity.reward})
    if request.method == "POST":
        form = ActivityCreationForm(request.user, request.POST, request.FILES,
                                    instance=activity.get_backup())
        if form.is_valid():
            form.save()
            response = JsonResponse({
                "success": True,
                "data": {
                    "url": "/action/%s/edit/2" % activity.id
                }
            }, content_type='text/html')
            return response
        else:
            data = {}
            errors = form.errors
            if 'start_time' in errors:
                data['start_time'] = u'开始时间不能早于当前时间'
            if 'end_time' in errors:
                data['end_time'] = u'结束时间不能早于开始时间'
            if data == {}:
                data['unknown'] = u'未知错误'
            return JsonResponse({
                "success": False,
                "data": data
            }, content_type='text/html')

    args = {}
    args.update(csrf(request))
    args["form"] = form
    activity_type = ActivityType.objects.all()
    args["types"] = activity_type
    args["action_id"] = action_id
    args["editing"] = True
    args["act_type"] = activity.activity_type
    # 下面的两个参数主要用来给移动端填充数据
    args["act"] = activity
    return render(request,
                  choose_template_by_device(request,
                                            "Activity/create-action-1.html",
                                            "Activity/mobile/create-action-1.html"),
                  args)


@login_required()
@profile_active_required
def edit_activity_2(request, action_id):
    activity = get_object_or_404(Activity, id=action_id, is_active=True)
    if not activity.host == request.user:
        return HttpResponseForbidden()

    if request.method == "POST":
        data = simplejson.loads(request.POST["criteria"])
        # 从POST上来的json数据中构造问卷
	logger.debug(u"编辑活动第二步，提交到新到问卷结构是{0}".format(request.POST["criteria"]))
        try:
            questionnaire = create_questionnaire_with_json({"criteria": data}, activity, is_active=False)
            request.session["questionnaire_id_tmp"] = questionnaire.id
            return JsonResponse({
                "success": True,
                "data": {
                    "url": "/action/%s/save" % activity.id
                }
            }, content_type='text/html')
        except ValidationError, error:
            error_info = error.message
            return JsonResponse({
                "success": True,
                "data": {
                    "unknown": "未知错误"
                }
            }, content_type='text/html')

    args = {}
    args.update(csrf(request))
    args["user"] = request.user
    args["activity"] = activity
    args["edit"] = True

    if Questionnaire.objects.filter(activity=activity, is_active=True).exists():
        questionnaire = Questionnaire.objects.filter(activity=activity, is_active=True)[0]
        single_choice_questions = ChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                                multi_choice=False)
        multi_choice_questions = ChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                               multi_choice=True)
        text_questions = NonChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                          type=0)
        file_questions = NonChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                          type=1)
        args["single_choice_questions"] = single_choice_questions
        args["multi_choice_questions"] = multi_choice_questions
        args["text_questions"] = text_questions
        args["file_questions"] = file_questions
        logger.debug(u"找到到问卷为id＝{0}, 其创建时间是{1}".format(questionnaire.id, questionnaire.created_at))
    else:
        logger.debug(u"没有找到该活动对应到问卷，活动id为{0}".format(activity.id))
    return render(request,
                  choose_template_by_device(request,
                                            "Activity/create-action-2.html",
                                            "Activity/mobile/create-action-2.html"),
                  args)


@login_required()
@profile_active_required
def save_an_activity(request, action_id):
    activity = get_object_or_404(Activity, id=action_id)
    if not activity.host == request.user:
        return HttpResponseForbidden()
    q_id = request.session.get("questionnaire_id_tmp", -1)
    q_id = int(q_id)

    if request.method == "POST":
        if activity.backup is None or not activity.is_active:
            activity.is_active = True
            activity.save()
            return JsonResponse({
                "success": True,
                "data": {
                    "url": "/mine/start"
                }
            }, content_type='text/html')

        if Questionnaire.objects.filter(activity=activity, is_active=False, id=q_id).exists():
            questionnaire = Questionnaire.objects.filter(activity=activity, is_active=False, id=q_id)[0]
            questionnaire.is_active = True
            questionnaire.save()
        backup = activity.backup
        tmp = backup.id
        backup.id = activity.id
        activity.id = tmp
        backup.is_active = True
        activity.is_active = False
        backup.save()
        activity.save()

        return JsonResponse({
            "success": True,
            "data": {
                "url": "/mine/start"
            }
        }, content_type='text/html')

    if Questionnaire.objects.filter(activity=activity, is_active=False, id=q_id).exists():
        questionnaire = Questionnaire.objects.filter(activity=activity, is_active=False)[0]
        single_choice_questions = ChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                                multi_choice=False)
        multi_choice_questions = ChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                               multi_choice=True)
        text_questions = NonChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                          type=0)
        file_questions = NonChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                          type=1)
        args = {
            "act_id": activity.id,
            "act": activity.backup,
            "single_choice_questions": single_choice_questions,
            "multi_choice_questions": multi_choice_questions,
            "text_questions": text_questions,
            "file_questions": file_questions,
            "show_publish": False
        }
        args.update(csrf(request))
        return render(request,
                      choose_template_by_device(request,
                                                "Activity/create-action-3.html",
                                                "Activity/mobile/create-action-3.html"),
                      args)
    else:
        args = {
            "act_id": activity.id,
            "act": activity.backup,
            "show_publish": False
        }
        args.update(csrf(request))
        return render(request,
                      choose_template_by_device(request,
                                                "Activity/create-action-3.html",
                                                "Activity/mobile/create-action-3.html"),
                      args)


@require_POST
@login_required()
@profile_active_required
def del_an_activity(request, action_id):
    try:
        act = Activity.objects.get(id=action_id)
    except ObjectDoesNotExist:
        return HttpResponse(simplejson.dumps({"success": False, "data": {"id": "指定的活动不存在"}}),
                            content_type="application/json")
    if not act.host == request.user:
        return HttpResponse(simplejson.dumps({"success": False, "data": {"user": "没有删除权限"}}),
                            content_type="application/json")

    act.is_active = False
    act.save()
    send_del_notification_to_candidate.delay(act)
    return HttpResponse(simplejson.dumps({"success": True, "data": {"url": "/mine/start"}}),
                        content_type="application/json")


@require_POST
@login_required()
@profile_active_required
def copy_an_activity(request, action_id):
    """
    Note:
    这里要考虑进行这个操作的权限检查的问题
    """
    try:
        act = Activity.objects.get(id=action_id, is_active=True)
    except ObjectDoesNotExist:
        return JsonResponse({
            "success": False,
            "data": {
                "id": "没有找到指定的活动"
            }
        }, content_type='text/html')
    q = None
    if Questionnaire.objects.filter(activity=act, is_active=True).exists():
        q = Questionnaire.objects.filter(activity=act, is_active=True)[0]

    act.pk = None
    act.host = request.user
    act.is_published = False
    act.save()
    if q:
        q.activity = act
        q.save()
    return JsonResponse({
        "success": True,
        "data": {
            "url": "/action/%s/edit/1" % act.id
        }
    }, content_type='text/html')


@require_GET
@login_required()
@profile_active_required
def get_share_link(request, action_id):
    activity = get_object_or_404(Activity, id=action_id, is_active=True)
    share = Share.objects.get_or_create(user=request.user,
                                        activity=activity)
    share_link = share.get_share_link()
    HttpResponse("")


@login_required()
@profile_active_required
def visit_from_share(request, action_id):
    """We create a share record here, and redirect the visitor to the detail page"""
    if "code" not in request.GET:
        raise Http404
    share_code = request.GET.get("code", "")
    activity = get_object_or_404(Activity, id=action_id)
    share = get_object_or_404(Share, share_code=share_code, activity=activity)
    ShareRecord.objects.get_or_create(share=share, target_user=request.user)
    return HttpResponseRedirect("/action/%s/detail" % activity.id)


def like_an_activity(request):
    if not request.user.is_authenticated():
        return JsonResponse({'success': True, 'data': {'url': '/login?next=%s' % request.META["HTTP_REFERER"]}},
                            content_type='text/html')
    elif not request.user.profile.is_active:
        return JsonResponse({'success': True, 'data': {'url': '/login?next=%s' % request.META["HTTP_REFERER"]}},
                            content_type='text/html')
    action_id = request.POST.get("id", "")
    try:
        action_id = int(action_id)
        act = Activity.objects.get(id=action_id)
    except (ValueError, ObjectDoesNotExist):
        error_info = {
            "success": False,
            "data": {
                "id": "指定的活动不存在"
            }
        }
        return HttpResponse(simplejson.dumps(error_info))

    like, created = ActivityLikeThrough.objects.get_or_create(user=request.user,
                                                              activity=act)
    if not created:
        like.is_active = not like.is_active
    like.save()

    return HttpResponse(simplejson.dumps({"success": True, "data": {}}))

