import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from server.django_backend.django_backend import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Administracion(AbstractBaseUser):
    id_receptor = models.IntegerField(unique=True)
    nombre_comercial = models.CharField(max_length=50)
    direccion = models.CharField(max_length=50)
    provincia = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=5)
    numero_administacion = models.CharField(max_length=2)
    id_propietario = models.IntegerField(unique=True)
    telefono = models.CharField(max_length=12)
    contraseña = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 
                    'id_receptor',
                    'nombre_comercial', 
                    'direccion', 
                    'provincia', 
                    'codigo_postal', 
                    'numero_administacion', 
                    'telefono', 
                    'contraseña'
                    ]

    def __str__(self):
        return self.email
    
    # Falta instalar la libreria jwt #

    # @property
    # def token(self):
    #     return self.generate_token_jwt(1080)
    
    # @property
    # def ref_token(self):
    #     return self.generate_token_jwt(10800)

    # def generate_token_jwt(self, token_time):
    #     dt = datetime.now() + datetime.timedelta(seconds=token_time)

    #     token = jwt.encode({'username': self.username, 'exp': dt.utcfromtimestamp(dt.timestamp())
    #     }, settings.SECRET_KEY, algorithm='HS256')

    #     return token.decode('utf-8')
