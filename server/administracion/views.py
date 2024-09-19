from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AdministracionSerializer, UsuarioSerializer
from django.contrib.auth.hashers import make_password
from .models import Administracion, CustomUserManager, Usuario
from rest_framework import status

@api_view(['POST'])
def register_newAdmon(request):
    usuario_data = request.data['usuario']
    dni = usuario_data.get('dni')

    # Check if the DNI already exists in usuario
    if Usuario.objects.filter(dni=dni).exists():
        return Response({'error': 'Un usuario con el DNI: ' + dni + ', ya existe'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if any unique value already exists in Administracion
    elif Administracion.objects.filter(usuario__dni=dni, num_receptor = request.data['num_receptor']).exists():
        return Response({'error': 'Una administración con este DNI de usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        usuario_serializer = UsuarioSerializer(data=usuario_data)
        if usuario_serializer.is_valid():

            usuario = Usuario.objects.create_usuario(**usuario_serializer.validated_data)

            request.data['usuario'] = dni
            administracion_serializer = AdministracionSerializer(data=request.data)
            if administracion_serializer.is_valid():
                try:
                    administracion = Administracion.objects.create_administracion(**administracion_serializer.validated_data)

                    return Response({'success': 'Usuario registrado correctamente'}, status=status.HTTP_201_CREATED)
                except:
                    usuario.delete()
                    return Response(administracion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                usuario.delete()  # delete the usuario object if Administracion data is not valid
                return Response(administracion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)