from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


class SafteyInUser(AbstractUser):
    is_volunteer = models.BooleanField(null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)

    AbstractUser._meta.get_field('email').blank = False


class Transit(models.Model):
    safety_in_user = models.ForeignKey(SafteyInUser, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.today)
    time = models.TimeField(default=datetime.now)
    starting_address = models.CharField(max_length=50)
    ending_address = models.CharField(max_length=50)