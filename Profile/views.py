# coding=utf-8
import random
import re
import simplejson
import json

from django.utils import timezone
from django.conf import settings
from django.shortcuts import render
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST

from .forms import UserRegisterFormStep1, UserRegisterFormStep2
from .forms import PasswordChangeForm, ProfileChangeForm
from Activity.models import Activity
from .models import RiceTeamContribution, RiceTeam
from .models import VerifyCode
from .utils import send_sms
# Create your views here.


@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        pwd = request.POST.get("pwd", "").strip()
        user = auth.authenticate(username=username, password=pwd)
        if user is not None:
            auth.login(request, user)
            success_info = {
                "success": True,
                "data": {
                    "url": request.GET.get("next", "/")
                }
            }
            return HttpResponse(json.dumps(success_info), content_type="application/json")
            # return HttpResponseRedirect(request.GET.get("next", "/"))
        else:
            error_info = {
                "success": False
            }
            if not auth.get_user_model().objects.filter(username=username).exists():
                error_info["data"] = {
                    "username": "该用户名不存在"
                }
            else:
                error_info["data"] = {
                    "pwd": "密码错误"
                }
            return HttpResponse(json.dumps(error_info), content_type="application/json")

    args = {}
    args.update(csrf(request))

    return render(request, "Profile/login.html", args)


@login_required()
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


@require_http_methods(["GET", "POST"])
def register_step_1(request):
    form = UserRegisterFormStep1()
    if request.method == "POST":
        form = UserRegisterFormStep1(request.POST)
        if form.is_valid():
            form.save()
            username = request.POST["username"]
            pwd = request.POST["password1"]
            new_user = auth.authenticate(username=username,
                                         password=pwd)
            auth.login(request, new_user)
            success_info = {
                "success": True,
                "data": {
                    "url": "/register"
                }
            }
            return HttpResponse(json.dumps(success_info), content_type="application/json")
        else:
            error_info = {
                "success": False
            }
            errors = form.errors
            data = {}
            if "password1" in errors:
                data["pwd"] = errors["password1"][0]
            if "password2" in errors:
                data["pwd-confirm"] = errors["password2"][0]
            if "username" in errors:
                data["username"] = errors["username"][0]
            else:
                data["unknown"] = "未知错误，请联系管理员"
            error_info["data"] = data
            print form.errors
            return HttpResponse(json.dumps(error_info), content_type="application/json")

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render(request, "Profile/register.html", args)


@require_http_methods(["GET", "POST"])
def register_step_2(request):
    user = request.user
    if not user.is_authenticated() or user.profile.is_active:
        return HttpResponseRedirect("/register/basic")

    form = UserRegisterFormStep2()
    if request.method == "POST":
        form = UserRegisterFormStep2(request.POST, request.FILES, instance=user.profile, initial={})
        if form.is_valid():
            form.save()
            success_info = {
                "success": True,
                "data": {
                    "url": "/"
                }
            }
            return HttpResponse(json.dumps(success_info), "application/json")
        else:
            print form.errors
            errors = form.errors
            error_info = {"success": False}
            data = {}
            if "code" in errors:
                data["verifycode"] = errors["code"][0]
            if "phoneNum" in errors:
                data["mobile"] = errors["phoneNum"][0]
            error_info["data"] = data
            return HttpResponse(json.dumps(error_info), content_type="application/json")

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render(request, "Profile/register-addon.html", args)


@require_http_methods(["GET", "POST"])
def reset_password(request):
    print "start reset password"
    form = PasswordChangeForm()
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = user.username
            pwd = form.cleaned_data["password1"]
            new_user = auth.authenticate(username=username, password=pwd)
            auth.login(request, new_user)
            success_info = {
                "success": True,
                "data": {
                    "url": "/"
                }
            }
            return HttpResponse(json.dumps(success_info), content_type="application/json")
        else:
            print form.errors
            error_info = {"success": False}
            data = {}
            errors = form.errors
            if "password1" in errors:
                data["pwd"] = errors["password1"][0]
            if "password2" in errors:
                data["pwd-confirm"] = errors["password2"][0]
            if "phoneNum" in errors:
                data["mobile"] = errors["phoneNum"][0]
            if "code" in errors:
                data["verifycode"] = errors["code"][0]
            error_info["data"] = data
            return HttpResponse(json.dumps(error_info), content_type="application/json")

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render(request, "Profile/reset-pwd.html", args)


@login_required()
def user_profile_modify(request):
    if request.method == "POST":
        form = ProfileChangeForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({"success": True, "data": {}}),
                                content_type="application/json")
        else:
            print form.errors
            return HttpResponse(simplejson.dumps({"success": False, "data": {"unknown": "未知错误，请联系管理员"}}),
                                content_type="application/json")

    else:
        form = ProfileChangeForm()
        args = {}
        args.update(csrf(request))
        args["form"] = form
        args["user"] = request.user

        return render(request, "Profile/modify-person-info.html", args)




def from_size_check_required(method):
    def wrapper(request, *args, **kwargs):
        try:
            start = int(request.GET.get("from", "0"))
        except ValueError:
            raise Http404
        try:
            size = int(request.GET.get("size", "12"))
            if size < 0:
                raise Http404
        except ValueError:
            raise Http404
        return method(request, size=size, start=start,
                      *args, **kwargs)
    return wrapper


@require_GET
@login_required()
@from_size_check_required
def mine_start(request, start, size):
    """我发布的活动"""
    user = request.user
    acts = Activity.objects.filter(host=user, is_active=True).order_by("-created_at")[start: start+size]
    return render(request, "Profile/start.html", {
        "activities": acts,
        "user": user
    })

@require_GET
@login_required()
@from_size_check_required
def mine_apply(request, start, size):
    """我申请的活动"""
    user = request.user
    acts = Activity.objects.filter(applications_through__user=user,
                                   applications_through__status="applying",
                                   is_active=True)[start:start+size]
    return render(request, "Profile/apply.html", {
        "activity": acts,
        "user": user
    })


@require_GET
@login_required()
@from_size_check_required
def mine_group(request, start, size):
    """我的米团"""
    user = request.user
    contributions = RiceTeamContribution.objects.filter(team=user.rice_team,
                                                        user__profile__is_active=True)[start:start+size]
    return render(request, "Profile/group.html", {
        "user": user,
        "contributions": contributions
    })


@require_GET
@login_required()
@from_size_check_required
def mine_like(request, start, size):
    """我关注的活动"""
    user = request.user
    acts = Activity.objects.filter(like_through__user=user, is_active=True)[start:start+size]
    return render(request, "Profile/like.html", {
        "activity": acts,
        "user": user
    })


def send_verify_code(request):
    phone = request.POST.get("mobile", "")
    print phone
    code = ""
    for i in range(0, 6):
        code += random.choice("1234567890")

    if VerifyCode.objects.filter(phoneNum=phone, is_active=True).exists():

        record = VerifyCode.objects.filter(phoneNum=phone, is_active=True)[0]
        tz = timezone.get_current_timezone()
        if (tz.normalize(timezone.now())-record.created_at).total_seconds() > 60:
            print "A"
            VerifyCode.objects.filter(phoneNum=phone).update(is_active=False)
            print "C"
            record = VerifyCode.objects.create(phoneNum=phone, code=code)
        else:
            print "code request rejected"
            return HttpResponse("")
    else:
        print "B"
        record = VerifyCode.objects.create(phoneNum=phone, code=code)

    code = settings.SMS_TEMPLATE % code
    print code
    response_status = send_sms(settings.SMS_KEY, code, phone)
    status_code = int(re.match(r'\{"code":(-?\d+),.*', response_status).group(1))
    print response_status
    if status_code != 0:
        print "error!"
        record.is_active = False
        record.save()
    return HttpResponse("")