from django.contrib import admin
from .models import SafetyInUser


class SafetyInUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(SafetyInUser, SafetyInUserAdmin)