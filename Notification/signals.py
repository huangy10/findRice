from django.dispatch import Signal

send_notification = Signal(providing_args=["notification_type"])