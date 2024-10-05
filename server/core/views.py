# core/views.py

from core.exceptions import InvalidStateTransition
from core.utils import ResponseStruct, get_error_response, get_success_response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from .models import ComunidadAutonoma, Pais, Provincia
from .serializers import (ComunidadAutonomaSerializer,
                          ComunidadAutonomaSimpleSerializer, PaisSerializer,
                          PaisSimpleSerializer, ProvinciaSerializer,
                          ProvinciaSimpleSerializer)


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


class ChangeStateAPIView(APIView):
    """
    Clase base para cambiar el estado de un objeto.
    Las subclases deben definir el método `get_model_class` y `get_valid_transitions`.
    """

    permission_classes = [IsAuthenticated]

    def get_model_class(self):
        """
        Método que debe ser sobreescrito para devolver el modelo que se va a utilizar
        (por ejemplo, Solicitud o Respuesta).
        """
        raise NotImplementedError("Subclases deben definir el método 'get_model_class'")

    def get_valid_transitions(self):
        """
        Método que debe ser sobreescrito para devolver los estados válidos para la transición.
        """
        raise NotImplementedError("Subclases deben definir el método 'get_valid_transitions'")
    
    def get(self, request, pk, *args, **kwargs):
        # Obtenemos el modelo y la instancia
        model_class = self.get_model_class()
        obj = get_object_or_404(model_class, pk=pk)

        # Esta respuesta es solo para mostrar el estado actual (no un cambio de estado)
        return get_success_response(f"Estado actual: {obj.estado}", data={"estado": obj.estado})

    def post(self, request, pk, *args, **kwargs):
        model_class = self.get_model_class()
        obj = get_object_or_404(model_class, pk=pk)

        valid_states = self.get_valid_transitions()
        nuevo_estado = request.data.get('nuevo_estado')
        if not nuevo_estado:
            return get_error_response("No se proporcionó un estado nuevo.", error_code=400)
        
        if nuevo_estado not in valid_states:
            return get_error_response("Nuevo estado no es correcto.", error_code=400)

        try:
            # Llamamos a `change_state()` en el modelo (solo realiza la lógica de negocio)
            mensaje = obj.change_state(nuevo_estado, valid_states)
            # Devolvemos una respuesta de éxito (generada en la vista)
            return get_success_response(mensaje, data={"id": obj.id, "nuevo_estado": nuevo_estado})

        except InvalidStateTransition as e:
            # Capturamos el error y devolvemos una respuesta de error (generada en la vista)
            return get_error_response(str(e), data={"id": obj.id, "estado_actual": obj.estado}, error_code=400)
