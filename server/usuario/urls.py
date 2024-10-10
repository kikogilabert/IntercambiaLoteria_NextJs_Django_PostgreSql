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

from usuario.views import AdministracionView, ChangePasswordView, UsuarioLoginView, UsuarioRegisterView, UsuarioView

urlpatterns = [
    # Register a new user
    path("register/", UsuarioRegisterView.as_view(), name="user-register"),
    # Login user
    path("login/", UsuarioLoginView.as_view(), name="user-login"),
    # Profile update (PUT for full, PATCH for partial)
    path("profile/update/", UsuarioView.as_view(), name="profile-update"),
    # Deactivate profile (DELETE)
    path("profile/deactivate/", UsuarioView.as_view(), name="profile-deactivate"),
    # Get profile data (GET)
    path("profile/", UsuarioView.as_view(), name="profile-get"),
    # Change password (POST)
    path("profile/update/password/", ChangePasswordView.as_view(), name="profile-update-password"),
    # Profile update (PUT for full, PATCH for partial)
    path("admon/update/", AdministracionView.as_view(), name="admon-update"),
    # Get profile data (GET)
    path("admon/", AdministracionView.as_view(), name="admon-get"),
]
