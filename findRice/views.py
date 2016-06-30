# coding=utf-8
import json
import logging

from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from django.utils import timezone

from Activity.models import Activity, ActivityType
from Profile.utils import from_size_check_required
from Homepage.models import HomepageIssue, HomepagePoster
from findRice.utils import choose_template_by_device

logger = logging.getLogger(__name__)


@from_size_check_required
def index_list(request, start, size):
    if "callback" in request.GET:
        activities = Activity.objects.filter(is_active=True, is_published=True, identified=True)\
            .order_by("recommended_level", "-created_at")[start: start+size]
        data = render_to_string(choose_template_by_device(request,
                                                          "list_item.html",
                                                          "home-mobile/list_item.html"),
                                {"activities": activities, 'user': request.user})
        data = {"html": data, "size": len(activities)}
        return HttpResponse(request.GET.get("callback", "")+'('+json.dumps(data)+')', content_type="text/javascript")

    if HomepageIssue.objects.exists():
        recent_issue = HomepageIssue.objects.all()[0]
        banners = HomepagePoster.objects.filter(issue=recent_issue,
                                                poster_type=0)
        try:
            footer = HomepagePoster.objects.filter(issue=recent_issue,
                                                   poster_type=1).first()
        except IndexError:
            footer = None
    else:
        banners = None
        footer = None
    activities = Activity.objects.filter(
        is_active=True, is_published=True, identified=True, end_time__lt=timezone.now()
    ).order_by("recommended_level", "-created_at")[start: start+size]
    act_types = ActivityType.objects.all()

    user = None
    if request.user.is_authenticated():
        user = request.user
    args = {
        "homepage_posters": banners,
        "footer": footer,
        "activity_types": act_types,
        "activities": activities,
        "user": user,
    }
    args.update(csrf(request))
    return render(request, choose_template_by_device(request, "list.html", "home-mobile/list.html"), args)


@from_size_check_required
def search_list(request, start, size):
    hot = request.GET.get("hot", "")
    stype = request.GET.get("type", "")
    q = request.GET.get("q", "")
    loc = request.GET.get("loc", "")
    user = request.user
    logger.debug(u"搜索参数为: hot=%s|type=%s|loc=%s|q=%s" % (hot, stype, loc, q))
    if not user.is_authenticated():
        user = None
    act = None

    def filter_hot(activity):
        if activity is None:
            queryset = Activity.objects
        else:
            queryset = activity
        if hot == "0":
            activity = queryset.filter(recommended=True,
                                       is_active=True, is_published=True,
                                       identified=True).order_by("-recommended_level", '-created_at')
        elif hot == "1":
            activity = queryset.filter(time_limited=True, is_active=True, is_published=True, identified=True)
        elif hot == "2":
            activity = queryset.filter(num_limited=True, is_active=True, is_published=True, identified=True)
        elif hot == "3":
            activity = queryset.filter(is_active=True, is_published=True, identified=True)
        else:
            activity = queryset.filter(is_active=True, is_published=True, identified=True)
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
            if stype_num == 0 or stype_num > len(act_types):
                activity = queryset.all()
                return activity
            elif stype_num < 0:
                return queryset.filter(activity_type=None, is_active=True, is_published=True)
            else:
                type_obj = act_types[stype_num-1]
                activity = queryset.filter(activity_type=type_obj, is_active=True, is_published=True)
                return activity
        except (ValueError, IndexError):
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
            activity = queryset.filter(name__contains=q, is_active=True, is_published=True)
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
            if "|" in loc:
                prov, city = loc.split("|")
                if prov == u"全部地区":
                    return activity
                if city == u"全部地区":
                    activity = queryset.filter(province=prov, is_active=True, is_published=True)
                else:
                    activity = queryset.filter(city=city, province=prov, is_active=True, is_published=True)
            else:
                activity = queryset.filter(location__contains=loc, is_active=True, is_published=True)
            return activity

    act = filter_loc(act)

    if hot == "3" and act is not None:
        act = act.order_by("-reward")

    if "callback" in request.GET:
        act_data = act[start: start+size]
        data = render_to_string(choose_template_by_device(request, "list.html", "home-mobile/list.html"),
                                {"activities": act_data,
                                 'user': request.user})
        data = {"html": data, "size": len(act_data)}
        return HttpResponse(request.GET.get("callback", "")+'('+json.dumps(data)+')', content_type="text/javascript")

    if HomepageIssue.objects.exists():
        recent_issue = HomepageIssue.objects.all()[0]
        banners = HomepagePoster.objects.filter(issue=recent_issue,
                                                poster_type=0)
        try:
            footer = HomepagePoster.objects.filter(issue=recent_issue,
                                                   poster_type=1).first()
        except IndexError:
            footer = None
    else:
        banners = None
        footer = None

    def stype_transfer(a):
        if a == "":
            return ""
        else:
            return int(a)

    # city display
   
    if not loc == "":
        prov, city = loc.split("|")
        if prov in [u"北京市", u"重庆市", u"上海市", u"天津市"] or city == u"全部地区":
            city = prov
    else:
        city = None
    args = {
        "user": user,
        "homepage_posters": banners,
        "footer": footer,
        "activity_types": act_types,
        "activities": act[start: start+size],
        "param": {
            "hot": hot,
            "q": q,
            "type": stype_transfer(stype),
            "loc": loc,
            "city": city
        }
    }
    args.update(csrf(request))
    return render(request, choose_template_by_device(request, "list.html", "home-mobile/list.html"), args)


def search_page(request):
    args = {}
    if request.user.is_authenticated():
        args['user'] = request.user
    return render(request, "home-mobile/search.html", args)


def statement(request):
    if request.user and request.user.is_authenticated():
        user = request.user
    else:
        user = None
    return render(request,
                  choose_template_by_device(request,
                                            "statement.html",
                                            "home-mobile/statement.html"),
                  {'user': user})


