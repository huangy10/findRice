from django.conf.urls import url, patterns

urlpatterns = patterns("Activity.views",
                       url(r"^(?P<action_id>\d+)/applicant$", "check_applicant_list", name="applicant"),
                       url(r"^(?P<action_id>\d+)/detail$", "check_activity_detail", name="detail"),
                       url(r"^(?P<action_id>\d+)$", "check_activity_detail", name="activity_detail"),
                       url(r"^new/edit/1$", "create_new_activity_1", name="create1"),
                       url(r"^(?P<action_id>\d+)/edit/2$", "create_new_activity_2", name="create2"),
                       url(r"^(?P<action_id>\d+)/publish$", "create_new_activity_3", name="create3"),
                       url(r"^(?P<action_id>\d+)/apply$", "apply_an_activity", name="apply_an_activity"),

                       url(r"(?P<action_id>\d+)/sharelink", "get_share_link", name="share_link"),
                       url(r"^like$", "like_an_activity", name="like"),
                       url(r"^(?P<action_id>\d+)/delete$", "del_an_activity", name="delete")
                       )