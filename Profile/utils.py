# coding=utf-8
"""这个文件是参考云片网给出的python参考代码写的"""

import httplib
import urllib

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
    params = urllib.urlencode({'apikey': apikey, 'text': text, 'mobile': mobile})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection(host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    return response_str


def from_size_check_required(method):
    def wrapper(request, *args, **kwargs):
        try:
            start = int(request.GET.get("from", "0"))
        except ValueError:
            raise Http404
        try:
            size = int(request.GET.get("size", "12"))
            if size < 0:
                raise Http404
        except ValueError:
            raise Http404
        return method(request, size=size, start=start,
                      *args, **kwargs)
    return wrapper