# coding=utf-8
from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect

from Activity.models import Activity, ActivityType
from Homepage.models import HomepageIssue, HomepagePoster


def index_list(request):
    recent_issue = HomepageIssue.objects.all()[0]
    banners = HomepagePoster.objects.filter(issue=recent_issue,
                                            poster_type=0)
    footer = HomepagePoster.objects.filter(issue=recent_issue,
                                           poster_type=1)[0]
    activities = Activity.objects.filter(recommended=True).order_by("recommended_level", "-created_at")
    act_types = ActivityType.objects.all()

    return render(request, "list.html", {
        "homepage_posters": banners,
        "footer": footer,
        "activity_types": act_types,
        "activities": activities
    })


def search_list(request):
    hot = request.GET.get("hot", "")
    stype = request.GET.get("type", "")
    q = request.GET.get("q", "")
    loc = request.GET.get("loc", "")
    act = None

    print hot, stype, q, loc

    order_in_reward = False

    def filter_hot(activity):
        if activity is None:
            queryset = Activity.objects
        else:
            queryset = activity
        if hot == "0":
            activity = queryset.filter(recommended=True,
                                       is_active=True).order_by("-recommended_level", '-created_at')[0:12]
        elif hot == "1":
            activity = queryset.filter(time_limited=True, is_active=True)
        elif hot == "2":
            activity = queryset.filter(num_limited=True, is_active=True)
        elif hot == "4":
            order_in_reward = True
            activity = queryset.all()
        else:
            activity = queryset.all()
        return activity

    act = filter_hot(act)
    act_types = ActivityType.objects.all()

    def filter_type(activity):
        if activity is None:
            queryset = Activity.objects
        else:
            queryset = activity
        try:
            stype_num = int(stype)
            if stype_num <= 0:
                return activity
            elif stype_num > len(act_types):
                return queryset.filter(activity_type=None)
            else:
                type_obj = act_types[stype_num-1]
                activity = queryset.filter(activity_type=type_obj)
                return activity
        except ValueError, IndexError:
            return activity

    act = filter_type(act)

    def filter_q(activity):
        if activity is None:
            queryset = Activity.objects
        else:
            queryset = activity
        if q == "":
            return activity
        else:
            activity = queryset.filter(name__contains=q)
            return activity

    act = filter_q(act)

    def filter_loc(activity):
        if activity is None:
            queryset = Activity.objects
        else:
            queryset = activity
        if loc == "":
            return activity
        else:
            activity = queryset.filter(location__contains=loc)
            return activity

    act = filter_loc(act)

    if order_in_reward and act is not None:
        act = act.order_by("-reward")

    recent_issue = HomepageIssue.objects.all()[0]
    banners = HomepagePoster.objects.filter(issue=recent_issue,
                                            poster_type=0)
    footer = HomepagePoster.objects.filter(issue=recent_issue,
                                           poster_type=1)[0]

    return render(request, "list.html", {
        "homepage_posters": banners,
        "footer": footer,
        "activity_types": act_types,
        "activities": act
    })



