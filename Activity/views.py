# coding=utf-8
import simplejson

from django.shortcuts import render, get_object_or_404
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse, Http404
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from .models import Activity, ApplicationThrough, ActivityType, ActivityLikeThrough
from Questionnaire.models import SingleChoiceAnswer, MultiChoiceAnswer, TextAnswer, FileAnswer
from Questionnaire.models import AnswerSheet, Questionnaire, ChoiceQuestion, NonChoiceQuestion
from Questionnaire.utils import create_questionnaire_with_json
from Promotion.models import Share
from .forms import ActivityCreationForm
from .utils import get_activity_session_representation
# Create your views here.


@require_GET
@login_required()
def check_applicant_list(request, action_id):
    activity = get_object_or_404(Activity, id=action_id)
    user = request.user
    if activity.host != user:
        """如果当前用户并不是这个活动的发布者，那么跳转到活动的详情页"""
        return HttpResponseRedirect("/action/%s" % action_id)

    applicant = ApplicationThrough.objects.filter(activity=activity,
                                                  activity__is_active=True,
                                                  user__profile__is_active=True)

    def findall(a):
        answer_set = []
        answer_sheet = AnswerSheet.objects.filter(user=a.user,
                                                  questionnaire__activity=activity)
        answer_set += SingleChoiceAnswer.objects.filter(answer_sheet__in=answer_sheet)
        answer_set += MultiChoiceAnswer.objects.filter(answer_sheet__in=answer_sheet)
        answer_set += TextAnswer.objects.filter(answer_sheet__in=answer_sheet)
        answer_set += FileAnswer.objects.filter(answer_sheet__in=answer_sheet)
        data = {"apply": a,
                "user": a.user,
                "answers": answer_set}
        return data

    datas = map(findall, applicant)
    print datas

    return render(request, "Activity/apply-list.html", {
        "user": user,
        "data_set": datas,
        "act": activity,
    })


@require_GET
def check_activity_detail(request, action_id):
    activity = get_object_or_404(Activity, id=action_id)
    # 增加浏览记录
    activity.viewed_times += 1
    activity.save()
    if Questionnaire.objects.filter(activity=activity, is_active=True).exists():
        questionnaire = Questionnaire.objects.filter(activity=activity, is_active=True)
        single_choice_questions = ChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                                multi_choice=False)
        multi_choice_questions = ChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                               multi_choice=True)
        text_questions = NonChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                          type=0)
        file_questions = NonChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                          type=1)
        return render(request, "Activity/detail.html", {
            "act": activity,
            "single_choice_questions": single_choice_questions,
            "multi_choice_questions": multi_choice_questions,
            "text_questions": text_questions,
            "file_questions": file_questions
        })
    else:
        return render(request, "Activity/detail.html", {
            "act": activity
        })


@require_POST
@login_required()
def apply_an_activity(request, action_id):
    activity = get_object_or_404(Activity, id=action_id)
    if activity.host == request.user:
        # 如果是当前登陆用户自己创建的活动，则跳转到申请列表页
        return HttpResponseRedirect("/action/%s/applicant" % action_id)

    application = ApplicationThrough.objects.get_or_create(activity=activity,
                                                     user=request.user,
                                                     is_active=True)
    if application[1]:
        return HttpResponse({"success": True, "data": {"url": "/action/%s/detail" % action_id}},
                            content_type="application/json")
    else:
        return HttpResponse({"success": False, "data": {"id": "已经申请过该活动"}},
                            content_type="application/json")


@login_required()
def create_new_activity_1(request):
    form = ActivityCreationForm(request.user)
    if request.method == "POST":
        form = ActivityCreationForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            act = form.save()
            request.session["activity_creation_info"] = \
                get_activity_session_representation(act)
            request.session.set_expiry(1800)  # 这个session只有在三十分钟内有效
            return HttpResponseRedirect("/action/%s/edit/2" % act.id)
        else:
            print form.errors

    args = {}
    args.update(csrf(request))
    args["form"] = form
    activity_type = ActivityType.objects.all()
    args["types"] = activity_type
    return render(request, "Activity/create-action-1.html", args)


@login_required()
def create_new_activity_2(request, action_id):
    """创建活动的第二步，首先检查session中的信息"""
    # 从第一步骤出来的
    activity = get_object_or_404(Activity, id=action_id, is_active=False)
    # activity = get_object_or_404(Activity, id=action_id)
    user = request.user

    if user != activity.host:
        # 如果发现试图访问这个链接的当前用户并不是当前用户的创建者，则引导其进入创建的第一步
        return HttpResponseRedirect("/action/new/edit/1")
    act_info = request.session.get("activity_creation_info", "")
    if get_activity_session_representation(activity) != act_info:
        # 检查这个链接是否是由第一步转移过来的，注意这个链接只在30分钟内有效，否则视为放弃了上面的活动
        return HttpResponseRedirect("/action/new/edit/1")
    error_info = None
    if request.method == "POST":
        data = simplejson.loads(request.body)
        # 从POST上来的json数据中构造问卷
        try:
            create_questionnaire_with_json(data, activity)
            return HttpResponseRedirect("/action/%s/publish" % activity.id)
        except ValidationError, error:
            error_info = error.message
            print error_info

    args = {}
    args.update(csrf(request))
    args["user"] = user
    args["activity"] = activity
    args["error_info"] = error_info
    return render(request, "Activity/create-action-2.html", args)


def create_new_activity_3(request, action_id):
    activity = get_object_or_404(Activity, id=action_id)
    user = request.user
    if user != activity.host:
        return HttpResponseRedirect("/action/new/edit/1")
    act_info = request.session.get("activity_creation_info", "")
    if get_activity_session_representation(activity) != act_info:
        return HttpResponseRedirect("action/new/edit/1")

    if request.method == "POST":
        activity.is_active = True
        activity.save()
        return HttpResponseRedirect("/action/%s/detail" % activity.id)

    if Questionnaire.objects.filter(activity=activity, is_active=True).exists():
        questionnaire = Questionnaire.objects.filter(activity=activity, is_active=True)
        single_choice_questions = ChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                                multi_choice=False)
        multi_choice_questions = ChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                               multi_choice=True)
        text_questions = NonChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                          type=0)
        file_questions = NonChoiceQuestion.objects.filter(questionnaire=questionnaire,
                                                          type=1)
        return render(request, "Activity/create-action-3.html", {
            "act": activity,
            "single_choice_questions": single_choice_questions,
            "multi_choice_questions": multi_choice_questions,
            "text_questions": text_questions,
            "file_questions": file_questions
        })
    else:
        return render(request, "Activity/create-action-3.html", {
            "act": activity
        })


@require_POST
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
    return HttpResponse(simplejson.dumps({"success": True, "data": {"url": "/mine/start"}}),
                        content_type="application/json")

@login_required()
def copy_an_activity(request, action_id):
    """
    Note:
    这里要考虑进行这个操作的权限检查的问题
    """
    try:
        act = Activity.objects.get(id=action_id)
    except ObjectDoesNotExist:
        return HttpResponse(simplejson.dumps({"success": False, "data": {"id": "指定的活动不存在"}}),
                            content_type="application/json")
    act.pk = None
    act.host = request.user
    act.save()
    return HttpResponse(simplejson.dumps({"success": True, "data": {"url": "action/%s/detail" % act.id}}),
                        content_type="application/json")



@require_GET
@login_required()
def get_share_link(request, action_id):
    activity = get_object_or_404(Activity, id=action_id)
    share = Share.objects.get_or_create(user=request.user,
                                        activity=activity)
    share_link = share.get_share_link
    HttpResponse("")


@login_required()
def visit_from_share(request, action_id):
    share_code = request.GET.get("code", "")
    share = get_object_or_404(Share, share_code=share_code)
    activity = get_object_or_404(Activity, id=action_id)
    if share.activity != activity:
        raise Http404
    target_user = request.user


@require_GET
@login_required()
def like_an_activity(request):
    action_id = request.GET.get("id", "")
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
        return HttpResponse(simplejson.dumps(error_info), content_type="application/json")

    like = ActivityLikeThrough.objects.get_or_create(user=request.user,
                                                     activity=act)[0]
    like.is_active = not like.is_active
    return HttpResponse(simplejson.dumps({"success": True, "data": {}}), content_type="application/json")
