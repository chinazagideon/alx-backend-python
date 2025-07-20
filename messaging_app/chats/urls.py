# chats/urls.py
"""
This file contains the urls for the chats app
"""

from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet, ChatViewSet
from rest_framework.authtoken import views as auth_views

# Create a router and register our viewsets with it
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'conversations', ConversationViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'chats', ChatViewSet)

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    # Authentication
    path('api/auth/', auth_views.obtain_auth_token),
    # path('api/auth/', include('djoser.urls')),
]