# chats/serializers.py
"""
This file contains the serializers for the chats app
"""

from rest_framework import serializers
# from .models import User, Conversation, Message, Chat
from django.conf import settings


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model
    """

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = "__all__"
        read_only_fields = ["user_id"]


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation objects.
    Handles nested messages and custom fields.
    """
    
    perticipants = serializers.PrimaryKeyRelatedField(
        queryset=settings.AUTH_USER_MODEL.objects.all(), 
        many=True
        help_text=_("Users participating in this conversation")
        )
    perticipants_count = serializers.SerializerMethodField()
    last_message_preview = serializers.SerializerMethodField()

    class Meta:
        model = settings.AUTH_CONVERSATION_MODEL
        fields = ["conversation_id", "perticipants", "perticipants_count", "last_message_preview"]
        read_only_fields = ["conversation_id"]

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model
    """

    class Meta:
        model = settings.AUTH_MESSAGE_MODEL
        fields = "__all__"
        read_only_fields = ["message_id", "conversation_id"]
        
    def validate_content(self, value):
        """
        Validate the content of the message
        """
        if not value.strip():
            raise serializers.ValidationError("Message content is required")
        if len(value) > 1000:
            raise serializers.ValidationError("Message content is too long")
        return value

class ChatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Chat model
    """

    class Meta:
        model = settings.AUTH_CHAT_MODEL
        fields = "__all__"
