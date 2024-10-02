from dataclasses import dataclass
import os
from typing import Any, Optional

from rest_framework import status as st
from rest_framework.response import Response

# At module level
STATUS_CODE_MAP = {
    getattr(st, attr): attr for attr in dir(st) if attr.startswith("HTTP_")
}


@dataclass
class ResponseStruct:
    """
    A structured response class for handling API responses with detailed information
    about the status, message, payload, and error codes. Provides utility methods
    for determining the status name and type, as well as converting the response to
    a dictionary or DRF Response object.

    Attributes
    ----------
    status : str
        Either "success" or "error" indicating the type of the response.
    message : str
        A descriptive message providing details about the response.
    data : Optional[Any], optional
        The data payload of the response, default is None.
    error_code : Optional[int], optional
        An HTTP status code (e.g., 200, 404), typically used for error handling, default is None.
    """

    status: str  # Either "success" or "error"
    message: str  # A descriptive message
    data: Optional[Any] = None  # Data payload
    error_code: Optional[int] = None  # Error code, typically HTTP status codes

    def get_status_name(self) -> str:
        """Gets the status name (e.g., HTTP_200_OK) corresponding to a given code."""
        return STATUS_CODE_MAP.get(self.error_code, "UNKNOWN_STATUS_CODE")

    def get_status_type(self) -> str:
        """Determines the type of status code (informational, success, redirect, client error, server error)."""
        if self.error_code is None:
            return "No Error Code"

        if self.is_informational(self.error_code):
            return "Informational"
        elif self.is_success(self.error_code):
            return "Success"
        elif self.is_redirect(self.error_code):
            return "Redirect"
        elif self.is_client_error(self.error_code):
            return "Client Error"
        elif self.is_server_error(self.error_code):
            return "Server Error"
        else:
            return "Unknown Error"

    @staticmethod
    def is_informational(code: int) -> bool:
        return 100 <= code <= 199

    @staticmethod
    def is_success(code: int) -> bool:
        return 200 <= code <= 299

    @staticmethod
    def is_redirect(code: int) -> bool:
        return 300 <= code <= 399

    @staticmethod
    def is_client_error(code: int) -> bool:
        return 400 <= code <= 499

    @staticmethod
    def is_server_error(code: int) -> bool:
        return 500 <= code <= 599

    def to_dict(self) -> dict:
        """Converts the response structure to a dictionary."""
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data,
            "error_code": self.error_code,
            "error_code_type": self.get_status_type(),
            "error_code_name": self.get_status_name(self.error_code)
            if self.error_code
            else None,
        }

    def to_response(self, status_code: int = st.HTTP_200_OK) -> Response:
        """
        Creates a Django Rest Framework (DRF) Response object.

        Parameters
        ----------
        status_code : int, optional
            The HTTP status code to set for the response (default is 200, HTTP_200_OK).

        Returns
        -------
        rest_framework.response.Response
            A DRF Response object containing the response data and status code.
        """
        self.error_code = status_code  # Set error_code if not already set
        return Response(self.to_dict(), status=status_code)


def get_env_variable(var_name, default_value=None):
    """Get the environment variable or return a default value."""
    return os.getenv(var_name, default_value)