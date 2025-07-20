from django.db import models
from users.models import User
from enum import Enum

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
class Chat(models.Model):
    message = models.CharField(max_length=255, null=True, blank=True)
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    message_type = models.CharField(max_length=50, choices=MessageType.choices, null=True, blank=True)
    message_status = models.CharField(max_length=50, choices=MessageStatus.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()
