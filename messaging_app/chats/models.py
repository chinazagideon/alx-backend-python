# chats/models.py
"""
This file contains the models for the chats app
"""

from django.db import models
from user.models import User
from message.models import Message

# Create your models here.
class Chat(models.Model):
    message_id = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='message_id')
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()
