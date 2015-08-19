# coding=utf-8
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from .models import UserProfile


class PhoneNumAuthenticateBackend(object):
    """
    手机认证，将用户名中的内容是为手机进行认证
    """
    def authenticate(self, username=None, password=None):
        if username is None or password is None:
            # 如果用户名和密码有一个为空，那么返回None
            return None
        try:
            u = get_user_model().objects.get(profile__phoneNum=username)
            if u.check_password(password):
                return u
	    else:
		return None
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None
