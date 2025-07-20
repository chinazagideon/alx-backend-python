from django.db import models
from chats.models import Chat
# Create your models here.
class ReferenceType(models.TextChoices):
    CHAT = 'chat'
    USER = 'user'
    GROUP = 'group'

class Upload(models.Model):
    file = models.FileField(upload_to='uploads/')
    reference_id = models.ForeignKey(models.Model, on_delete=models.CASCADE, related_name='reference_id')
    reference_type = models.CharField(max_length=255, choices=ReferenceType.choices, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file.name