from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import NotificationCenter, Notification
from .models import SystemNotification, ActivityNotification, WelfareNotification

# Create your views here.


@login_required()
def notification_center(request):
    center = request.user.notification_center
    sys_msg = SystemNotification.objects.filter(notification_center=center,
                                                read=False)
    act_msg = ActivityNotification.objects.filter(notification_center=center,
                                                  read=False)
    wel_msg = WelfareNotification.objects.filter(notification_center=center,
                                                 read=False)
    msg_list = list(sys_msg) + list(act_msg) + list(wel_msg)
    msg_list_order = sorted(msg_list, key=lambda msg: msg.created_at, reverse=True)

    return render(request, "Notification/message.html", {
        "msgs": msg_list_order,
        "user": request.user
    })

@login_required()
def unread_messages(request):
    center = request.user.notification_center
    return JsonResponse({"success": True, "data": {"unread": center.unread_notifications_count}})