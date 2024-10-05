
from core.utils import ResponseStruct
from rest_framework.views import exception_handler


class InvalidStateTransition(Exception):
    """Excepción personalizada para manejar intentos no válidos de cambio de estado."""
    def __init__(self, message):
        super().__init__(message)


def custom_exception_handler(exc, context):
    """Custom handler for API exceptions."""
    response = exception_handler(exc, context)
    
    if response is not None:
        # Return a structured error response using ResponseStruct
        error_response = ResponseStruct(
            status='error',
            message=str(exc),
            error_code=response.status_code
        )
        return error_response.to_response(status_code=response.status_code)
    
    return response


# settings.py
#REST_FRAMEWORK = {
#    'EXCEPTION_HANDLER': 'core.exceptions.custom_exception_handler',
#}

