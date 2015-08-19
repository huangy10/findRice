# coding=utf-8
def set_profile_info(backend, user, response, *args, **kwargs):
    """这个是python-social-auth这个模块联合使用，第三方登陆时将数据记录到Profile表里面"""
    profile = user.profile
    if backend.name == "weixin":
        profile.name = response["nickname"]
        profile.avatar_social = response["headimgurl"]
        profile.gender = 2
    elif backend.name == "qq":
        profile.name = response["nickname"]
        profile.avatar_social = response["figureurl_qq_1"]
        profile.gender = response["gender"]
    elif backend.name == "weibo":
        profile.name = response["name"]
        profile.avatar_social = response["profile_image_url"]
        profile.gender = response["gender"]
    profile.save()