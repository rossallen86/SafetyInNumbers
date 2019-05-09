from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class SafetyInUser(AbstractUser):
    is_volunteer = models.BooleanField(default=False)
    telephone = models.CharField(max_length=15, blank=True, null=True)

    AbstractUser._meta.get_field('email').blank = False


class Transit(models.Model):
    date = models.DateField(default=datetime.today)
    time = models.TimeField(default=datetime.now)
    starting_address = models.CharField(max_length=50)
    ending_address = models.CharField(max_length=50)
    comments = models.CharField(max_length=140, null=True, blank=True)


class JoinedTransit(models.Model):
    class Meta:
        unique_together = ('safety_in_user', 'transit')

    safety_in_user = models.ForeignKey(SafetyInUser, on_delete=models.CASCADE)
    transit = models.ForeignKey(Transit, on_delete=models.CASCADE)