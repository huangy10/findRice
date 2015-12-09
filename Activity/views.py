# coding=utf-8
import simplejson
import json
import logging

from django.shortcuts import render, get_object_or_404
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

from .models import Activity, ApplicationThrough, ActivityType, ActivityLikeThrough
from .forms import ActivityCreationForm
from .utils import get_activity_session_representation
from .tasks import send_del_notification_to_candidate
from Questionnaire.models import SingleChoiceAnswer, MultiChoiceAnswer, TextAnswer, FileAnswer
from Questionnaire.models import AnswerSheet, Questionnaire, ChoiceQuestion, NonChoiceQuestion
from Questionnaire.utils import create_questionnaire_with_json, create_answer_set_with_json
from Promotion.models import ShareRecord
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
                                                  user__is_active=True,
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
    """ 不必要在这个步骤里面追踪Share code，事实上share code已经全面取消。但是在这个页面中需要埋入当前用户的promotion code
    """
    activity = get_object_or_404(Activity, id=action_id, is_active=True)
    user = request.user

    if user.is_authenticated():
        if "code" in request.GET:
            promotion_code = request.GET.get('code')
            if promotion_code == user.profile.promotion_code:
                # 如果当前的code是本用户
                promotion_code = request.GET.get("precode", None)
            else:
                # 如果当前的code不是当前用户的,那么重整url
                return HttpResponseRedirect("/action/{0}?code={1}&precode={2}".format(
                    action_id, user.profile.promotion_code, promotion_code
                ))
        else:
            return HttpResponseRedirect("/action/%s?code=%s" % (action_id, user.profile.promotion_code))
    else:
        promotion_code = request.GET.get("code")

    # 到这里为止,promotion_code, 表征的就是向当前用户推广的推广者, 如果没有推广者,则为None,

    if user.is_authenticated() and activity.host_id != user.id:
        # 更新浏览次数
        activity.viewed_times += 1
        activity.save()
    # 查看当前用户是否点赞过这个用户
    if user.is_authenticated():
        liked = ActivityLikeThrough.objects.filter(user=user, activity=activity).exists()
    else:
        liked = False
        user = None

    # 取出问卷
    questionnaire = Questionnaire.objects.filter(activity=activity, is_active=True).first()

    if questionnaire is not None:
        # questionnaire = Questionnaire.objects.get(activity=activity, is_active=True)
        single_choice_questions = ChoiceQuestion.objects.filter(questionnaire=questionnaire, multi_choice=False)
        multi_choice_questions = ChoiceQuestion.objects.filter(questionnaire=questionnaire, multi_choice=True)
        text_questions = NonChoiceQuestion.objects.filter(questionnaire=questionnaire, type=0)
        file_questions = NonChoiceQuestion.objects.filter(questionnaire=questionnaire, type=1)
        if len(single_choice_questions) + len(multi_choice_questions) + len(text_questions) + len(file_questions) == 0:
            has_questions = False
        else:
            has_questions = True
        args = {
            "act": activity,
            "single_choice_questions": single_choice_questions,
            "multi_choice_questions": multi_choice_questions,
            "text_questions": text_questions,
            "file_questions": file_questions,
            "user": user,
            "like": liked,
            "promotion_code": promotion_code,
            "questionnaire": has_questions,
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
            "promotion_code": promotion_code,
            "like": liked,
        }
        args.update(csrf(request))
        return render(request,
                      choose_template_by_device(request,
                                                "Activity/detail.html",
                                                "Activity/mobile/detail.html"),
                      args)


@require_POST
def apply_an_activity(request, action_id):
    user = request.user
    activity = get_object_or_404(Activity, id=action_id, is_active=True)
    if not user.is_authenticated():
        # 如果用户没有登陆，将其到引导登陆页面
        next_url = '/login?next=/action/%s' % action_id
        # 注意追踪推广参数
        if 'promotion_code' in request.POST:
            next_url += '?code=%s' % request.POST['promotion_code']
        return HttpResponse(json.dumps({'success': True, 'data': {'url': next_url}}))

    # 确认用户已经登陆以后，开始开始申请活动
    if Questionnaire.objects.filter(activity=activity, is_active=True).exists():
        # Then load the answer data and create the answer sheet
        q = Questionnaire.objects.filter(activity=activity, is_active=True).first()
        json_data = simplejson.loads(request.POST.get("answer", "{}"))
        try:
            create_answer_set_with_json({"answer": json_data}, request, q, request.user)
        except ValidationError:
            logger.debug(u"创建答案失败，发生了Validation错误，提交的json格式为：{0:s}".format(json))
            raise ValidationError(u"创建答案失败")

    # 此时，尝试申请活动
    application, success, error_info = ApplicationThrough.objects.try_to_apply(activity=activity, user=user)
    if success:
        # 向活动的创建者发送通知
        send_notification.send(sender=get_user_model(),
                               notification_type="activity_notification",
                               notification_center=activity.host.notification_center,
                               activity=activity,
                               user=request.user,
                               activity_notification_type="activity_applied")
        # 在这里我们需要检查当前用户是否是由其他用户分享过来的
        code = request.POST.get('promotion_code', None)
        if code is not None and code != user.profile.promotion_code:
            try:
                sharer = get_user_model().objects.get(profile__promotion_code=code)
                ShareRecord.objects.create(sharer=sharer, user=user, activity=activity)
            except ObjectDoesNotExist:
                logger.debug(u"发现非法的promotion_code: %s" % code)
        # 在日志内记录本次申请行为
        logger.debug(u"报名活动成功，对应活动为|{0:s}|(id:{1:d}), 当前用户为|{2:s}|({3:s})"
                     .format(activity.name, activity.id, request.user.profile.name, request.user.username))
        return HttpResponse(json.dumps({'success': True, 'data': {'url': '/mine/apply'}}))
    else:
        logger.debug(u"报名活动失败，对应活动为|{0:s}|(id:{1:d}), 当前用户为|{2:s}|({3:s})，原因为:{4:s}"
                     .format(activity.name, activity.id, request.user.profile.name, request.user.username, error_info))
        return HttpResponse(json.dumps({'success': False, 'data': {'id': error_info}}))


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

    q_id = request.session.get("questionnaire_id_tmp", -1)

    if request.method == "POST":
        activity.is_active = True
        activity.is_published = True
        activity.save()

        return JsonResponse({
            "success": True,
            "data": {
                "url": reverse('action:activity_detail', args=(action_id, ))
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


@login_required()
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

