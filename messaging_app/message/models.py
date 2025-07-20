# message/models.py
"""
This file contains the models for the message app
"""
from django.db import models
from users.models import User
from chats.models import Chat

class MessageType(models.TextChoices):
    TEXT = 'text'
    IMAGE = 'image'
    AUDIO = 'audio' 

class MessageStatus(models.TextChoices):
    PENDING = 'pending'
    SENT = 'sent'
    DELIVERED = 'delivered'
    READ = 'read'
    FAILED = 'failed'

# Create your models here.
class Message(models.Model):
    """
    This model is used to store the messages sent by the user to the user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    message = models.CharField(max_length=255, null=False, blank=False)
    message_type = models.CharField(max_length=50, choices=MessageType.choices, null=True, blank=True)
    message_status = models.CharField(max_length=50, choices=MessageStatus.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message
