# coding=utf-8
"""这个文件是参考云片网给出的python参考代码写的"""

import httplib
import urllib

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