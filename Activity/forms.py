# coding=utf-8
from django import forms

from .models import Activity, ActivityType


class ActivityCreationForm(forms.ModelForm):

    error_messages = {
        "should_be_int": u"应当填写整书",
        "invalid_activity_type": u"活动类型无效"
    }

    day = forms.NumberInput(attrs={
        "class": "content time"
    })
    hour = forms.NumberInput(attrs={
        "class": "content time"
    })
    minute = forms.NumberInput(attrs={
        "class": "content time"
    })
    activity_type = forms.HiddenInput(attrs={
        "id": "action_type",
        "name": "action-type"
    })

    def clean_day(self):
        day = self.cleaned_data.get("day")
        if isinstance(day, int):
            raise forms.ValidationError(self.error_messages["should_be_int"],
                                        code="should_be_int")
        return day

    def clean_hour(self):
        hour = self.cleaned_data.get("hour")
        if isinstance(hour, int):
            raise forms.ValidationError(self.error_messages["should_be_int"],
                                        code="should_be_int")
        return hour

    def clean_minute(self):
        minute = self.cleaned_data.get("minute")
        if isinstance(minute, int):
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
        obj = super(ActivityCreationForm, self).save(commit=True)
        obj.activity_type = ActivityType.objects.all()[int(self.cleaned_data.get("activity_type"))]
        obj.is_active = False   # 创建的表格在问卷生成以后才会有效
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
                "class": "content host",
            }),
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