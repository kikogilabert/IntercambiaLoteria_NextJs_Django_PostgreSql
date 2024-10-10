from django.utils.functional import lazy


def get_provincias_choices():
    from core.models import Provincia

    # Crear una lista de tuplas con el formato [(id, nombre_front)] incluyendo andorra.
    return [
        (provincia["id"], provincia["nombre_front"])
        for provincia in Provincia.objects.filter(pais__id__in=[1, 2]).values("id", "nombre_front")
    ]


# Usar lazy para evaluar la consulta solo cuando sea necesario
PROVINCIAS_CHOICES = lazy(get_provincias_choices, list)()
