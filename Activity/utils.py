# coding=utf-8


"""下面是一些功能函数"""


def active_required(method):
    """定义一个装饰器，来确保方法在执行前检查该类是否是active的，如果不是active的不执行方法"""
    def wrapper(self, *args, **kwargs):
        if not self.is_active:
            return
        else:
            return method(self, *args, **kwargs)
    return wrapper
