# chats/views.py
"""
This file contains the views for the chats app
"""

from email import message
from uuid import UUID
import django
from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message, MessageThread
from .permissions import TokenHasScope
from rest_framework.response import Response
# filters for the models
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.http import HttpResponse, HttpRequest, JsonResponse

from django.views.decorators.cache import cache_page # Import the cache_page decorator


from django.http import HttpResponse
from pprint import pprint
import logging

# Set up logger for token scope debugging
logger = logging.getLogger(__name__)

# serializers for the models
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    MessageSerializer,
    MessageThreadSerializer,
)

# import permissions
from .permissions import isParticipantOfConversation

def serialize_message(message):
    """
    Helper function to convert message object to a dictionary
    """
    return{ 
        'id': str(message.id),
        'receiver': message.receiver,
        'sender': message.sender.first_name+ ' '+ message.sender_last_name ,
        'message_body': message.message_body,
        'content':message.content,
        'timestamp': message.timestamp.isoformat(),
        'edited': message.edited,
        'parent_id': str(message.parent_message.id) if message.message_parent else None,
        'replies': []
    }


@login_required
@cache_page(60)
def inbox(request):
    """
    Displays a user's inbox, showing only unread messages.
    This view uses the custom UnreadMessagesManager.
    """
    # Use the custom manager 'unread' to get all unread messages for the user.
    # The .only() optimization is included within the manager's method.
    unread_messages = Message.unread.unread_for_user(request.user)

    # Note: `unread_messages` is a queryset, ready to be passed to a template
    # for rendering. The .only() call inside the manager ensures the
    # query is optimized.
    
    context = {
        'unread_messages': unread_messages,
    }

    # reender message
    return render(request, 'messaging/inbox.html', context)


def get_threaded_messages(conversation_id):
    """
    fetch threaded messages
    """

    try: 
        conversation = get_object_or_404(Conversation, id=UUID(conversation_id))
    except ValueError:
        return JsonResponse ({'error': 'Invalid conversation ID'}, status=400)

    messages = list(Message.objects.filter(conversation=conversation).select_related('parent_message', 'sender').order_by('timestamp'))
    message_dict = {str(msg.id): serialize_message(msg) for msg in messages}

    threaded_list = []
    for msg in messages:
        if msg.parent_message:
            #if parent message is in message object add as reply
            parent_id_str = str(msg.parent_message.id)
            if parent_id_str in message_dict:
                message_dict[parent_id_str]['replies'].append(message_dict[str(msg.id)])
            else:
                # If the parent is not in the list (e.g., it's a message from another
                # conversation, which should not happen, or a disconnected message),
                # we treat it as a top-level message.
                threaded_list.append(message_dict[str(msg.id)])
        else:

            # Add top-level messages to the main list
            threaded_list.append(message_dict[str(msg.id)])
    return threaded_list
    
@login_required
def get_unread_conversation(request, conversation_id):
    """
    Get unread User messages
    """
    unread_messages = Message.objects.for_user(request.user)
    unread_conversation = unread_messages.filter(conversation_id=conversation_id)

    return JsonResponse({'unread_conversation': unread_conversation}, status = 200)

@login_required
def get_conversation_json(request, conversation_id):
    """
    Get conversation's messages in threaded format
    """
    sender=request.user
    threaded_messages = get_threaded_messages(conversation_id)
    return JsonResponse({'messages': threaded_messages, 'user': sender}, status=200)

@login_required
def delete_user(request: HttpRequest) -> HttpResponse:
    """
    Delete the current user
    """
    if request.method == "POST":
        user = request.user
        user.delete()
        logout(request)
        messages.success(request, "Your account has been deleted")
        return redirect("home")


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
    permission_classes = [
        permissions.IsAuthenticated
        ]
    
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user_id"]

    def get_queryset(self):
        """
        Filter the queryset by the user id
        """
        print(self.request.user)
        # Convert data to a readable string
        return filter_by_user(self.queryset, self.request.user.user_id)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows conversations to be viewed or edited.
    """

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        TokenHasScope,
        isParticipantOfConversation,
    ]

    required_scopes = {
        "GET": ["read:messages"],
        "POST": ["manage:conversations"],
        "PUT": ["manage:conversations"],
        # "PATCH": ["manage:conversations"],
        # "DELETE": ["manage:conversations"],
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
        return Conversation.objects.none()


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows messages to be viewed or edited.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        TokenHasScope,
        isParticipantOfConversation,
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
        if not conversation.participants.filter(user_id=self.request.user.user_id).exists():
            return Response({'detail': 'You are not a participant of this conversation'}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        # logger.info(f"[{self.request.user.user_id}] Sending message to conversation: {conversation.conversation_id}")
        
        serializer.save(status="sent")

    def perform_update(self, serializer):
        """
        update conversation, conversation can only be updated by a perticipant
        """

        #retrieve message object
        message_obj = self.get_object() 

        #manually check participants
        if not Message.objects.filter(message_id=message_obj.message_id, conversation__participants=self.request.user).exists():
            return Response({"detail": "Action denied due to you are not a participant of this conversation"}, 
                            status=status.HTTP_403_FORBIDDEN)        
        serializer.save()

    def perform_destroy(self, instance):
        """
        Handle delete conversation, verify request user is authorised 
        """
        if not Message.objects.filter(message_id=instance.message_id, conversation__participants=self.request.user).exists():
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

class MessageThreadViewSet(viewsets.ModelViewSet):
    """
    API endpoint to returns message thread history.
    """

    queryset = MessageThread.objects.all()
    serializer_class = MessageThreadSerializer
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
