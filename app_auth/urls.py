from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  *
from . import  views
from .models import *
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('register/', RegisterViewSet.as_view(), name='register'),
    path('login/', LoginViewSet.as_view(), name='login'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]