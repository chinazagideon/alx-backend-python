from django.contrib import admin
from .models import Notification, Message, Conversation
# Register your models here.
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    #customize admin conversation view
    list_display = ('created_at', 'updated_at', 'get_participant_count')

    #filter list by created date
    list_filter = ('created_at',)

    #add a search bar for participants by username
    search_fields = ('participants__username',)

    def get_participant_count (self, obj):
        return obj.participants.count()
    get_participant_count.short_description = 'Participants' #column header


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'conversation', 'sender', 'receiver', 'message_body', 'content_preview')

    #declare table filters
    list_filter = ('conversation', 'sender', 'receiver')

    #searchable fields
    search_fields=("sender__username", "receiver__username", 'message_body', )

    #add editable column 
    list_editable  = ('message_body',)

    def content_preview(self, obj):
        #display a truncated version of the message body
        return obj.message_body[:50] + '...' if len(obj.message_body) > 50 else obj.message_body
    content_preview.short_description = "message preview"

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", 'message', "is_read", "created_at")

    list_filter = ("user", "is_read", "created_at", )

    search_fields = ("user__first_name", "message__message_body",)

    list_editable = ('is_read', )








