# coding=utf-8
import hashlib

"""下面是一些功能函数"""


def active_required(method):
    """定义一个装饰器，来确保方法在执行前检查该类是否是active的，如果不是active的不执行方法"""
    def wrapper(self, *args, **kwargs):
        if not self.is_active:
            return
        else:
            return method(self, *args, **kwargs)
    return wrapper


def get_activity_session_representation(activity):
    rep = str(activity.id) + activity.name + "session_info"
    return hashlib.md5(rep.encode("utf-8")).hexdigest()
