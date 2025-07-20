# chats/urls.py
"""
This file contains the urls for the chats app
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet, ChatViewSet
from rest_framework.authtoken import views as auth_views
from drf_yasg import openapi

from drf_yasg.views import get_schema_view

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"conversations", ConversationViewSet)
router.register(r"messages", MessageViewSet)
router.register(r"chats", ChatViewSet)

# nested routers
conversation_router = nested_routers.NestedDefaultRouter(router, r"conversations", lookup="conversation")
conversation_router.register(r"messages", MessageViewSet, basename="conversation-messages")

# add the nested routers to the router
router.registry.extend(conversation_router.registry)


schema_view = get_schema_view(
    openapi.Info(
        title="Messaging API",
        default_version='v1',
        description="API for the Messaging App",
    ),
    public=True,
)
urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # api
    path('api/', include(router.urls)), # include the router urls Watch -> ["api"]
    # authentication
    # path('api-auth/', include(rest_framework_urls, namespace='rest_framework')),
    path('api/auth/token/', auth_views.obtain_auth_token),
    # nested api
    # path('api/conversations/<int:conversation_id>/', include(conversation_router.urls)),
    # swagger   
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # swagger ui
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), # redoc ui
]