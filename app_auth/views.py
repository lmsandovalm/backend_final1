from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from rest_framework import viewsets

class RegisterViewSet(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        role = user.role
        if role == 'admin':
            pass
        elif role == 'instructor':
            pass
        elif role == 'aprendiz':
            pass

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
    
class UserProfileViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class TematicaViewSet(viewsets.ModelViewSet):
    queryset = Tematica.objects.all()
    serializer_class = TematicaSerializer
    
class PreguntaViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer

class RespuestaViewSet(viewsets.ModelViewSet): 
    queryset = Respuesta.objects.all()
    serializer_class = RespuestaSerializer

    
class ResultadoViewSet(viewsets.ModelViewSet):
    queryset = Resultado.objects.all()
    serializer_class = ResultadoSerializer

class InscripcionViewSet(viewsets.ModelViewSet):
    queryset = Inscripcion.objects.all()
    serializer_class = InscripcionSerializer

class ActividadIAViewSet(viewsets.ModelViewSet):
    queryset = ActividadIA.objects.all()
    serializer_class = ActividadIASerializer

class RespuestaActViewSet(viewsets.ModelViewSet):
    queryset = RespuestaAct.objects.all()
    serializer_class = RespuestaActSerializer

class PreguntaMovilViewSet(viewsets.ModelViewSet):
    queryset = PreguntaMovil.objects.all()
    serializer_class = PreguntaMovilSerializer

class RespuestaMovilViewSet(viewsets.ModelViewSet):
    queryset = RespuestaMovil.objects.all()
    serializer_class = RespuestaMovilSerializer