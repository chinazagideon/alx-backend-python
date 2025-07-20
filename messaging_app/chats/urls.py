# chats/urls.py
"""
This file contains the urls for the chats app
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet, ChatViewSet
from rest_framework.authtoken import views as auth_views
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"conversations", ConversationViewSet)
router.register(r"messages", MessageViewSet)
router.register(r"chats", ChatViewSet)

router_arrays = [
    'users', 'conversations', 'messages', 'chats', 
    "api-auth/", "auth/token/", "swagger/", "redoc/",
    "api/", "api/<str:router_array>/", "api/<str:router_array>/<int:pk>/", 
    "api/<str:router_array>/<int:pk>/<str:router_array_2>/",
      "api/<str:router_array>/<int:pk>/<str:router_array_2>/<int:pk_2>/", "api/<str:router_array>/<int:pk>/<str:router_array_2>/<int:pk_2>/<str:router_array_3>/", "api/<str:router_array>/<int:pk>/<str:router_array_2>/<int:pk_2>/<str:router_array_3>/<int:pk_3>/", "api/<str:router_array>/<int:pk>/<str:router_array_2>/<int:pk_2>/<str:router_array_3>/<int:pk_3>/<str:router_array_4>/", "api/<str:router_array>/<int:pk>/<str:router_array_2>/<int:pk_2>/<str:router_array_3>/<int:pk_3>/<str:router_array_4>/<int:pk_4>/"]

schema_view = get_schema_view(
    openapi.Info(
        title="Messaging API",
        default_version='v1',
        description="API for the Messaging App",
    ),
    public=True,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)), # include the router urls Watch -> ["api"]
    path('api/<str:router_array>/', include(router.urls)), # include the router urls Watch -> ["api/users"]
    path('api/<str:router_array>/<int:pk>/', include(router.urls)), # include the router urls Watch -> ["api/users/1"]
    path('api/<str:router_array>/<int:pk>/<str:router_array_2>/', include(router.urls)), # include the router urls Watch -> ["api/users/1/messages"]
    path('api/<str:router_array>/<int:pk>/<str:router_array_2>/<int:pk_2>/', include(router.urls)), # include the router urls Watch -> ["api/users/1/messages/1"]
    path('api/<str:router_array>/<int:pk>/<str:router_array_2>/<int:pk_2>/<str:router_array_3>/', include(router.urls)), # include the router urls Watch -> ["api/users/1/messages/1/chats"]
    path('api/<str:router_array>/<int:pk>/<str:router_array_2>/<int:pk_2>/<str:router_array_3>/<int:pk_3>/', include(router.urls)), # include the router urls Watch -> ["api/users/1/messages/1/chats/1"]
    path('api/<str:router_array>/<int:pk>/<str:router_array_2>/<int:pk_2>/<str:router_array_3>/<int:pk_3>/<str:router_array_4>/', include(router.urls)), # include the router urls Watch -> ["api/users/1/messages/1/chats/1/messages"]
    path('api/<str:router_array>/<int:pk>/<str:router_array_2>/<int:pk_2>/<str:router_array_3>/<int:pk_3>/<str:router_array_4>/<int:pk_4>/', include(router.urls)), # include the router urls Watch -> ["api/users/1/messages/1/chats/1/messages/1"]
    # authentication
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/token/', auth_views.obtain_auth_token),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), # swagger ui
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), # redoc ui
]