# coding=utf-8
"""这个文件是参考云片网给出的python参考代码写的"""

import httplib
import urllib

from django.http import HttpResponseRedirect

from django.http import Http404

# 服务地址
host = "yunpian.com"
# 端口号
port = 80
# 版本号
version = "v1"
# 通用短信接口的uri
sms_send_uri = "/" + version + "/sms/send.json"


def send_sms(apikey, text, mobile):
    """
    This utility function enables sending sms to the user given its phone number, api key
     and the message content.
    """
    params = urllib.urlencode({'apikey': apikey, 'text': text, 'mobile': mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def from_size_check_required(method):
    """
    This decorator get the 'start' and 'size' parameters from the GET dict
    """
    def wrapper(request, *args, **kwargs):
        try:
            start = int(request.GET.get("start", "0"))
        except ValueError:
            start = 0
        try:
            size = int(request.GET.get("size", "12"))
            if size < 0:
                size = 12
        except ValueError:
            start = 12
        return method(request, size=size, start=start,
                      *args, **kwargs)
    return wrapper


def profile_active_required(method):
    """
    This decorator is used to ensure that the users who login in from 3rd-party social media have provided essential
     Profile information. Note that this decorator must be placed after the login_required decorator
    """
    def wrapper(request, *args, **kwargs):
        user = request.user     # Get current user, and check its profile obj
        if user.is_authenticated() and not user.profile.is_active:
            return HttpResponseRedirect('/social/profile')
        return method(request, *args, **kwargs)

    return wrapper