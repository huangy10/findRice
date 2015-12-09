# coding=utf-8
import random
import re
import simplejson
import json
import excel_response
import logging

from django.utils import timezone
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.core.context_processors import csrf
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404, HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from django.db.models import F, Sum

from .forms import UserRegisterForm, PasswordResetForm
from .forms import PasswordChangeForm, ProfileChangeForm
from Activity.models import Activity, ApplicationThrough
from .models import RiceTeamContribution, UserProfile
from .models import VerifyCode
from .utils import send_sms, from_size_check_required, profile_active_required
from Notification.signals import send_notification
from Promotion.models import ShareRecord
from Welfare.models import WelfareGift
from findRice.utils import choose_template_by_device

from .tasks import create_zipped_avatar
# Create your views here.

logger = logging.getLogger(__name__)

# TODO: 重新改造整个后台的注册、登陆系统


@require_http_methods(["GET", "POST"])
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        pwd = request.POST.get("pwd", "").strip()
        print username, pwd
        user = auth.authenticate(username=username, password=pwd)
        if user is not None and user.is_active:
            auth.login(request, user)
            next_url = request.session.pop('next', '/')
            success_info = {
                "success": True,
                "data": {
                    "url": next_url
                }
            }
            return HttpResponse(json.dumps(success_info))
        else:
            error_info = {
                "success": False
            }
            data = {}
            if not auth.get_user_model().objects.filter(username=username).exists():
                data['username'] = '该用户名不存在'
            else:
                data['pwd'] = '密码错误'
            error_info['data'] = data
            return HttpResponse(json.dumps(error_info))
    # 将在GET参数里面的next参数暂时存储在session中
    request.session["next"] = request.GET.get("next", "/")
    args = {}
    args.update(csrf(request))
    # 这个next参数会被埋在登陆页面的注册按钮，构造/register?next=/url/to/next的链接
    args['next'] = request.GET.get("next", None)

    return render(request, choose_template_by_device(request, "Profile/new_login.html", "Profile/mobile/new_login.html"), args)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user_auth = auth.authenticate(username=user.username, password=request.POST["password1"])
            auth.login(request, user_auth)
            next_url = request.session.pop('next', '/')
            return HttpResponse(json.dumps({'success': True, 'data': {'url': next_url}}))
        else:
            errors = form.errors
            logger.debug(u'用户注册过程中出错，错误信息为：%s' % errors)
            return HttpResponse(json.dumps({'success': False, 'data': errors}))
    # TODO: 这里为了稳定性考虑，避免使用session，故code应该埋点在网页中被post上来
    if 'next' in request.GET:
        request.session['next'] = request.GET['next']
    args = {}
    args.update(csrf(request))
    args['form'] = UserRegisterForm()
    # TODO: 注意这里要从next参数里面解析code
    if "next" in request.GET:
        next_url = request.GET.get('next')
        find_code = re.match(r'/action/(\d+)\?code=(\w+)', next_url)
        if find_code is not None:
            promotion_code = find_code.groups()[1]
        else:
            promotion_code = None
    elif "code" in request.GET:
        promotion_code = request.GET.get("code")
    else:
        promotion_code = None
    args['promotion_code'] = promotion_code

    # TODO: 注意，这里模板渲染应当不再使用form
    return render(request,
                  choose_template_by_device(request,
                                            "Profile/new_register.html",
                                            "Profile/mobile/new_register.html"),
                  args)


@require_POST
@login_required()
@profile_active_required
def user_modify(request):
    profile = request.user.profile
    if "name" in request.POST:
        profile.name = request.POST.get("name", "NAME")
    if "bday" in request.POST:
        profile.birthDate = timezone.datetime.strptime(request.POST["bday"], "%Y-%m-%d").date()
    if "gender" in request.POST:
        profile.gender = request.POST["gender"]
    # if "mobile" in request.POST:
    #     profile.phoneNum = request.POST["mobile"]
    if "portrait" in request.FILES:
        profile.avatar = request.FILES["portrait"]
        profile.avatar_zipped = None
    profile.save()
    create_zipped_avatar.delay(profile, force=True)
    data = {
        "name": profile.name,
        "gender": profile.get_gender_display(),
        "age": str(profile.age) + u'岁',
        "portrait": profile.avatar_url
    }
    logger.debug(u'用户信息修改成功，修改值为%s' % data)
    return JsonResponse({
        "success": True,
        "data": data
    }, content_type='text/html')


@require_http_methods(["GET", "POST"])
def reset_password(request):
    form = PasswordChangeForm()
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save()
            # 当用户没有登陆时将其导到登陆界面，否则返回首页
            success_info = {
                "success": True,
                "data": {
                    "url": "/" if request.user.is_authenticated() else '/login'
                }
            }
            return HttpResponse(json.dumps(success_info))
        else:
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
            if data == {}:
                data["unknown"] = "未知错误，请联系管理员"
            error_info["data"] = data
            return HttpResponse(json.dumps(error_info))

    args = {}
    args.update(csrf(request))
    args['form'] = form

    return render(request, choose_template_by_device(request, "Profile/find_password.html", "Profile/mobile/find_password.html"), args)


@login_required()
@profile_active_required
def user_profile_modify(request):
    if request.method == "POST":
        form = ProfileChangeForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return HttpResponse(simplejson.dumps({"success": True, "data": {}}),
                                content_type="application/json")
        else:
            logger.debug(u"用户|%s(id: %s)|信息修改失败，错误信息为: %s" % (
                request.user.profile.name, request.user.id, form.errors.as_data))
            return HttpResponse(simplejson.dumps({"success": False, "data": {"unknown": "未知错误，请联系管理员"}}),
                                content_type="application/json")

    else:
        form = ProfileChangeForm()
        args = {}
        args.update(csrf(request))
        args["form"] = form
        args["user"] = request.user
        return render(request,
                      choose_template_by_device(request,
                                                "Profile/modify-person-info.html",
                                                "Profile/mobile/modify-person-info.html"),
                      args)


@require_GET
@login_required()
@profile_active_required
@from_size_check_required
def mine_start(request, start, size):
    """我发布的活动"""
    user = request.user
    acts = Activity.objects.filter(host=user, is_active=True).order_by("-created_at")[start: start+size]
    if "callback" in request.GET:
        data = render_to_string(choose_template_by_device(request,
                                                          "Profile/start_item.html",
                                                          "Profile/mobile/start_item.html"),
                                {"activities": acts, "user": user})
        data = {"html": data, "size": len(acts)}
        return HttpResponse(request.GET.get("callback", "")+'('+json.dumps(data)+')', content_type="text/javascript")
    args = {
        "activities": acts,
        "user": user
    }
    args.update(csrf(request))
    return render(request, choose_template_by_device(request, "Profile/start.html", "Profile/mobile/start.html"), args)


@require_GET
@login_required()
@profile_active_required
@from_size_check_required
def mine_apply(request, start, size):
    """我申请的活动"""
    user = request.user
    acts = Activity.objects.filter(applications_through__user=user,
                                   applications_through__status__in=["applying", "approved", "denied", "finished"],
                                   applications_through__is_active=True,
                                   is_active=True)[start:start+size]
    if "callback" in request.GET:
        data = render_to_string(choose_template_by_device(request,
                                                          "Profile/apply_item.html",
                                                          "Profile/mobile/apply_item.html"),
                                {"activities": acts, "user": user})
        data = {"html": data, "size": len(acts)}
        return HttpResponse(request.GET.get("callback", "")+'('+json.dumps(data)+')', content_type="text/javascript")
    args = {
        "activities": acts,
        "user": user
    }
    args.update(csrf(request))
    return render(request, choose_template_by_device(request, "Profile/apply.html", "Profile/mobile/apply.html"), args)


@require_GET
@login_required()
@profile_active_required
@from_size_check_required
def mine_group(request, start, size):
    """我的米团"""
    user = request.user
    # 注意，这里先去掉分页，直接返回所有的米团成员
    # contributions = RiceTeamContribution.objects.filter(team=user.rice_team,
    #                                                     user__profile__is_active=True)[start:start+size]
    # contributions = RiceTeamContribution.objects.filter(leader=user,
    #                                                     user__is_active=True)
    team_members = get_user_model().objects.filter(profile__team_leader=user).\
        annotate(contributed_coin=Sum("my_contributions__contributed_coin"))
    args = {
        "user": user,
        "member_num": team_members.count(),
        "members": team_members
    }
    args.update(csrf(request))
    return render(request, choose_template_by_device(request, "Profile/group.html", "Profile/mobile/group.html"), args)


@require_GET
@login_required()
@profile_active_required
@from_size_check_required
def mine_like(request, start, size):
    """我关注的活动"""
    user = request.user
    acts = Activity.objects.filter(like_through__user=user,
                                   is_active=True,
                                   like_through__is_active=True)[start:start+size]
    if "callback" in request.GET:
        data = render_to_string(choose_template_by_device(request,
                                                          "Profile/like_item.html",
                                                          "Profile/mobile/like_item.html"),
                                {"activities": acts, "user": user})
        data = {"html": data, "size": len(acts)}
        return HttpResponse(request.GET.get("callback", "")+'('+json.dumps(data)+')', content_type="text/javascript")
    args = {
        "activities": acts,
        "user": user
    }
    args.update(csrf(request))
    return render(request, choose_template_by_device(request, "Profile/like.html", "Profile/mobile/like.html"), args)


def send_verify_code(request):
    phone = request.POST.get("mobile", "")
    code = ""
    for i in range(0, 6):
        code += random.choice("1234567890")
    if VerifyCode.objects.filter(phoneNum=phone, is_active=True).exists():

        record = VerifyCode.objects.filter(phoneNum=phone, is_active=True)[0]
        if (timezone.now()-record.created_at).total_seconds() > 60:
            VerifyCode.objects.filter(phoneNum=phone).update(is_active=False)
            record = VerifyCode.objects.create(phoneNum=phone, code=code)
        else:
            return JsonResponse({'success': False, 'data': {}}, content_type='text/html')
    else:
        record = VerifyCode.objects.create(phoneNum=phone, code=code)

    code = settings.SMS_TEMPLATE % code
    response_status = send_sms(settings.SMS_KEY, code, phone)
    status_code = int(re.match(r'\{"code":(-?\d+),.*', response_status).group(1))
    # if status_code != 0:
    #     record.is_active = False
    #     record.save()
    #     return JsonResponse({'success': False, 'data': {}}, content_type='text/html')
    return JsonResponse({'success': True}, content_type='text/html')

#
# @login_required()
# @profile_active_required
# def manage_an_activity(request):
#     if request.method == "POST":
#         optype = request.POST.get("optype", "")
#         action_id = request.POST.get("action", "")
#         target_id = request.POST.get("target", "")
#     else:
#         optype = request.GET.get("optype", "")
#         action_id = request.GET.get("action", "")
#         target_id = request.GET.get("target", "")
#     activity = get_object_or_404(Activity, id=int(action_id))
#     if not activity.host == request.user:
#         return JsonResponse({"success": False, "data": {"error": "Permission Denied"}}, content_type='text/html')
#     elif not activity.is_active:
#         return JsonResponse({"success": False, "data": {"error": "该活动不存在"}}, content_type='text/html')
#     if optype == "approve":
#         if ApplicationThrough.objects.filter(activity=activity, is_active=True, status="approved").count() >= activity.max_attend:
#             return JsonResponse({"success": True, "data": {"error": "该活动已报满"}}, content_type='text/html')
#         target = get_object_or_404(get_user_model(), id=target_id)
#         applicant = get_object_or_404(ApplicationThrough, activity=activity, user=target, is_active=True)
#         applicant.status = "approved"
#         applicant.save()
#         # send a message to the target
#         send_notification.send(sender=get_user_model(),
#                                notification_center=target.notification_center,
#                                notification_type="activity_notification",
#                                activity=activity,
#                                user=target,
#                                activity_notification_type="apply_approved")
#         # 检查这个活动是否是用于认证的用户，如果是的话，令申请者成为认证用户
#         identification_act = Activity.objects.identification_act
#         if activity.id == identification_act.id:
#             target.profile.identified = True
#             target.profile.identified_date = timezone.now()
#             target.profile.save()
#
#         return JsonResponse({"success": True, "data": {}}, content_type='text/html')
#     elif optype == "approve_cancel":
#         target = get_object_or_404(get_user_model(), id=target_id)
#         applicant = get_object_or_404(ApplicationThrough, activity=activity, user=target, is_active=True)
#         if not applicant.status == "approved":
#             return JsonResponse({"success": False, "data": {}}, content_type='text/html')
#         applicant.status = "applying"
#         applicant.save()
#         # 检查这个活动是否是用于认证的用户，如果是的话，则剥夺该用户的认证资格
#         identification_act = Activity.objects.identification_act
#         if activity.id == identification_act.id:
#             target.profile.identified = False
#             target.profile.save()
#         # I'm not sure about which kind of notification should be sent here
#         return JsonResponse({"success": True, "data": {}}, content_type='text/html')
#     elif optype == "deny":
#         target = get_object_or_404(get_user_model(), id=target_id)
#         applicant = get_object_or_404(ApplicationThrough, activity=activity, user=target, is_active=True)
#         applicant.status = "denied"
#         applicant.save()
#         # No notification if defined here
#         # send a message to the target
#         send_notification.send(sender=get_user_model(),
#                                notification_center=target.notification_center,
#                                notification_type="activity_notification",
#                                activity=activity,
#                                user=target,
#                                activity_notification_type="apply_rejected")
#         return JsonResponse({"success": True, "data": {}}, content_type='text/html')
#     elif optype == "deny_cancel":
#         target = get_object_or_404(get_user_model(), id=target_id)
#         applicant = get_object_or_404(ApplicationThrough, activity=activity, user=target, is_active=True)
#         if not applicant.status == "denied":
#             return JsonResponse({"success": False, "data": {}}, content_type='text/html')
#         applicant.status = "applying"
#         applicant.save()
#         return JsonResponse({"success": True, "data": {}}, content_type='text/html')
#     elif optype == "finish":
#         target = get_object_or_404(get_user_model(), id=target_id)
#         applicant = get_object_or_404(ApplicationThrough, activity=activity, user=target, is_active=True)
#         if not (applicant.status == "approved" and activity.status == 2):
#             return JsonResponse({"success": False, "data": {}}, content_type='text/html')
#         applicant.status = "finished"
#         applicant.save()
#         # Send Notification to the target user
#         send_notification.send(sender=get_user_model(),
#                                notification_center=target.notification_center,
#                                notification_type='activity_notification',
#                                activity=activity,
#                                user=target,
#                                activity_notification_type='activity_finished')
#         # Check if this target user is recommended
#         try:
#             share_record = ShareRecord.objects.get(application=applicant,
#                                                    target_user=target,
#                                                    is_active=True)
#             share_record.finished = True
#             share_record.save()
#             send_notification.send(sender=get_user_model(),
#                                    notification_center=share_record.share.user.notification_center,
#                                    notification_type="activity_notification",
#                                    activity=activity,
#                                    user=target,
#                                    activity_notification_type="share_finished")
#         except ObjectDoesNotExist:
#             logger.debug(u"用户|%s(id: %s)|完成了活动|%s(id: %s)|，但是没有找到相应分享链接" % (
#                 target.username, target.id, activity.name, activity.id))
#
#         return JsonResponse({"success": True, "data": {}}, content_type='text/html')
#     elif optype == "finish_cancel":
#         return JsonResponse({"success": False, "data": {}}, content_type='text/html')
#     elif optype == "detail":
#         pass
#     elif optype == "excel":
#         def generate_excel_data():
#             applicants = ApplicationThrough.objects.filter(activity=activity,
#                                                            is_active=True)
#             column_names = [u"用户姓名", u"性别", u"出生日期", u"年龄", u"联系方式", u"报名时间", u"申请状态"]
#
#             def row_generator(app):
#                 # accept the applicant data as input, output the row data for the excel file
#                 row_user_profile = app.user.profile
#                 row_data = [row_user_profile.name,
#                             row_user_profile.get_gender_display(),
#                             row_user_profile.birthDate.strftime("%Y-%m-%d"),
#                             str(row_user_profile.age),
#                             row_user_profile.phoneNum,
#                             timezone.make_naive(timezone.localtime(app.apply_at)).strftime("%Y-%m-%d %H-%M-%S"),
#                             app.get_status_display()]
#                 return row_data
#
#             data = map(row_generator, applicants)
#             return [column_names] + data
#         excel_data = generate_excel_data()
#         return excel_response.ExcelResponse(excel_data, output_name=(activity.name+u"报名列表").encode("utf-8"))
#     elif optype == "ready_required":
#         pass


@login_required()
def manage_an_activity2(request):
    user = request.user
    # 解析操作参数
    if request.method == 'GET':
        optype = request.GET['optype']
        action_id = request.GET['action']
        target_id = request.GET['target']
    else:
        optype = request.POST["optype"]
        action_id = request.POST["action"]
        target_id = request.POST["target"]
    # 获取目标活动
    activity = get_object_or_404(Activity, id=action_id, is_active=True)
    # 检查当前用户的操作权限
    if not activity.host_id != user.id:
        return HttpResponse(json.dumps({'success': False, 'data': {'error': 'Permission Denied'}}))
    # 获取目标用户
    try:
        target_user = get_user_model().objects.select_related('profile').get(id=target_id)
    except ObjectDoesNotExist:
        target_user = None

    # 开始按照optype参数的种类注意检查操作
    if optype == 'approve':
        # 通过申请操作
        if target_user is None:
            return HttpResponse(json.dumps({"success": False, "data": {"error": "参数缺失"}}))
        approved_num = ApplicationThrough.objects.filter(activity=activity, is_active=True, status='approved').count()
        if approved_num >= activity.max_attend:
            # 如果当前已经通过的人数超过了最大运行的人数，则申请失败
            return HttpResponse(json.dumps({"success": False, "data": {"error": "该活动已报满"}}))
        # 查找出申请记录
        try:
            applicant = ApplicationThrough.objects.get(activity=activity, user=target_user, is_active=True,
                                                       status__in=['applying', 'denied'])
            applicant.status = "approved"
            applicant.save()
            send_notification.send(
                sender=get_user_model(),
                notification_center=target_user.notification_center,
                notification_type="activity_notification",
                activity=activity,
                user=target_user,
                activity_notification_type="apply_approved")

            if activity.id in Activity.objects.identification_acts_id:
                target_user.profile.identified = True
                target_user.profile.identified_date = timezone.now()
                target_user.profile.save()
            return HttpResponse(json.dumps({"success": True, "data": {}}))
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({"success": False, "data": {"error": "目标并未申请本活动"}}))

    elif optype == 'approve_cancel':
        # 取消通过目标用户的申请
        if target_user is None:
            return HttpResponse(json.dumps({"success": False, "data": {"error": "参数缺失"}}))
        try:
            applicant = ApplicationThrough.objects.get(
                activity=activity, user=target_user, is_active=True, status='approved')
            applicant.status = 'applying'
            applicant.save()
            # 检查这是否牵涉到认证用户，若是，需要剥夺相关用户的认证
            if activity.id in Activity.objects.identification_acts_id:
                target_user.profile.identified = False
                target_user.profile.save()
            return HttpResponse(json.dumps({"success": True, "data": {}}))
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({"success": False, "data": {"error": "目标并未申请本活动或者其申请未被通过"}}))

    elif optype == 'deny':
        # 拒绝某个人的申请
        if target_user is None:
            return HttpResponse(json.dumps({"success": False, "data": {"error": "参数缺失"}}))
        # 首先检索出目标用户的申请记录, 修改记录的状态
        try:
            applicant = ApplicationThrough.objects.get(activity=activity, user=target_user, is_active=True,
                                                       status__in=['applying', 'approved'])
            applicant.status = 'denied'
            applicant.save()
            # 向目标用户发送通知
            send_notification.send(
                sender=get_user_model(),
                notification_center=target_user.notification_center,
                notification_type="activity_notification",
                activity=activity,
                user=target_user,
                activity_notification_type="apply_rejected")
            # 返回json响应
            return HttpResponse(json.dumps({'success': True, 'data': {}}))
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({"success": False, "data": {"error": "目标并未申请本活动"}}))

    elif optype == 'deny_cancel':
        # 取消拒绝
        if target_user is None:
            return HttpResponse(json.dumps({"success": False, "data": {"error": "参数缺失"}}))
        try:
            applicant = ApplicationThrough.objects.get(
                activity=activity, user=target_user, is_active=True, status='denied')
            applicant.status = 'applying'
            applicant.save()
            return HttpResponse(json.dumps({'success': True, 'data': {}}))
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({"success": False, "data": {"error": "目标并未申请本活动或者其申请未被拒绝"}}))

    elif optype == 'finish':
        # 完成活动
        if target_user is None:
            return HttpResponse(json.dumps({"success": False, "data": {"error": "参数缺失"}}))
        if activity.status != 2:
            return HttpResponse(json.dumps({'success': False, "data": {'error': '活动尚未结束'}}))
        try:
            applicant = ApplicationThrough.objects.get(
                activity=activity, user=target_user, is_active=True, status='approved')
            applicant.status = 'finished'
            applicant.save()
            # 向目标用户发送消息
            send_notification.send(
                sender=get_user_model(),
                notification_center=target_user.notification_center,
                notification_type='activity_notification',
                activity=activity,
                user=target_user,
                activity_notification_type='activity_finished')
            # TODO: 这里要确定应该是向米团长还是活动分享人发送通知
            try:
                share_record = ShareRecord.objects.get(user=user, activity=activity)
            except ObjectDoesNotExist:
                share_record = None
            team_leader = target_user.profile.team_leader
            contribution = RiceTeamContribution.objects.create(
                leader=team_leader, user=target_user, activity=activity)
            if team_leader is not None and activity.host.profile.identified:
                team_leader.profile.coin += contribution.contributed_coin
                team_leader.save()
            return HttpResponse(json.dumps({'success': True, 'data': {}}))
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps({'success': False, 'data': {'error': '目标并未申请或者申请未被通过'}}))

    elif optype == "excel":
        def generate_excel_data():
            applicants = ApplicationThrough.objects.filter(activity=activity,
                                                           is_active=True)
            column_names = [u"用户姓名", u"性别", u"出生日期", u"年龄", u"联系方式", u"报名时间", u"申请状态"]

            def row_generator(app):
                # accept the applicant data as input, output the row data for the excel file
                row_user_profile = app.user.profile
                row_data = [row_user_profile.name,
                            row_user_profile.get_gender_display(),
                            row_user_profile.birthDate.strftime("%Y-%m-%d"),
                            str(row_user_profile.age),
                            row_user_profile.phoneNum,
                            timezone.make_naive(timezone.localtime(app.apply_at)).strftime("%Y-%m-%d %H-%M-%S"),
                            app.get_status_display()]
                return row_data

            data = map(row_generator, applicants)
            return [column_names] + data
        excel_data = generate_excel_data()
        return excel_response.ExcelResponse(excel_data, output_name=(activity.name+u"报名列表").encode("utf-8"))

    else:
        return HttpResponse(json.dumps({'success': False, 'data':{'error': '操作未定义'}}))


@profile_active_required
def mine_info(request):
    user = request.user
    if not user.is_authenticated() or ('code' in request.GET and request.GET['code'] != user.profile.promotion_code
                                       and not user.is_authenticated()):
        # We always attach the promotion code after the user info url
        #  so read the promotion code from GET
        return HttpResponseRedirect('/register?code=' + request.GET['code'])
    args = {"user": user}
    args.update(csrf(request))
    return render(request, "Profile/mobile/mine.html", args)


@require_POST
@login_required()
@profile_active_required
def exchange_for_rmb(request):
    """This view is responsible for managing the rice coin exchange"""
    coin = int(request.POST['num'])                # 需要兑换的米币数量
    zfb_accout = request.POST['alipay']         # 对应的支付宝账户
    rmb = coin * 1
    profile = request.user.profile
    print coin, request.user.profile.coin
    if coin > request.user.profile.coin:
        logger.debug(u"兑换米币失败，对应的用户为|%s(id: %s)|，兑换的米币为%s, 米币余额为%s" %
                     (request.user.profile.name, request.user.username, rmb, request.user.profile.coin))
        return JsonResponse({'success': False, 'data': {'coin': u'米币不足'}}, content_type='text/html')
    else:
        WelfareGift.objects.create(target=request.user, zfb_account=zfb_accout, rmb=rmb)
        profile.coin -= rmb
        profile.save()
        logger.debug(u"兑换米币成功，对应的用户为|%s(id: %s)|，兑换的米币为%s, 米币余额为%s" %
                     (request.user.profile.name, request.user.username, rmb, request.user.profile.coin))
        return JsonResponse({'success': True, 'data': {'coin': profile.coin}}, content_type='text/html')
