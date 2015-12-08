# coding=utf-8
import datetime
import logging
import re
from PIL import Image

from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import UserProfile
from .models import VerifyCode
from .tasks import create_zipped_avatar


logger = logging.getLogger(__name__)


class UserRegisterForm(forms.Form):

    nickname = forms.CharField(max_length=100)
    password1 = forms.CharField(max_length=30)
    password2 = forms.CharField(max_length=30)
    phone_num = forms.CharField(max_length=20)
    avatar = forms.FileInput()
    code = forms.CharField(max_length=6)
    promotion_code = forms.CharField(required=False)
    birthDate = forms.DateField()
    gender = forms.CharField(max_length=2)

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        if len(args) < 2 or 'avatar' not in args[1]:
            self.avatar = None
        else:
            self.avatar = args[1]['avatar']

    def clean(self):
        """ 在这里检查验证码和password2
        """
        # 检查密码的匹配
        password2 = self.cleaned_data['password2']
        password1 = self.cleaned_data['password1']
        if not 8 < len(password1) < 30:
            self.add_error('password1', u'密码长度不符合要求，密码长度请控制在8-30位')
        if password1 != password2:
            self.add_error('password2', u'两次输入的密码不一致')
        # 检查验证码
        code = self.cleaned_data['code']
        phone = self.cleaned_data['phone_num']
        if get_user_model().objects.filter(profile__phoneNum=phone).exists():
            self.add_error('phone_num', u"该手机号已经被注册了")
            return
        time_threshold = timezone.now() - datetime.timedelta(minutes=5)
        if not VerifyCode.objects.filter(
                phoneNum=phone, code=code, created_at__gt=time_threshold, is_active=True).exists():
            self.add_error('code', u'验证码错误')
        # 验证头像的格式，只接受图像文件
        try:
            if self.avatar is not None:
                Image.open(self.avatar)
        except IOError:
            self.add_error('avatar', u'头像格式错误')

    def save(self):
        phone = self.cleaned_data['phone_num']
        user = get_user_model().objects.create(username=phone)
        user.set_password(self.cleaned_data['password1'])
        user.profile.phoneNum = phone
        user.profile.avatar = self.avatar
        user.profile.gender = self.cleaned_data['gender']
        user.profile.name = self.cleaned_data['nickname']
        user.profile.birthDate = self.cleaned_data['birthDate']
        user.profile.is_active = True
        try:
            if "promotion_code" in self.cleaned_data:
                leader = get_user_model().objects.get(profile__promotion_code=self.cleaned_data['promotion_code'])
                user.profile.team_leader = leader
        except ObjectDoesNotExist:
            pass
        # if self.rice_leader is not None:
        #     user.profile.rice_leader = self.rice_leader
        user.save()
        logger.debug(u'用户%s成功完成了注册' % phone)
        # 完成注册以后将无用的验证码删除
        VerifyCode.objects.filter(phoneNum=phone).delete()
        return user


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(max_length=30)
    password2 = forms.CharField(max_length=30)
    phone_num = forms.CharField(max_length=20)
    code = forms.CharField(max_length=6)

    # def clean_phone_num(self):
    #     phone_num = self.cleaned_data['phone_num']
    #     if not get_user_model().objects.filter(username=phone_num).exists():
    #         raise forms.ValidationError(u'该手机号尚未被注册', code='phone_num_does_not_exists')
    #     return phone_num

    def clean(self):
        """ 在这里检查验证码和password2
        """
        # 检查密码的匹配
        password2 = self.cleaned_data['password2']
        password1 = self.cleaned_data['password1']
        if not 8 < len(password1) < 30:
            self.add_error('password1', u'密码长度不符合要求，密码长度请控制在8-30位')
        if password1 != password2:
            self.add_error('password2', u'两次输入的密码不一致')
        # 检查验证码
        code = self.cleaned_data['code']
        phone = self.cleaned_data['phone_num']
        if not get_user_model().objects.filter(profile__phoneNum=phone).exists():
            self.add_error('phone_num', u'该手机号尚未被注册')
        time_threshold = timezone.now() - datetime.timedelta(minutes=5)
        if not VerifyCode.objects.filter(
                phoneNum=phone, code=code, created_at__gt=time_threshold, is_active=True).exists():
            self.add_error('code', u'验证码错误')

    def save(self):
        phone = self.cleaned_data['phone_num']
        user = get_user_model().objects.get(username=phone)
        user.set_password(self.cleaned_data['password1'])
        user.profile.phoneNum = phone
        user.save()
        logger.debug(u'用户%s修改了密码' % phone)
        return user


class PasswordChangeForm(forms.Form):

    phoneNum = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        "id": "mobile",
        "placeholder": "请输入手机号码",
    }))

    code = forms.CharField(max_length=10, widget=forms.TextInput(attrs={
        "id": "verifycode",
        "name": "verifycode",
        "placeholder": "请输入验证码"
    }))

    password1 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        "id": "pwd",
        "placeholder": "请输入密码"
    }))

    password2 = forms.CharField(max_length=30, widget=forms.PasswordInput(attrs={
        "id": "pwd-confirm",
        "placeholder": "请再次输入密码"
    }))

    error_messages = {
        'password_mismatch': "两次输入的密码不匹配",
        'user_does_not_exist': "对应用户不存在",
        "code_mismatch": "验证码不匹配",
        "password_too_short": "密码太短，密码的长度至少在6位",
    }

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.record = None
        self.user = None

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 6:
            raise forms.ValidationError(
                self.error_messages['password_too_short'],
                code='password_too_short'
            )
        return password1

    def clean_phoneNum(self):
        phone = self.cleaned_data.get("phoneNum")
        try:
            user = get_user_model().objects.get(profile__phoneNum=phone, profile__is_active=True)
            self.user = user
        except ObjectDoesNotExist:
            raise forms.ValidationError(
                self.error_messages["user_does_not_exist"],
                code="user_does_not_exist"
            )
        return phone

    def clean_code(self):
        code = self.cleaned_data.get("code")
        phone = self.cleaned_data.get("phoneNum")
        try:
            time_threshold = timezone.now() - datetime.timedelta(minutes=5)
            record = VerifyCode.objects.get(phoneNum=phone,
                                            code=code,
                                            is_active=True,
                                            created_at__gt=time_threshold)
            # record.is_active = False
            # record.save()
            self.record = record
        except ObjectDoesNotExist:
            raise forms.ValidationError(self.error_messages["code_mismatch"],
                                        code="code_mismatch")
        return code

    def save(self, commit=True):
        if self.user is not None and commit:
            self.user.set_password(self.cleaned_data["password1"])
            self.user.save()
            self.record.is_active = False
            self.record.save()
        else:
            raise ValueError
        return self.user


class ProfileChangeForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ("name", "phoneNum", "birthDate", "avatar", "gender")
        widgets = {
            "phoneNum": forms.TextInput(attrs={
                "id": "mobile",
                "placeholder": u"请输入手机号码",
            }),
            "name": forms.TextInput(attrs={
                "id": "name",
                "name": "name",
                "placeholder": u"请输入姓名/企业名",
            }),
            "birthDate": forms.TextInput(attrs={
                "id": "bday",
                "name": "bday",
                "class": "form-control bday-i",
                "size": "16",
                "value": "",
                "readonly placeholder": u"请选择您的出生日期",
            }),
            "gender": forms.HiddenInput(attrs={
                "id": "gender",
                "name": "gender",
            }),
            "avatar": forms.FileInput(attrs={
                "id": "portrait",
                "class": "fn-hide",
            }),
        }
