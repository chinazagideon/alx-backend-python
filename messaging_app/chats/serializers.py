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
    # this field is not inherited from the AbstractConversation class
    perticipants = serializers.PrimaryKeyRelatedField(
        queryset=settings.AUTH_USER_MODEL.objects.all(), 
        many=True,
        help_text=("IDs of users participating in this conversation")
        )
    # this field is not inherited from the AbstractConversation class
    perticipants_count = serializers.SerializerMethodField()
    # this field is not inherited from the AbstractConversation class
    last_message_preview = serializers.SerializerMethodField()

    class Meta:
        model = settings.AUTH_CONVERSATION_MODEL
        fields = ["conversation_id", "perticipants", "perticipants_count", "last_message_preview"]
        read_only_fields = ["conversation_id"]

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model
    """
    # this field is not inherited from the AbstractMessage class
    conversation_id = serializers.PrimaryKeyRelatedField(
        queryset=settings.AUTH_CONVERSATION_MODEL.objects.all(),
        help_text=("The conversation this message belongs to")
    )
    # this field is not inherited from the AbstractMessage class
    message_body = serializers.CharField(
        max_length=1000,
        min_length=1,
        help_text=("The content of the message")
    )

    # this field is not inherited from the AbstractMessage class
    def validate_message_body(self, value):
        """
        Validate the content of the message
        """
        if not value.strip():
            raise serializers.ValidationError("Message content is required")
        if len(value) > 1000:
            raise serializers.ValidationError("Message content is too long")
        return value
    
    # this field is not inherited from the AbstractMessage class
    class Meta:
        model = settings.AUTH_MESSAGE_MODEL
        fields = "__all__"
        read_only_fields = ["message_id", "conversation_id"]

class ChatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Chat model
    """

    class Meta:
        model = settings.AUTH_CHAT_MODEL
        fields = "__all__"
