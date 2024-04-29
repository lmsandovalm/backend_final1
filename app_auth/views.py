from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
    

class UserProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        # Obtener el perfil de usuario del usuario autenticado
        try:
            return self.request.user
        except UserProfile.DoesNotExist:
            # Si el perfil de usuario no existe, crear uno nuevo
            return UserProfile.objects.create(user=self.request.user)

    def get_queryset(self):
        # Devolver solo el perfil del usuario autenticado
        return UserProfile.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        # Obtener el perfil de usuario del usuario autenticado
        user_profile = self.get_object()
        serializer = self.get_serializer(user_profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Guardar el perfil actualizado
        return Response(serializer.data)
    
    
class PreguntaMovilViewSet(viewsets.ModelViewSet):
    queryset = PreguntaMovil.objects.all()
    serializer_class = PreguntaMovilSerializer

class RespuestaMovilViewSet(viewsets.ModelViewSet):
    queryset = RespuestaMovil.objects.all()
    serializer_class = RespuestaMovilSerializer

class TematicaViewSet(viewsets.ModelViewSet):
    queryset = Tematica.objects.all()
    serializer_class = TematicaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related('preguntas')
    
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer       
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related('tematicas')

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

