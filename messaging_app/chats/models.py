# chats/models.py
"""
This file contains the models for the chats app
"""

from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractConversation, AbstractMessage
from message.models import Message
from uuid import uuid4
from chats.models import User # WATCHOUT: user defined in settings.py as Auth_User_Model might handle this differently
from django.utils.translation import gettext_lazy as _

class Message(AbstractMessage):
    """
    This model is used to store the message details
    """
    message_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)
class Conversation(AbstractConversation):
    """
    This model is used to store the conversation details
    """
    conversation_id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name='participants')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class User(AbstractUser):
    """
    This model is used to store the user details
    """
    # this fields are inherited from the AbstractUser class
    user_id = models.UUIDField(
        primary_key=True, 
        default=uuid4, 
        editable=False,
        help_text=_("User\'s unique identifier")
    )
    # this field is inherited from the AbstractUser class
    first_name = models.CharField(
        _("first name"),
        max_length=255,
        null=False,
        blank=False,
        help_text=_("User\'s first name")
    )

    last_name = models.CharField(
        _("last name"),
        max_length=255,
        null=False,
        blank=False,
        help_text=_("User\'s last name")
    )
    # this field is inherited from the AbstractUser class
    email = models.EmailField(
        _("email address"),
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        help_text=_("User\'s email address")
    )
    # this field is inherited from the AbstractUser class
    password = models.CharField(
        _("password"),
        max_length=255,
        null=False,
        blank=False,
        help_text=_("User\'s password")
    )
    # this field is not inherited from the AbstractUser class
    phone_number = models.CharField(
        _("phone number"),
        max_length=15, 
        null=False, 
        blank=False,
        unique=True,
        help_text=_("User\'s phone number, e.g., +12125551212")
    )

# Create your models here.
class Chat(models.Model):
    chat_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='message_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

