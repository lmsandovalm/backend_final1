from django.db import models
from core import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers.user import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    ROLES = (
        ('admin', 'Admin'),
        ('aprendiz', 'Aprendiz'),
        ('instructor', 'Instructor'),
    )
    
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=254)
    password = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=20, choices=ROLES, default='aprendiz')
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email' 

##########################################################
################ Perfil Usuario ##########################
##########################################################

class UserProfile(models.Model):
    userprofile = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.userprofile if self.userprofile else 'UserProfile'

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(userprofile=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()



##########################################################
################ Preguntas y Respuestas ##################
##########################################################

class Pregunta(models.Model):
    texto_pregunta = models.CharField(max_length=200)

    def __str__(self):
        return self.texto_pregunta

class Respuesta(models.Model):
    estilos = (
        ("kinestesico","Kinestesico"),
        ("auditivo","Auditivo"),
        ("visual","Visual"),
    )
    id_pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    texto_respuesta = models.CharField(max_length=200)
    estilo = models.CharField(max_length=20, choices = estilos)

    def __str__(self):
        return self.texto_respuesta

class Resultado(models.Model):
    respuesta = models.ForeignKey(Respuesta, on_delete=models.CASCADE)
    usuario = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, default=1)
    fecha_resultado = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Resultado de {self.usuario}: {self.respuesta}"


##########################################################
################### Iscripcion Cursos ####################
##########################################################

class Curso(models.Model):
    nombre_curso = models.CharField(max_length=50)
    descripcion_curso = models.CharField(max_length=200)
    duracion_curso = models.IntegerField()

    def __str__(self):
        return self.nombre_curso


class Tematica(models.Model):
    id_curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    nombre_tematica = models.CharField(max_length=50)
    contenido_tematica = models.TextField()

    def __str__(self):
        return self.nombre_tematica


class Inscripcion(models.Model): 
    usuario = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, default=1)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField()

    def __str__(self):
        return f"Inscripción de {self.usuario} en curso {self.curso}"
    

##########################################################
###################### Actividades #######################
##########################################################

class ActividadIA(models.Model):
    id_tematica = models.ForeignKey(Tematica, on_delete=models.CASCADE)
    contenido_actividades = models.TextField()
    promt = models.TextField(null=True, blank=True)
    archivos = models.FileField(upload_to='actividades')

    def __str__(self):
        return self.id_tematica.nombre_tematica


class RespuestaAct(models.Model):
    id_actividadIA          = models.ForeignKey(ActividadIA, on_delete=models.CASCADE)
    id_perfil               = models.PositiveBigIntegerField(null=True, blank=True)  
    # id_perfil               = models.ForeignKey(Perfil, on_delete=models.CASCADE)  
    fecha_progreso          = models.DateField(auto_now=True)
    comentario              = models.TextField(null=True, blank=True)
    calificacion_progreso   = models.BooleanField(default=False)

    def __str__(self):
        return f"({self.id_actividadIA}): {self.calificacion_progreso}"



##########################################################
###################### ConsumoMovil #######################
##########################################################

class PreguntaMovil(models.Model):
    texto_pregunta = models.CharField(max_length=200)
    tematica = models.ForeignKey(Tematica, on_delete=models.CASCADE, related_name='preguntas')

    def __str__(self):
        return self.texto_pregunta

class RespuestaMovil(models.Model):
    pregunta = models.ForeignKey(PreguntaMovil, on_delete=models.CASCADE, related_name='respuestas')
    texto_respuesta = models.CharField(max_length=200)
    es_correcta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto_respuesta

