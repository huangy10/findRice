# coding=utf-8
import datetime

from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from .models import UserProfile
from .models import VerifyCode


class UserRegisterFormStep1(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ("username", )
        widgets = {
            "username": forms.TextInput(attrs={
                "id": "username",
                "placeholder": u"请输入邮箱/用户名"
            })
        }
        error_messages = {
            "username": {
                "unique": "该用户名已存在"
            }
        }

    error_messages = {
        'password_mismatch': "两次输入的密码不匹配",
        'username_too_short': "用户名太短",
        'password_too_short': "密码太短，密码的长度至少为8位"
        }
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        "id": "pwd",
        "name": "pwd",
        "placeholder": u"请输入密码"
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        "id": "pwd-confirm",
        "name": "pwd-confirm",
        "placeholder": u"请再次输入密码"
    }))



    def clean_password1(self):
        password1 = self.cleaned_data["password1"]
        if len(password1) < 8:
            raise forms.ValidationError(self.error_messages["password_too_short"],
                                        code="password_too_short")
        return password1

    def clean_username(self):
        username = self.cleaned_data.get("username")
        username = username.strip()
        if len(username) < 8:
            raise forms.ValidationError(
                self.error_messages["username_too_short"],
                code="username_too_short"
            )
        return username

    def save(self, commit=True):
        user = super(UserRegisterFormStep1, self).save(commit=False)
        if commit:
            user.save()
        return user


class UserRegisterFormStep2(forms.ModelForm):

    error_messages = {
        "code_mismatch": u"验证码不匹配",
        "phone_already_exist": u"该手机已注册"
    }

    code = forms.CharField(max_length=6, widget=forms.TextInput(attrs={
        "id": "verifycode",
        "name": "verifycode",
        "placeholder": u"请输入验证码"
    }))

    def save(self, commit=True):
        profile = super(UserRegisterFormStep2, self).save(commit=False)
        profile.is_active = True
        profile.save()
        return profile

    def clean_phoneNum(self):
        phone = self.cleaned_data.get("phoneNum")
        try:
            user = get_user_model().objects.get(profile__phoneNum=phone, profile__is_active=True)
            if user is not None:
                raise forms.ValidationError(self.error_messages["phone_already_exist"],
                                            code="phone_already_exist")
        except ObjectDoesNotExist:
            pass
        return phone

    def clean_code(self):
        code = self.cleaned_data.get("code")
        phone = self.cleaned_data.get("phoneNum")
        try:
            tz = timezone.get_current_timezone()
            time_threshold = tz.normalize(timezone.now()) - datetime.timedelta(minutes=5)
            record = VerifyCode.objects.get(phoneNum=phone,
                                            code=code,
                                            is_active=True,
                                            created_at__gt=time_threshold)
            record.is_active = False
            record.save()
        except (ObjectDoesNotExist, IndexError):
            print "the code posted is %s" % code
            raise forms.ValidationError(self.error_messages["code_mismatch"],
                                        code="code_mismatch")
        return code

    class Meta:
        model = UserProfile
        fields = ("phoneNum", "name", "birthDate", "gender", "avatar")
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
        "password_too_short": "密码太短，密码的长度至少在8位",
    }

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
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
        if len(password1) < 8:
            raise forms.ValidationError()

    def clean_phoneNum(self):
        phone = self.cleaned_data.get("phoneNum")
        try:
            user = get_user_model().objects.get(profile__phoneNum=phone)
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
            tz = timezone.get_current_timezone()
            time_threshold = tz.normalize(timezone.now()) - datetime.timedelta(minutes=5)
            record = VerifyCode.objects.get(phoneNum=phone,
                                            code=code,
                                            is_active=True,
                                            created_at__gt=time_threshold)
            record.is_active = False
            record.save()
        except ObjectDoesNotExist:
            raise forms.ValidationError(self.error_messages["code_mismatch"],
                                        code="code_mismatch")

    def save(self, commit=True):
        if self.user is not None:
            self.user.set_password(self.cleaned_data["password1"])
            self.user.save()
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