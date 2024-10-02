# core/views.py

from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from core.utils import ResponseStruct

from .models import ComunidadAutonoma, Pais, Provincia
from .serializers import (
    ComunidadAutonomaSerializer,
    ComunidadAutonomaSimpleSerializer,
    PaisSerializer,
    PaisSimpleSerializer,
    ProvinciaSerializer,
    ProvinciaSimpleSerializer,
)


# Pais views
class PaisListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        paises = Pais.objects.all()
        serializer = PaisSimpleSerializer(paises, many=True)

        return ResponseStruct(
            message="List of countries fetched successfully", data=serializer.data
        ).to_response()


class PaisDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        pais = get_object_or_404(Pais, pk=pk)
        serializer = PaisSerializer(pais)

        return ResponseStruct(
            message="List of countries with details fetched successfully",
            data=serializer.data,
        ).to_response()


# ComunidadAutonoma views
class ComunidadAutonomaListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        comunidades = ComunidadAutonoma.objects.all()
        serializer = ComunidadAutonomaSimpleSerializer(comunidades, many=True)

        return ResponseStruct(
            message="List of Community fetched successfully", data=serializer.data
        ).to_response()


class ComunidadAutonomaDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        comunidad = get_object_or_404(ComunidadAutonoma, pk=pk)
        serializer = ComunidadAutonomaSerializer(comunidad)

        return ResponseStruct(
            message="List of Community with details fetched successfully",
            data=serializer.data,
        ).to_response()


# Provincia views
class ProvinciaListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        provincias = Provincia.objects.all()
        serializer = ProvinciaSimpleSerializer(provincias, many=True)

        return ResponseStruct(
            message="List of Province fetched successfully", data=serializer.data
        ).to_response()


class ProvinciaDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        provincia = get_object_or_404(Provincia, pk=pk)
        serializer = ProvinciaSerializer(provincia)

        return ResponseStruct(
            message="List of Province with details fetched successfully",
            data=serializer.data,
        ).to_response()


class ProvinciaFromPaisView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pais_id):
        # Get the country by its id, or return a 404 if it doesn't exist
        pais = get_object_or_404(Pais, id=pais_id)

        # Filter provinces that belong to the given country
        provincias = Provincia.objects.filter(pais=pais)

        # Serialize the provinces
        serializer = ProvinciaSimpleSerializer(provincias, many=True)

        # Extract only the 'nombre' field from each province
        # provincias = Provincia.objects.filter(pais=pais).values_list('codigo', 'nombre')
        # list(provincias)

        # Return the response
        return ResponseStruct(
            message=f"Provinces for country {pais.nombre} fetched successfully",
            data=serializer.data,
        ).to_response()
