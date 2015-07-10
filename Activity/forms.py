# coding=utf-8
from django import forms

from .models import Activity, ActivityType


class ActivityCreationForm(forms.ModelForm):

    error_messages = {
        "should_be_int": u"应当填写整书",
        "invalid_activity_type": u"活动类型无效"
    }
    day = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "content time"
    }), required=False, initial=0)
    hour = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "content time"
    }), required=False, initial=0)
    minute = forms.IntegerField(widget=forms.NumberInput(attrs={
        "class": "content time"
    }), required=False, initial=0)
    activity_type = forms.CharField(max_length=10, widget=forms.HiddenInput(attrs={
        "id": "action-type",
        "name": "action-type"
    }))

    def __init__(self, user=None, *args, **kwargs):
        super(ActivityCreationForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean_day(self):
        day = self.cleaned_data.get("day")
        if not isinstance(day, int):
            raise forms.ValidationError(self.error_messages["should_be_int"],
                                        code="should_be_int")
        return day

    def clean_hour(self):
        hour = self.cleaned_data.get("hour")
        if not isinstance(hour, int):
            raise forms.ValidationError(self.error_messages["should_be_int"],
                                        code="should_be_int")
        return hour

    def clean_minute(self):
        minute = self.cleaned_data.get("minute")
        if not isinstance(minute, int):
            raise forms.ValidationError(self.error_messages["should_be_int"],
                                        code="should_be_int")
        return minute

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

    def save(self, commit=True):
        obj = super(ActivityCreationForm, self).save(commit=False)
        obj.last_length = self.cleaned_data["day"]*24*60 + self.cleaned_data["hour"]*60 + self.cleaned_data["minute"]
        type_no = int(self.cleaned_data.get("activity_type"))
        print type_no
        if type_no == -1:
            obj.activity_type = None
        else:
            obj.activity_type = ActivityType.objects.all()[type_no]
        obj.is_active = False   # 创建的表格在问卷生成以后才会有效
        obj.host = self.user
        if commit:
            obj.save()
        return obj

    class Meta:
        model = Activity
        fields = ("name", "host_name", "location", "description",
                  "start_time", "end_time", "poster", "max_attend", "reward")
        widgets = {
            "name": forms.TextInput(attrs={
                "id": "name",
                "class": "content",
            }),
            "host_name": forms.TextInput(attrs={
                "id": "host",
                "name": "host",
                "class": "content host",
                "placeholder": "龚子仪"
            })
            ,
            "location": forms.TextInput(attrs={
                "id": "detail-addr",
                "class": "content",
                "place_holder": u"请输入活动地点"
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
            "reward": forms.NumberInput(attrs={
                "class": "content",
                "placeholder": u"请输入奖励金额"
            }),
            "description": forms.Textarea(attrs={
                "id": "desc",
                "class": ""
            }),
            "poster": forms.FileInput(attrs={
                "id": "poster",
                "name": "poster"
            })
        }