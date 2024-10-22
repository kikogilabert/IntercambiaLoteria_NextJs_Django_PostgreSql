from django.urls import path

from intercambios.views import (
                    ChangeRespuestaStateAPIView,
                    ChangeSolicitudStateAPIView,
                    IntercambioAPIView,
                    RespuestaAPIView,
                    SolicitudAPIView,
                    SolicitudFilterView,
)

urlpatterns = [
    path("solicitud/", SolicitudAPIView.as_view(), name="solicitud"),
    path("solicitud/<int:pk>/", SolicitudAPIView.as_view(), name="get_solicitud"),
    path("solicitud/<int:pk>/estado/", ChangeSolicitudStateAPIView.as_view(), name="solicitud_estado"),
    # Ruta para el filtrado (GET) -> GET /api/intercambios/solicitud/filter/?tipo=0&estado=ABIERTA&sorteo=2
    path("solicitud/filter/", SolicitudFilterView.as_view(), name="solicitud_filter"),

    path("respuesta/", RespuestaAPIView.as_view(), name="respuesta"),
    path("respuesta/<int:pk>/", RespuestaAPIView.as_view(), name="get_respuesta"),
    path("respuesta/<int:pk>/estado/", ChangeRespuestaStateAPIView.as_view(), name="respuesta_estado"),

    path("intercambio/", IntercambioAPIView.as_view(), name="intercambio"),
    path("intercambio/<int:pk>/", IntercambioAPIView.as_view(), name="get_intercambio"),
]
