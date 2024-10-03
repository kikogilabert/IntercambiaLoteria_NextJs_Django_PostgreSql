from django.urls import path

from .views import IntercambioAPIView, RespuestaAPIView, SolicitudAPIView

urlpatterns = [
    path("solicitud/", SolicitudAPIView.as_view(), name="solicitud"),
    path("respuesta/", RespuestaAPIView.as_view(), name="respuesta"),
    path("intercambio/", IntercambioAPIView.as_view(), name="intercambio"),

]
