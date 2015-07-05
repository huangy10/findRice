# coding=utf-8
from django.shortcuts import render

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