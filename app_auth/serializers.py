from rest_framework import serializers
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        role = validated_data.get('role')
        group, _ = Group.objects.get_or_create(name=role)

        group.user_set.add(user)

        if role == 'admin':
            user.is_staff = True
            user.save()
            pass
        elif role == 'instructor':
            pass
        elif role == 'aprendiz':
            pass

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
                raise serializers.ValidationError('Invalid email or password.')

        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        data['user'] = user
        return data
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'
        
class TematicaSerializer(serializers.HyperlinkedModelSerializer): 
    class Meta:
        model = Tematica
        fields = '__all__'

class PreguntaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pregunta
        fields = '__all__'

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta 
        fields = '__all__'
        
        
class ResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultado
        fields = '__all__'
        
class InscripcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscripcion
        fields = '__all__'
        
        
class ActividadIASerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadIA 
        fields = '__all__'
        
class RespuestaActSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaAct
        fields = '__all__'

class RespuestaMovilSerializer(serializers.ModelSerializer):
    class Meta:
        model = RespuestaMovil
        fields = '__all__'

class PreguntaMovilSerializer(serializers.ModelSerializer):
    respuestas = RespuestaMovilSerializer(many=True, read_only=True)
    
    class Meta:
        model = PreguntaMovil
        fields = '__all__'