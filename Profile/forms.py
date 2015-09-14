# coding=utf-8
import datetime
import logging

from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth import get_user_model
from django import forms
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models import UserProfile
from .models import VerifyCode
from .tasks import create_zipped_avatar


class UserRegisterFormStep1(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ("username", )
        widgets = {
            "username": forms.TextInput(attrs={
                "id": "username",
                "placeholder": u"请输入用户名"
            })
        }
        error_messages = {
            "username": {
                "unique": "该用户名已存在"
            }
        }

    error_messages = {
        'password_mismatch': "两次输入的密码不匹配",
        'username_too_short': "用户名太短，长度至少在8位",
        'password_too_short': "密码太短，密码的长度至少为4位",
        'username_already_exist': "该用户名已存在"
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
        if len(password1) < 4:
            raise forms.ValidationError(self.error_messages["password_too_short"],
                                        code="password_too_short")
        return password1

    def clean_password2(self):
        if 'password1' not in self.cleaned_data:
            return ''
        password2 = self.cleaned_data['password2']
        password1 = self.cleaned_data['password1']
        if not password1 == password2:
            raise forms.ValidationError(self.error_messages['password_mismatch'],
                                        code='password_mismatch')
        return password2

    def clean(self):
        try:
            user = get_user_model().objects.get(username=self.cleaned_data['username'],
                                                is_active=True,
                                                profile__is_active=True)
            if user:
                self.add_error('username', u'该用户名已被注册')
        except ObjectDoesNotExist:
            pass

    def save(self, commit=True):
        try:
            # Check if the given username is already in the User list, and its profile is not activated
            # If it does exist, then reuse it
            print 'username:' + self.cleaned_data['username']
            user = get_user_model().objects.get(username=self.cleaned_data['username'],
                                                profile__is_active=False,
                                                is_active=False)
            user.set_password(self.cleaned_data["password1"])
            logging.debug(u"User条目被复用: %s" % self.cleaned_data['username'])
        except ObjectDoesNotExist:
            logging.debug(u"创建用户条目，用户名为%s，密码为%s" % (
                self.cleaned_data['username'], self.cleaned_data['password1']))
            user = super(UserRegisterFormStep1, self).save(commit=False)
            # Note: 要手动设置密码
            user.set_password(self.cleaned_data['password1'])
        user.is_active = False
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
        profile.user.is_active = True
        if commit:
            profile.user.save()
            create_zipped_avatar.delay(profile)
        return profile

    def clean_phoneNum(self):
        phone = self.cleaned_data.get("phoneNum")
        try:
            user = get_user_model().objects.get(profile__phoneNum=phone,
                                                profile__is_active=True)
            if user is not None:
                raise forms.ValidationError(self.error_messages["phone_already_exist"],
                                            code="phone_already_exist")
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            pass
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
            record.is_active = False
            record.save()
        except (ObjectDoesNotExist, IndexError):
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
                "readonly placeholder": u"请选择出生日期",
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
