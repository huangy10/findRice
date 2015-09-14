from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import NotificationCenter, Notification
from .models import SystemNotification, ActivityNotification, WelfareNotification
from findRice.utils import choose_template_by_device
from Profile.utils import profile_active_required

# Create your views here.


@login_required()
@profile_active_required
def notification_center(request):
    center = request.user.notification_center
    sys_msg = SystemNotification.objects.filter(notification_center=center)
    act_msg = ActivityNotification.objects.filter(notification_center=center)
    wel_msg = WelfareNotification.objects.filter(notification_center=center)

    msg_list = list(sys_msg[0:20]) + list(act_msg[0:20]) + list(wel_msg[0:20])
    msg_list_order = sorted(msg_list, key=lambda msg: msg.created_at, reverse=True)[0:20]

    response = render(request,
                      choose_template_by_device(request,
                                                "Notification/message.html",
                                                "Notification/mobile/message.html"),
                      {"msgs": msg_list_order,
                       "user": request.user})

    # mark all these notifications as read
    sys_msg.update(read=True)
    act_msg.update(read=True)
    wel_msg.update(read=True)

    return response


@login_required()
@profile_active_required
def unread_messages(request):
    center = request.user.notification_center
    return JsonResponse({"success": True, "data": {"unread": center.unread_notifications_count}}, content_type='text/html')
