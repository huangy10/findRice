from django.dispatch import Signal

share_record_signal = Signal(providing_args=["share_record"])
