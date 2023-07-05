from django.contrib import admin
from .models import ContactMessage


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['sender_name', 'sender_email', 'processed']
    list_editable = ['processed']
    list_display_links = ['sender_name', 'sender_email']


admin.site.register(ContactMessage, ContactMessageAdmin)
