from django.urls import path

from .views import (ChangeRespuestaStateAPIView, ChangeSolicitudStateAPIView,
                    IntercambioAPIView, RespuestaAPIView, SolicitudAPIView)

urlpatterns = [
    path("solicitud/", SolicitudAPIView.as_view(), name="solicitud"),
    path("respuesta/", RespuestaAPIView.as_view(), name="respuesta"),
    path("intercambio/", IntercambioAPIView.as_view(), name="intercambio"),
    path('solicitud/<int:pk>/estado/', ChangeSolicitudStateAPIView.as_view(), name='solicitud_estado'),
    path('respuesta/<int:pk>/estado/', ChangeRespuestaStateAPIView.as_view(), name='respuesta_estado'),
]