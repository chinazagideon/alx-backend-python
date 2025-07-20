# chats/models.py
"""
This file contains the models for the chats app
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from message.models import Message
from uuid import uuid4
from django.utils.translation import gettext_lazy as _


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
    email = models.EmailField(
        _("email address"),
        max_length=255,
        null=False,
        blank=False,
        unique=True,
        help_text=_("User\'s email address")
    )
    password = models.CharField(
        _("password"),
        max_length=255,
        null=False,
        blank=False,
        help_text=_("User\'s password")
    )
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

