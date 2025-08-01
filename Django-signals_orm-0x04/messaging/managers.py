from django.db import models

class UnreadMessagesManager(models.Manager):
    """
    Custom manager to filter unread messages for a specific user.
    """
    def unread_for_user(self, user):
        """
        Returns a queryset of unread messages for the specified user,
        optimizing the query to only retrieve necessary fields.
        """
        # We use .only() to fetch only the required fields, which is
        # a powerful optimization for large databases.
        return self.filter(
            receiver=user,
            read=False
        ).only('id', 'sender', 'conversation', 'timestamp', 'content')
