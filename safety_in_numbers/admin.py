from django.contrib import admin
from .models import SafetyInUser, Transit, JoinedTransit


class SafetyInUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(SafetyInUser, SafetyInUserAdmin)
admin.site.register(Transit, SafetyInUserAdmin)
admin.site.register(JoinedTransit, SafetyInUserAdmin)
