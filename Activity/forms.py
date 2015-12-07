# coding=utf-8
import copy
import logging

from django import forms
from django.utils import timezone

from .models import Activity, ActivityType
from .tasks import create_zipped_poster, create_share_thumbnail

logger = logging.getLogger(__name__)

class ActivityCreationForm(forms.ModelForm):

    error_messages = {
        "should_be_int": u"应当填写整数",
        "invalid_activity_type": u"活动类型无效",
        "wrong_prov_city": u"省份/城市数据格式错误",
        "start_time_error": u"活动不能在过去开始",
        "end_time_error": u"活动不能在开始之前结束",
        "last_length_error": u'持续时间太长'
    }
    day = forms.CharField(widget=forms.NumberInput(attrs={
        "class": "content time"
    }), required=False, initial=0)
    hour = forms.CharField(widget=forms.NumberInput(attrs={
        "class": "content time"
    }), required=False, initial=0)
    minute = forms.CharField(widget=forms.NumberInput(attrs={
        "class": "content time"
    }), required=False, initial=0)
    activity_type = forms.CharField(max_length=10, widget=forms.HiddenInput(attrs={
        "id": "action-type",
        "name": "action-type"
    }))
    poster = forms.ImageField(widget=forms.FileInput(attrs={
        "id": "poster",
        "name": "poster"
    }), required=False)
    present = forms.CharField(required=False)

    reward = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "content",
        "placeholder": u"请输入奖励金额"
    }), required=False, initial=0)

    def __init__(self, user=None, *args, **kwargs):
        super(ActivityCreationForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_activity_type(self):
        activity_type = self.cleaned_data.get("activity_type")
        try:
            num = int(activity_type)
            if num > ActivityType.objects.all().count():
                raise forms.ValidationError(self.error_messages["invalid_activity_type"],
                                            code="invalid_activity_type")
        except ValueError:
            raise forms.ValidationError(self.error_messages["invalid_activity_type"],
                                        code="invalid_activity_type")
        return activity_type

    def clean(self):
        start_time = self.cleaned_data['start_time']
        now = timezone.now()
        if start_time < now:
            self.add_error('start_time', self.error_messages['start_time_error'])
        end_time = self.cleaned_data['end_time']
        if end_time < start_time:
            self.add_error('end_time', self.error_messages['end_time_error'])

    def save(self, commit=True):
        obj = super(ActivityCreationForm, self).save(commit=False)
        # add the additional data to the act obj
        obj.last_length = int(self.cleaned_data["day"])*24*60 + int(self.cleaned_data["hour"])*60 + int(self.cleaned_data["minute"])
        logger.debug(u'上传的持续时间参数为{0}d{1}h{2}m, 计算得到的持续时间为{3}m'.format(
            self.cleaned_data['day'],
            self.cleaned_data['hour'],
            self.cleaned_data['minute'],
            obj.last_length
        ))
        type_no = int(self.cleaned_data.get("activity_type"))
        print self.cleaned_data
        obj.activity_type = list(ActivityType.objects.all())[type_no]
        if self.cleaned_data['poster'] is not None or not self.is_bound:
            obj.poster = self.cleaned_data['poster']

        # reward system
        if self.cleaned_data['present']:
            obj.reward_gift = True
            obj.reward_gift_detail = self.cleaned_data['present']
        else:
            obj.reward_gift = False

        if self.cleaned_data['reward']:
            obj.reward = self.cleaned_data['reward']
        else:
            obj.reward = 0

        obj.is_active = False   # 创建的表格在问卷生成以后才会有效
        obj.host = self.user

        if not obj.host.profile.identified and self.instance.pk is None:
            obj.identified = False
            obj.reward_for_share = 0
            obj.reward_for_share_and_finished_percentage = 0
            obj.reward_share_limit = 0
        else:
            obj.identified = True

        if commit:
            obj.save()
            # copy a new instance of the act object
            if obj.poster:
                new_obj = copy.deepcopy(obj)
                create_zipped_poster.delay(new_obj, force=True)
                create_share_thumbnail(new_obj, force=True)
        return obj

    class Meta:
        model = Activity
        fields = ("name", "host_name", "location", "description",
                  "start_time", "end_time", "max_attend", "city", "province")
        widgets = {
            "name": forms.TextInput(attrs={
                "id": "name",
                "class": "content",
                "placeholder": u"请输入活动名称"
            }),
            "host_name": forms.TextInput(attrs={
                "id": "host",
                "name": "host",
                "class": "content host",
                "readonly": "readonly"
            })
            ,
            "location": forms.TextInput(attrs={
                "id": "detail-addr",
                "class": "content",
                "placeholder": u"请输入活动地点"
            }),
            "start_time": forms.TextInput(attrs={
                "id": "startdate",
                "name": "startdate",
                "class": "form-control bday-i",
                "size": "16",
                "value": "",
                "readonly placeholder": u"请选择活动开始时间"
            }),
            "end_time": forms.TextInput(attrs={
                "id": "enddate",
                "name": "enddate",
                "class": "form-control bday-i",
                "size": "16",
                "value": "",
                "readonly placeholder": u"请选择活动结束时间"
            }),
            "max_attend": forms.NumberInput(attrs={
                "class": "content",
            }),
            "description": forms.Textarea(attrs={
                "id": "desc",
                "class": "",
                "placeholder": u"请输入活动简介"
            }),
        }
