from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from rest_framework import viewsets

from django.contrib.auth.models import Group

class RegisterViewSet(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        role = user.role
        if role == 'admin':
            user.is_staff = True
            user.save()
            admin_group = Group.objects.get(name='admin')
            user.groups.add(admin_group)
        elif role == 'usuarios':
            user_group = Group.objects.get(name='usuarios')
            user.groups.add(user_group)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginViewSet(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        return Response({
            'token': token,
            'user': RegisterSerializer(user).data
        }, status=status.HTTP_200_OK)
    

