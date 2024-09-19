from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import BoletoSerializer
from .models import Boleto
from administracion.models import Administracion


@api_view(['GET'])
def getAllBoletos(request):
    boletos = Boleto.objects.all()
    boletos_serializer = BoletoSerializer(boletos, many=True)
    return Response(boletos_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def getBoletosByNumber(request):
    boletos = Boleto.objects.filter(numero_boleto = request.data['numero_boleto'])
    boletos_serializer = BoletoSerializer(boletos, many=True)
    return Response(boletos_serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_boleto(request):
        
        if Administracion.objects.filter(id_administracion = request.data['administracion']).exists():
            print('administracion encontrada')
            boleto_serializer = BoletoSerializer(data=request.data)
            if boleto_serializer.is_valid():
                print('boleto objeto con formato correcto')
                
                Boleto.objects.create(numero_boleto = boleto_serializer.validated_data['numero_boleto'],
                                        series_boleto = boleto_serializer.validated_data['series_boleto'],
                                        num_series_disponibles = boleto_serializer.validated_data['num_series_disponibles'],    
                                        administracion = boleto_serializer.validated_data['administracion'])
                
                return Response({'Boleto creado': boleto_serializer.data}, status=status.HTTP_201_CREATED)
            else: 
                return Response({'error': 'Boleto con formato incorrecto'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Administracion no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def updateBoleto(request, id): 
    old_boleto = Boleto.objects.filter(id = id)
    if old_boleto.exists():
        boleto_serializer = BoletoSerializer(data=request.data)
        if boleto_serializer.is_valid():
            print('serializer correcto')
            if Administracion.objects.filter(id_administracion = boleto_serializer.validated_data['administracion']).exists():
                print('administracion encontrada')
                # old_boleto.update(numero_boleto = boleto_serializer.validated_data['numero_boleto'],
                #                     series_boleto = boleto_serializer.validated_data['series_boleto'],
                #                     num_series_disponibles = boleto_serializer.validated_data['num_series_disponibles'],    
                #                     administracion = boleto_serializer.validated_data['administracion'])
                # return Response({'Boleto actualizado': boleto_serializer.data}, status=status.HTTP_200_OK)
            else: 
                return Response({'error': 'Nueva Administracion no encontrada', "value": boleto_serializer.data['administracion']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Boleto con formato incorrecto'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Boleto no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteBoletoByID(request, id):
    boletos = Boleto.objects.filter(id = id)
    boletos.delete()
    return Response({'error': 'Boleto borrado correctamente'}, status=status.HTTP_200_OK)