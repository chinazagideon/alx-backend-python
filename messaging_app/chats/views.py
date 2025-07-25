# chats/views.py
"""
This file contains the views for the chats app
"""

from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message, Chat
from oauth2_provider.contrib.rest_framework import OAuth2ScopedPermission
from rest_framework.response import Response

# filters for the models
from django.shortcuts import get_object_or_404

# serializers for the models
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    MessageSerializer,
    ChatSerializer,
)

# import permissions
from .permissions import isPerticipantOfConversation


def filter_by_user(queryset, user_id):
    """
    Filter the queryset by the user id
    """
    return queryset.filter(user_id=user_id)


def filter_by_conversation(queryset, conversation_id):
    """
    Filter the queryset by the conversation id
    """
    return queryset.filter(conversation=conversation_id)


def filter_by_message(queryset, message_id):
    """
    Filter the queryset by the message id
    """
    return queryset.filter(message=message_id)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user_id"]

    def get_queryset(self):
        """
        Filter the queryset by the user id
        """
        return filter_by_user(self.queryset, self.request.user.id)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or edited.
    """

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        OAuth2ScopedPermission,
        isPerticipantOfConversation,
    ]

    required_scopes = {
        "GET": ["read:messages"],
        "POST": ["manage:conversations"],
        "PUT": ["manage:conversations"],
        "PATCH": ["manage:conversations"],
        "DELETE": ["manage:conversations"],
    }

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["conversation_id"]

    def get_queryset(self):
        """
        Filter the queryset by the user's conversations
        """
        user = self.request.user
        if user.is_authenticated:
            return Conversation.objects.filter(participants=user).distinct()
        # return self.queryset.filter(participants=self.request.user)
        return Conversation.objects.none()


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        OAuth2ScopedPermission,
        isPerticipantOfConversation,
    ]

    required_scopes = {
        'GET': ['read:messages'],
        'POST': ['send:messages'],
        'PUT': ['send:messages', 'manage:conversations'],
        'PATCH': ['send:messages', 'manage:conversations'],
        'DELETE': ['manage:conversations']
    }

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["conversation", "status"]

    def perform_create(self, serializer):
        """
        use Current  User as message sender
        add as participant
        """

        conversation = serializer.validated_data.get('conversation')

        # check user is authenticated, general authentication
        if not self.request.user.is_authenticated:
            return Response({'detail': "Action not authorised, login and try again"}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        # check request user is a participant of conversation
        if not conversation.perticipants.filter(id=self.request.user.id).exists():
            return Response({'detail': 'You are not a participant of this conversation'}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        serializer.save(sender=self.request.user)

    def perform_update(self, serializer):
        """
        update conversation, conversation can only be updated by a perticipant
        """

        #retrieve message object
        message_obj = self.get_object() 

        #manaully check perticipants
        if not Message.objects.filter(id=message_obj.id, conversation__perticipants=self.request.user).exists():
            return Response({"detail": "Action denied due to you are not a participant of this conversation"}, 
                            status=status.HTTP_403_FORBIDDEN)        
        serializer.save()

    def perform_destroy(self, instance):
        """
        Handle delete conversation, verify request user is authorised 
        """
        if not Message.objects.filter(id=instance.id, conversation__participants=self.request.user).exists():
            return Response({'detail', "Action is Unauthorised"}, status=status.HTTP_403_FORBIDDEN)
        
        instance.delete()

    def get_queryset(self):
        """
        Filter the queryset by the user's conversations
        """
        user = self.request.user
        if  user.is_authenticated:
            user_conversation = Conversation.objects.filter(participants=user)
            return Message.objects.filter(conversation__in=user_conversation)
        return Message.objects.none()

class ChatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows chats to be viewed or edited.
    """

    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["message"]

    def get_queryset(self):
        """
        Filter the queryset by the user's messages
        """
        return self.queryset.filter(
            message__conversation__participants=self.request.user
        )
