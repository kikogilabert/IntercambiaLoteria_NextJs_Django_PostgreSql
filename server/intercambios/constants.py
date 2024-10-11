from enum import IntEnum


class TiposSolicitud(IntEnum):
    OFERTA = 0
    BUSQUEDA = 1

class TiposCondicion(IntEnum):
    CESION = 0
    INDIFERENTE = 1
    EXPLICITA = 2

# Example usage
TIPOS_SOLICITUD = [(tipo.value, tipo.name) for tipo in TiposSolicitud]
TIPOS_CONDICION = [(condicion.value, condicion.name) for condicion in TiposCondicion]


# State Choices
ESTADO_ABIERTA = "ABIERTA"
ESTADO_ACEPTADA = "ACEPTADA"
ESTADO_COMPLETADA = "COMPLETADA"
ESTADO_CANCELADA = "CANCELADA"
ESTADO_RECHAZADA = "RECHAZADA"
ESTADO_PENDIENTE = "PENDIENTE"


ESTADOS_SOLICITUD = [
    (ESTADO_ABIERTA, "Abierta"),
    (ESTADO_COMPLETADA, "Completada"),
    (ESTADO_CANCELADA, "Cancelada"),
]


ESTADOS_RESPUESTA = [
    (ESTADO_ABIERTA, "Abierta"),
    (ESTADO_ACEPTADA, "Aceptada"),
    (ESTADO_COMPLETADA, "Completada"),
    (ESTADO_RECHAZADA, "Rechazada"),
    (ESTADO_CANCELADA, "Cancelada"),
]
