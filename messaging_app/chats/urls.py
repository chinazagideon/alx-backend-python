# chats/urls.py
"""
This file contains the urls for the chats app
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet, ChatViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"conversations", ConversationViewSet)
router.register(r"messages", MessageViewSet)
router.register(r"chats", ChatViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("api/", include(router.urls)),
]