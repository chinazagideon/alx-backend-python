
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification, Message
from django.conf import settings

import logging

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    """
    Signal receiver to create new notification when a new Message instance is saved.
    """
    if created: #only create notification after is mesaage created
        if instance.receiver: 
            #notification can't be sent to message sender
            if instance.sender != instance.receiver:

                try :
                    #create notification
                    Notification.objects.create(
                        user=instance.receiver,
                        message=instance,
                        is_read=False
                    )
                except Exception as e:
                    logging.info(f"an error occurred while creating notification {instance.message_id}{e}")
            else:
                logging.info(f"skip notification to sender {instance.message_id}")

        else:
            logging.info(f"skip notification for message no receiver provided")

