from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models

TIPOS_PROPIETARIOS = [
    ('PF', 'Persona Fisica'),
    ('PJ', 'Persona Juridica')
]

class PropietarioManager(models.Manager):
    def create_propietario(self, **extra_fields):
        propietario = self.model(**extra_fields)
        propietario.save(using=self._db)
        return propietario

class Propietario(models.Model):
    dni = models.CharField(max_length=9, primary_key=True)
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=50)
    tipo_propietario = models.CharField(max_length=25, choices=TIPOS_PROPIETARIOS, default='PF')

    objects = PropietarioManager()

    def __str__(self):
        return self.dni

class CustomUserManager(BaseUserManager):
    def create_administracion(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(email, password, **extra_fields)
    

class Administracion(AbstractBaseUser):
    # ADMON ID FIELDS
    id_administracion = models.IntegerField(primary_key=True, unique=True)
    num_receptor= models.IntegerField(unique=True)
    nombre_comercial = models.CharField(max_length=50)
    # ADMON ADDRESS
    direccion = models.CharField(max_length=50)
    localidad = models.CharField(max_length=20)
    provincia = models.CharField(max_length=20)
    numero_admon = models.IntegerField()
    codigo_postal = models.IntegerField(null=True)

    # ADMON USER FIELDS
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=12)

    # ADITIONAL ADMON STATUS FIELDS
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'id_administracion'
    REQUIRED_FIELDS = [ 
                        'num_receptor',
                        'propietario', 
                        'nombre_comercial',
                        'direccion',
                        'localidad', 
                        'provincia', 
                        'numero_admon', 
                        'codigo_postal', 
                        'telefono', 
                        'email', 
                        'direccion'
                        ]
    
    def __str__(self):
        return self.id_administracion