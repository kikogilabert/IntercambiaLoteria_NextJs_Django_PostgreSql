from django_filters import rest_framework as filters

from intercambios.models import Solicitud


class SolicitudFilter(filters.FilterSet):
    """
    FilterSet for Solicitud model. Provides various filters for querying Solicitud objects.
    """

    id = filters.NumberFilter(field_name="id")
    tipo = filters.CharFilter(field_name="tipo", lookup_expr="exact")
    administracion = filters.CharFilter(field_name="administracion", lookup_expr="icontains")
    numero = filters.CharFilter(field_name="numero", lookup_expr="exact")
    numero_range = filters.RangeFilter(field_name="numero")
    num_series = filters.NumberFilter(field_name="num_series")
    sorteo = filters.NumberFilter(field_name="sorteo")
    condicion = filters.CharFilter(field_name="condicion", lookup_expr="exact")
    num_cond = filters.CharFilter(field_name="num_cond", lookup_expr="icontains")
    num_series_cond = filters.NumberFilter(field_name="num_series_cond")
    sorteo_cond = filters.NumberFilter(field_name="sorteo_cond")
    estado = filters.CharFilter(field_name="estado", lookup_expr="exact")
    created_at = filters.DateTimeFromToRangeFilter(field_name="created_at")
    updated_at = filters.DateTimeFromToRangeFilter(field_name="updated_at")

    class Meta:
        model = Solicitud
        fields = [
            "id",
            "tipo",
            "administracion",
            "numero",
            "num_series",
            "sorteo",
            "condicion",
            "num_cond",
            "num_series_cond",
            "sorteo_cond",
            "estado",
            "created_at",
            "updated_at",
        ]
        ordering = ["id", "created_at", "updated_at"]
