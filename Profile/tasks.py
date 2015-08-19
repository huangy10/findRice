# coding=utf-8
import StringIO
from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from findRice.celery import app

@app.task()
def create_zipped_avatar(profile, force=False):
    """
    为头像创建缩略图
    """
    if profile.avatar_zipped and not force:
        return
    if not profile.avatar:
        return

    with Image.open(profile.avatar) as im:
        im.thumbnail((128, 128))
        zipped_io = StringIO.StringIO()
        im.save(zipped_io, format='JPEG')
        profile.avatar_zipped = InMemoryUploadedFile(file=zipped_io,
                                                     field_name=None,
                                                     name='foo.jpg',
                                                     content_type='image/jpeg',
                                                     size=zipped_io.len,
                                                     charset=None)
        profile.save()
        zipped_io.close()


@app.task()
def limit_avatar_size(profile):
    """
    限制头像的大小
    """
    pass