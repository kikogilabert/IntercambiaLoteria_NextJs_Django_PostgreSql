"""
URL configuration for django_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from .views import ProfileView, UsuarioLoginView, UsuarioRegisterView, UsuarioUpdateView

urlpatterns = [
    # Register a new user
    path("register/", UsuarioRegisterView.as_view(), name="user-register"),
    # Login user
    path("login/", UsuarioLoginView.as_view(), name="user-login"),
    # Profile update (PUT for full, PATCH for partial)
    path("profile/update/", UsuarioUpdateView.as_view(), name="profile-update"),
    # Deactivate profile (DELETE)
    path("profile/deactivate/", UsuarioUpdateView.as_view(), name="profile-deactivate"),
    # Get profile data
    path('profile/', ProfileView.as_view(), name='profile'),
]
