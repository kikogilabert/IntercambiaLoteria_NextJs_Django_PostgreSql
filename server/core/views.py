# core/views.py

from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from core.exceptions import InvalidStateTransition
from core.utils import ResponseStruct, get_error_response, get_success_response

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

        return ResponseStruct(message="List of countries fetched successfully", data=serializer.data).to_response()


class PaisDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        pais = get_object_or_404(Pais, pk=pk)
        serializer = PaisSerializer(pais)

        return ResponseStruct(
            message="List of countries with details fetched successfully", data=serializer.data
        ).to_response()


# ComunidadAutonoma views
class ComunidadAutonomaListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        comunidades = ComunidadAutonoma.objects.all()
        serializer = ComunidadAutonomaSimpleSerializer(comunidades, many=True)

        return ResponseStruct(message="List of Community fetched successfully", data=serializer.data).to_response()


class ComunidadAutonomaDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        comunidad = get_object_or_404(ComunidadAutonoma, pk=pk)
        serializer = ComunidadAutonomaSerializer(comunidad)

        return ResponseStruct(
            message="List of Community with details fetched successfully", data=serializer.data
        ).to_response()


# Provincia views
class ProvinciaListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        provincias = Provincia.objects.all()
        serializer = ProvinciaSimpleSerializer(provincias, many=True)

        return ResponseStruct(message="List of Province fetched successfully", data=serializer.data).to_response()


class ProvinciaDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        provincia = get_object_or_404(Provincia, pk=pk)
        serializer = ProvinciaSerializer(provincia)

        return ResponseStruct(
            message="List of Province with details fetched successfully", data=serializer.data
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
            message=f"Provinces for country {pais.nombre} fetched successfully", data=serializer.data
        ).to_response()


class ProvinciasRegister(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            # Verificar si existen los países con ID 1 y 2
            if not Pais.objects.filter(id=1).exists() and not Pais.objects.filter(id=2).exists():
                return get_error_response(message="No se encontraron los países especificados.", error_code=404)

            # Obtener las comunidades autónomas y provincias para los países especificados
            comunidades = ComunidadAutonoma.objects.filter(pais__id=1).values("id", "nombre_front")
            provincias = Provincia.objects.filter(pais__id__in=[1, 2]).values(
                "id", "nombre_front", "comunidad_autonoma", "pais"
            )

            # Crear un diccionario para almacenar las comunidades y sus provincias
            comunidad_dict = {comunidad["nombre_front"]: {"provincias": []} for comunidad in comunidades}

            # Asociar las provincias a sus respectivas comunidades autónomas
            for provincia in provincias:
                if provincia["pais"] == 1:  # Si la provincia pertenece a España
                    for comunidad in comunidades:
                        if comunidad["id"] == provincia["comunidad_autonoma"]:
                            comunidad_dict[comunidad["nombre_front"]]["provincias"].append(
                                {"id": provincia["id"], "nombre_front": provincia["nombre_front"]}
                            )
                elif provincia["pais"] == 2:  # Si la provincia pertenece a Andorra
                    if "Andorra" not in comunidad_dict:
                        comunidad_dict["Andorra"] = {"provincias": []}
                    comunidad_dict["Andorra"]["provincias"].append(
                        {"id": provincia["id"], "nombre_front": provincia["nombre_front"]}
                    )

            return get_success_response("Provincias extraidas correctamente.", data=comunidad_dict)

        except Exception as e:
            return get_error_response(
                message=f"Ha ocurrido un error al obtener las provincias: {str(e)}", error_code=500
            )


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
        nuevo_estado = request.data.get("nuevo_estado")
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
