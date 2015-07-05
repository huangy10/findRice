# coding=utf-8
from django.shortcuts import render
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.views.decorators.http import require_http_methods, require_GET

from .forms import UserRegisterFormStep1, UserRegisterFormStep2
from .forms import PasswordChangeForm
from Activity.models import Activity
from Profile.models import RiceTeamContribution, RiceTeam
# Create your views here.


@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        pwd = request.POST.get("pwd").strip()

        user = auth.authenticate(username=username, password=pwd)
        if user is not None:
            auth.login(user)
            HttpResponseRedirect("/")
        else:
            HttpResponseRedirect("/login?error=invalid")

    args = {}
    args.update(csrf(request))

    return render(request, "Profile/login.html", args)


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
            return HttpResponseRedirect("/register")
        else:
            print "form invalid"
            print form.errors

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render(request, "Profile/register.html", args)


@require_http_methods(["GET", "POST"])
def register_step_2(request):
    user = request.user
    print user
    if not user.is_authenticated() or user.profile.is_active:
        return HttpResponseRedirect("/register/basic")

    form = UserRegisterFormStep2()
    if request.method == "POST":
        form = UserRegisterFormStep2(request.POST, instance=user.profile, initial={})
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
        else:
            print "form invalid"
            print form.errors

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render(request, "Profile/register-addon.html", args)


@require_http_methods(["GET", "POST"])
def reset_password(request):
    form = PasswordChangeForm()
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            print "change pwd form valid"
            user = form.save()
            username = user.username
            pwd = form.cleaned_data["password1"]
            new_user = auth.authenticate(username=username, password=pwd)
            auth.login(request, new_user)
            return HttpResponseRedirect("/")
        else:
            print "form invalid"
            print form.errors

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render(request, "Profile/reset-pwd.html", args)


def from_size_check_required(method):
    def wrapper(request, *args, **kwargs):
        if "from" not in request.GET or "size" not in request.GET:
            raise Http404
        try:
            start = int(request.GET.get("from"))
            size = min(int(request.GET.get("size")), 12)
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
    return render(request, "Profile/apply.html", {
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