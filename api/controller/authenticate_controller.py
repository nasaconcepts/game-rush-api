from rest_framework.decorators import api_view
from ..util.utils import api_response
from api.authentication.google_sign import GoogleSignIn
from api.authentication.user_manager import UserManager

google_service = GoogleSignIn()
user_service = UserManager()
@api_view(['POST'])
def google_login(request):
    token = request.data.get('token')
    return google_service.google_auth(token)

@api_view(['POST'])
def register_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    return user_service.signup_user(email, password)

@api_view(['POST'])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = user_service.authenticate(email, password)
    if user:
        tokens = user_service.generate_tokens(user)  # Use custom JWT generator
        
        return api_response(success=True, data=tokens,message="Sign In was successful",status=200)

    return api_response(success=False,message="Invalid credentials",status=400)
@api_view(['GET'])
def verify_email(request, token):
    """Handles email verification when user clicks the link."""
    if user_service.verify_email(token):
        return api_response(success=True,message="Email successfully verified!",status=200)
    return api_response(success=False,message="Invalid or expired verification token.",status=400)
@api_view(["POST"])
def generate_access_token(request):
    refresh_token = request.data.get("refreshToken")
    if not refresh_token:
        return api_response(success=True,message="Refresh token is required",status=400)
    return user_service.generate_access_token_by_refresh(refresh_token)

