# coding=utf-8
from django.shortcuts import render, get_object_or_404
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_http_methods, require_GET
from django.http import HttpResponseForbidden, HttpResponseRedirect

from .models import Activity, ApplicationThrough
from Profile.models import UserProfile
from Questionnaire.models import SingleChoiceAnswer, MultiChoiceAnswer, TextAnswer, FileAnswer
from Questionnaire.models import AnswerSheet
from .forms import ActivityCreationForm
# Create your views here.


@require_GET
@login_required()
def check_applicant_list(request, action_id):
    activity = get_object_or_404(Activity, id=action_id)
    user = request.user
    if activity.host != user:
        """如果当前用户并不是这个活动的发布者，那么禁止查看"""
        return HttpResponseForbidden("403 Forbidden")

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
@login_required()
def check_activity_detail(request, action_id):
    activity = get_object_or_404(Activity, id=action_id)
    return render(request, "Activity/detail.html", {
        "act": activity
    })


@login_required()
def create_new_activity_1(request):
    form = ActivityCreationForm()
    if request.method == "POST":
        form = ActivityCreationForm(request.POST)
        if form.is_valid:
            act = form.save()
            return HttpResponseRedirect("/action/%s/edit/2" % act.id)
        else:
            print form.errors

    args = {}
    args.update(csrf(request))
    args["form"] = form

    return render(request, "Activity/create-action-1.html", args)
