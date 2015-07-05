from django.conf.urls import url, patterns

urlpatterns = patterns("Activity.views",
                       url(r"^(?P<action_id>\d+)/applicant", "check_applicant_list", name="applicant"),
                       url(r"^(?P<action_id>\d+)/detail", "check_activity_detail", name="detail"),
                       url(r"^(?P<action_id>\d+)", "check_activity_detail"),
                       url(r"^new/edit/1", "create_new_activity_1", name="created1")
                       )