
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models import Notification, Message, MessageHistory, Conversation
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

@receiver(post_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Signal receiver to log message edit
    """
    if instance.pk:
        try:
            
            old_instance = Message.objects.get(pk=instance.pk)
            #check if the content has changed
            if old_instance.content != instance.content:
                MessageHistory.objects.create(
                    message=instance,
                    old_content=old_instance.content
                    )
                #update content edited to true
                instance.edited = True
                instance.edited_by = instance.sender
                instance.save()
        except Message.DoesNotExist:
            logging.info(f"warning: message {instance.message_id} does not exist")

@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Signal receiver to clean up all the user data after a User is deleted
    """
    try:
        #delete user messages sender instance 
        Message.objects.filter(sender=instance).delete()

        #delete user messages receiver instance
        Message.objects.filter(receiver=instance).delete()

        #delete notifications
        Notification.objects.filter(user=instance).delete()

    except Exception as e:
        logging.info(f"error {e}")




