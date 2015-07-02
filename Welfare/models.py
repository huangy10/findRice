from django.db import models

# Create your models here.


class WelfareGift(models.Model):
    address = models.CharField(max_length=255)