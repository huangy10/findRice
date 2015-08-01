from django.conf.urls import url, patterns

urlpatterns = patterns("Activity.views",
                       url(r"^(?P<action_id>\d+)/applicant$", "check_applicant_list", name="applicant"),
                       url(r"^(?P<action_id>\d+)/detail$", "check_activity_detail", name="detail"),
                       url(r"^(?P<action_id>\d+)$", "check_activity_detail", name="activity_detail"),
                       url(r"^new/create/1$", "create_new_activity_1", name="create1"),
                       url(r"^(?P<action_id>\d+)/create/1$", "edit_new_activity_1", name="create_edit1"),
                       url(r"^(?P<action_id>\d+)/create/2$", "create_new_activity_2", name="create2"),
                       url(r"^(?P<action_id>\d+)/publish$", "publish_an_activity", name="create3"),
                       url(r"^(?P<action_id>\d+)/apply$", "apply_an_activity", name="apply_an_activity"),
                       url(r"^(?P<action_id>\d+)/unapply$", "unapply_an_activity", name="unapply_an_activity"),
                       url(r"^(?P<action_id>\d+)/edit/1", "edit_activity_1", name="edit1"),
                       url(r"^(?P<action_id>\d+)/edit/2", "edit_activity_2", name="edit2"),
                       url(r"^(?P<action_id>\d+)/save", "save_an_activity", name="edit3"),

                       url(r"(?P<action_id>\d+)/sharelink", "get_share_link", name="share_link"),
                       url(r"^like$", "like_an_activity", name="like"),
                       url(r"^(?P<action_id>\d+)/delete$", "del_an_activity", name="delete"),
                       url(r"^(?P<action_id>\d+)/duplicate", "copy_an_activity", name="duplicate"),
                       url(r"^(?P<action_id>\d+)/stop", "stop_accepting_apply", name="stop"),
                       url(r"^(?P<action_id>\d+)/start", "restart_accepting_apply", name="restart"),
                       )