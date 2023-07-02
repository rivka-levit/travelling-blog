from django.contrib import admin
from .models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'name', 'is_active']
    list_display_links = ['email', 'name']
    list_editable = ['is_active']
    list_filter = ['is_active']


admin.site.register(Subscriber, SubscriberAdmin)
