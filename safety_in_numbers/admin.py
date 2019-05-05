from django.contrib import admin
from .models import SafteyInUser


class SafetyInUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(SafteyInUser, SafetyInUserAdmin)