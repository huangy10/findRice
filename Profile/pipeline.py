# coding=utf-8
def set_profile_info(backends, user, response, *args, **kwargs):
    """这个是python-social-auth这个模块联合使用，第三方登陆时将数据记录到Profile表里面"""
    profile = user.profile
    if backends.name == "weixin":
        profile.name = response["nickname"]
        profile.avatar = response["headimgurl"]
        profile.gender = 2
    elif backends.name == "qq":
        profile.name = response["nickname"]
        profile.avatar = response["figureurl_qq_1"]
        profile.gender = response[""]
    elif backends.name == "weibo":
        profile.name = response["name"]
        profile.avatar = response["profile_image_url"]
        profile.gender = response["gender"]