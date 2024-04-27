from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  *
from .models import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'userProlife', UserProfileViewSet, basename='userProlife')
router.register(r'cursos', CursoViewSet, basename='curso')
router.register(r'tematicas', TematicaViewSet, basename='tematica')
router.register(r'preguntas', PreguntaViewSet, basename='pregunta')
router.register(r'respuestas', RespuestaViewSet, basename='respuesta')
router.register(r'resultados', ResultadoViewSet, basename='resultado')
router.register(r'inscripciones', InscripcionViewSet, basename='inscripcion')
router.register(r'actividadesia', ActividadIAViewSet, basename='actividadia')
router.register(r'respuestasact', RespuestaActViewSet, basename='respuestaact')
router.register(r'preguntaMovil', PreguntaMovilViewSet, basename='preguntaMovil')
router.register(r'respuestaMovil', RespuestaMovilViewSet, basename='respuestaMovil')


urlpatterns = [
    path('profiles/', UserProfileViewSet.as_view(), name='userprofile'),
    path('register/', RegisterViewSet.as_view(), name='register'),
    path('login/', LoginViewSet.as_view(), name='login'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]