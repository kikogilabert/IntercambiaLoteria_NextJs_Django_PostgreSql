from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AdministracionSerializer, PropietarioSerializer
from django.contrib.auth.hashers import make_password
from .models import Administracion, CustomUserManager, Propietario
from rest_framework import status

@api_view(['POST'])
def register_newAdmon(request):
    propietario_data = request.data['propietario']
    dni = propietario_data.get('dni')

    # Check if the DNI already exists in Propietario
    if Propietario.objects.filter(dni=dni).exists():
        return Response({'error': 'Un propietario con el DNI: ' + dni + ', ya existe'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if any unique value already exists in Administracion
    elif Administracion.objects.filter(propietario__dni=dni, num_receptor = request.data['num_receptor']).exists():
        return Response({'error': 'Una administración con este DNI de propietario ya existe'}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        propietario_serializer = PropietarioSerializer(data=propietario_data)
        if propietario_serializer.is_valid():

            propietario = Propietario.objects.create_propietario(**propietario_serializer.validated_data)

            request.data['propietario'] = dni
            administracion_serializer = AdministracionSerializer(data=request.data)
            if administracion_serializer.is_valid():
                try:
                    administracion = Administracion.objects.create_administracion(**administracion_serializer.validated_data)

                    return Response({'success': 'Usuario registrado correctamente'}, status=status.HTTP_201_CREATED)
                except:
                    propietario.delete()
                    return Response(administracion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                propietario.delete()  # delete the Propietario object if Administracion data is not valid
                return Response(administracion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)