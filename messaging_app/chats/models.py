# chats/models.py
"""
This file contains the models for the chats app
"""

from django.db import models
from user.models import User
from message.models import Message
from uuid import uuid4

# Create your models here.
class Chat(models.Model):
    chat_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='message_id')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

