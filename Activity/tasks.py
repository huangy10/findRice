# coding=utf-8
import StringIO
from PIL import Image

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile

from findRice.celery import app

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
            new_im = im.resize((int(W), tmp_h), resampe=Image.LANCZOS)
            new_im = new_im.crop((0, tmp_h/2-int(H)/2, int(W), tmp_h/2+int(H)/2))
        else:
            tmp_w = int(H / h * w)
            new_im = im.resize((tmp_w, int(H)), resampe=Image.LANCZOS)
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


@app.task()
def limit_poster_size(act):
    """
    限制海报的大小
    """
    pass
