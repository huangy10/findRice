from django.conf.urls import patterns, url

urlpatterns = patterns("Notification.views",
                       url("^$", "notification_center", name="notification_center"))