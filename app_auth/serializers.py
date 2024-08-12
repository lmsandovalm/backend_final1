from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = CustomUser
        fields = '__all__'

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if password != password_confirmation:
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden.'})

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        
        role = validated_data.get('role')

        if role == 'admin':
            user.is_staff = True
            user.save()
            admin_group = Group.objects.get(name='admin')
            user.groups.add(admin_group)
        elif role == 'usuarios':
            user_group = Group.objects.get(name='usuarios')
            user.groups.add(user_group)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)

            if not user:
                raise serializers.ValidationError('Email o contraseña invalidos.')

        else:
            raise serializers.ValidationError('Debe incluir "email" y "contraseña".')

        data['user'] = user
        return data
    
