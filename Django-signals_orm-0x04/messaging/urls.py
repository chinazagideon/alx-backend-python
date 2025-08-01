# chats/urls.py
"""
This file contains the urls for the chats app
"""

from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_nested import routers as nested_routers
from .views import (
    UserViewSet,
    ConversationViewSet,
    MessageViewSet,
    MessageThreadViewSet,
    # test_logging,
)
from rest_framework.authtoken import views as auth_views

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"conversations", ConversationViewSet)
router.register(r"messages", MessageViewSet)
router.register(r"message-threads", MessageThreadViewSet)

# nested routers
conversation_router = nested_routers.NestedDefaultRouter(
    router, r"conversations", lookup="conversation"
)
conversation_router.register(
    r"messages", MessageViewSet, basename="conversation-messages"
)

# add the nested routers to the router
router.registry.extend(conversation_router.registry)

urlpatterns = [
    # api
    path("", include(router.urls)),
    # authentication
    path("auth/", auth_views.obtain_auth_token),
    path("profile/delete", views.delete_user, name="delete_user"),
    # test endpoint for logging
    # path("test-logging/", test_logging, name="test_logging"),
    path(
        "api/conversation/<uuid:conversation_id>/",
        views.get_conversation_json,
        name="get_conversation_json",
    ),
]
