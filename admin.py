from django.contrib import admin
from .models import MailingRecipient, Message, Sending, MailingAttempt


@admin.register(MailingRecipient)
class MailingRecipientAdmin(admin.ModelAdmin):
    list_display = ()
    list_filter = ()
    search_fields = ()

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ()
    list_filter = ()
    search_fields = ()

@admin.register(Sending)
class SendingAdmin(admin.ModelAdmin):
    list_display = ()
    list_filter = ()
    search_fields = ()

@admin.register(MailingAttempt)
class MailingAttempt(admin.ModelAdmin):
    list_display = ()
    list_filter = ()
    search_fields = ()