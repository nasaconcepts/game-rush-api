# from django.utils.deprecation import MiddlewareMixin
import jwt
from api.util.utils import api_response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.exceptions import AuthenticationFailed

class JWTMiddleware:
    """Middleware to enforce access token expiration."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get("Authorization", None)

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                # Decode the token and check expiration
                decoded_token = AccessToken(token)
                if decoded_token.is_expired:
                    return api_response(success=False,message="Access token has expired",status=401)

            except jwt.ExpiredSignatureError:
                return api_response(success=False,message="Access token has expired",status=401)
            except jwt.InvalidTokenError:
                return api_response(success=False,message="Invalid token",status=401)

        return self.get_response(request)