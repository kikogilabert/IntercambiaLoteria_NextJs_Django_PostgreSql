from django.urls import path

from .views import (IntercambioAPIView, SolicitudAPIView,
                    SolicitudRespuestaAPIView)

urlpatterns = [
    path("solicitud/", SolicitudAPIView.as_view(), name="solicitud"),
    path("respuesta/", SolicitudRespuestaAPIView.as_view(), name="respuesta"),
    path("intercambio/", IntercambioAPIView.as_view(), name="intercambio"),

]
