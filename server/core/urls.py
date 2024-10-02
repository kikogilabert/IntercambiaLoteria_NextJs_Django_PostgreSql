# core/urls.py

from django.urls import path

from .views import (
    ComunidadAutonomaDetailView,
    ComunidadAutonomaListView,
    PaisDetailView,
    PaisListView,
    ProvinciaDetailView,
    ProvinciaFromPaisView,
    ProvinciaListView,
)

urlpatterns = [
    # Pais URLs
    path('paises/', PaisListView.as_view(), name='pais-list'),  # List all countries
    path('paises/<int:pk>/', PaisDetailView.as_view(), name='pais-detail'),  # Get a specific country by ID

    # ComunidadAutonoma URLs
    path('comunidades/', ComunidadAutonomaListView.as_view(), name='comunidad-list'),  # List all autonomous communities
    path('comunidades/<int:pk>/', ComunidadAutonomaDetailView.as_view(), name='comunidad-detail'),  # Get a specific autonomous community by ID

    # Provincia URLs
    path('provincias/', ProvinciaListView.as_view(), name='provincia-list'),  # List all provincias
    path('provincias/<int:pk>/', ProvinciaDetailView.as_view(), name='provincia-detail'),  # Get a specific provincias by ID

    # Get provincias by country (pais_id)
    path('paises/<int:pais_id>/provincias/', ProvinciaFromPaisView.as_view(), name='provincias-from-pais'),
]
