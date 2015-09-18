# coding=utf-8
import StringIO
from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from findRice.celery import app
from Notification.signals import send_notification


def cut_image_to_size(size, obj, attr='poster', suffix='zipped'):
    """This function cut the image marked by attr of obj"""
    W, H = [float(x) for x in size]
    with Image.open(getattr(obj, attr)) as im:
        w, h = im.size
        if w/W*H < h:
            tmp_h = int(W / w * h)
            new_im = im.resize((int(W), tmp_h), resample=Image.LANCZOS)
            new_im = new_im.crop((0, tmp_h/2-int(H)/2, int(W), tmp_h/2+int(H)/2))
        else:
            tmp_w = int(H / h * w)
            new_im = im.resize((tmp_w, int(H)), resample=Image.LANCZOS)
            new_im = new_im.crop((tmp_w/2-int(W)/2, 0, tmp_w/2+int(W)/2, int(H)))
        # im.thumbnail((300, 220))
        zipped_io = StringIO.StringIO()
        new_im.save(zipped_io, format='JPEG')
        setattr(obj, '{0}_{1}'.format(attr, suffix),
                InMemoryUploadedFile(file=zipped_io,
                                     field_name=None,
                                     name='foo.jpg',
                                     content_type='image/jpeg',
                                     size=zipped_io.len,
                                     charset=None))
        if callable(getattr(obj, 'save')):
            obj.save()
        zipped_io.close()


@app.task()
def create_zipped_poster(act, force=False):
    """
    为海报创建缩略图
    """
    if act.poster_zipped and not force:
        return

    with Image.open(act.poster) as im:
        W = 250.0 * 2
        H = 110.0 * 2
        w, h = im.size
        if w/W*H < h:
            tmp_h = int(W / w * h)
            new_im = im.resize((int(W), tmp_h), resample=Image.LANCZOS)
            new_im = new_im.crop((0, tmp_h/2-int(H)/2, int(W), tmp_h/2+int(H)/2))
        else:
            tmp_w = int(H / h * w)
            new_im = im.resize((tmp_w, int(H)), resample=Image.LANCZOS)
            new_im = new_im.crop((tmp_w/2-int(W)/2, 0, tmp_w/2+int(W)/2, int(H)))
        # im.thumbnail((300, 220))
        zipped_io = StringIO.StringIO()
        new_im.save(zipped_io, format='JPEG')
        act.poster_zipped = InMemoryUploadedFile(file=zipped_io,
                                                 field_name=None,
                                                 name='foo.jpg',
                                                 content_type='image/jpeg',
                                                 size=zipped_io.len,
                                                 charset=None)
        act.save()
        zipped_io.close()

    # at the end of this function ,create thumbnail for the act
    create_share_thumbnail(act)


@app.task()
def limit_poster_size(act):
    """
    限制海报的大小
    """
    pass


@app.task()
def send_del_notification_to_candidate(act):
    """ 向该活动的所有参与者发送该活动已经被删除的通知
    """
    from Activity.models import ApplicationThrough
    applicants = ApplicationThrough.objects.filter(is_active=True,
                                                   activity=act,
                                                   status__in=['applying', 'approved', 'ready'])
    for applicant in applicants:
        send_notification.send(sender=settings.AUTH_USER_MODEL,
                               notification_type='activity_notification',
                               notification_center=applicant.user.notification_center,
                               activity=act,
                               user=applicant.user,
                               activity_notification_type='activity_deleted')

    applicants.update(is_active=False)


@app.task()
def create_share_thumbnail(act):
    """ 生成适用于分享到朋友圈的缩略图，尺寸为300 * 300
    """
    if act.poster_thumbnail:
        return
    cut_image_to_size((184, 136), act, 'poster', 'thumbnail')
