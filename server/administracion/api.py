from rest_framework import viewsets, permissions
from .models import Administracion
from .serializers import AdministracionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

# Administracion CRUD Viewset
class AdministracionViewSet(viewsets.ModelViewSet):
    queryset = Administracion.objects.all() # aso es com fer un crud
    permissions_classes = [permissions.AllowAny] # qui pot accedir a esta ruta o consulta, en este cas -> allow all   # permission_classes = [permissions.IsAuthenticated] mes avant camvbiar aixo per a que nomes puga accedir si esta autenticat
    serializer_class = AdministracionSerializer # com es estructura la informacio



    @action(detail=False, methods=['get'])
    def getAdministrationsNames(self, request, pk=None):
        administrations = Administracion.objects.all()
        names = []
        for administration in administrations:
            names.append(administration.nombre)
        return Response(names)
    

    @action(detail=False, methods=['put'])
    def updateAdministrationName(self, request, pk=None):
        administration = Administracion.objects.get(id=request.data['id'])
        administration.nombre = request.data['new_name']
        administration.save()
        return Response('Name updated successfully', administration.nombre)