from rest_framework.response import Response

def api_response(success=True, data=None, message="", errors=None, status=200):
    """
    Standard API response format.
    """
    response = {
        "success": success,
        "data": data,
        "message": message,
        "errors": errors,
    }
    return Response(response, status=status)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.
    """
    from rest_framework.views import exception_handler
    response = exception_handler(exc, context)

    if response is not None:
        return api_response(
            success=False,
            message="An error occurred",
            errors=response.data,
            status=response.status_code
        )
    return api_response(
        success=False,
        message="Internal server error",
        errors=str(exc),
        status=500
    )