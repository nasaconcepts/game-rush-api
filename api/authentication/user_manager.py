import uuid

from api.db.repositoryimpl.user_athenticate_repo_impl import authenticate_repository
from api.notifications.email_notification import email_notifier
from ..util.utils import api_response
import bcrypt
from rest_framework_simplejwt.tokens import RefreshToken
from api.authentication.jwt_token import do_generate_tokens
import jwt



class UserManager:
    email_service = email_notifier()
    authenticate_repo = authenticate_repository()
   

    def __init__(self):
        self.email_service = email_notifier()
        self.refresh = RefreshToken()

    def signup_user(self, email: str, password=None,login_mode='custom'):
        # create user with hashed password
        hashed_password =None

        user = self.authenticate_repo.fetch_user(email)
        if user:
            return api_response(success=False, message="User already exist", status=409)
        if password:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        # This "isVerified": password is None, ensures that google sign in does not required verification
        # "verificationToken": str(uuid.uuid4()) if password is not None else None (ensure no token is provided
        user_data = {
            "userId": str(uuid.uuid4()),
            "email": email,
            "password": hashed_password,
            "isVerified": password is None,
            "verificationToken": str(uuid.uuid4()) if login_mode=='custom' else None,
            "isProfiled":False,
            "loginMode":login_mode
        }
        user_created_response  = self.authenticate_repo.create_user(user_data)
        if user_created_response:
            
            tokens = self.generate_tokens(user_created_response)  # Use custom JWT generator
            return api_response(success=True, data=tokens,message="Sign In was successful",status=200)
        return None

    def authenticate(self, email, password):
        # Authenticate user by checking the hash password
        user = self.authenticate_repo.fetch_user(email)
        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
            return user  # Authentication successful
        return None

    def generate_tokens(self, user):
        self.refresh["email"] = user["email"]
        print(f"Show users {user}")
        access_token,refresh_token = do_generate_tokens(user["email"])

        return {
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "user":{"userId":user["userId"],"isVerified":user["isVerified"],"isProfiled":user.get("isProfiled",False),"loginMode":user["loginMode"]}
        }

    def verify_email(self, token):
        return self.authenticate_repo.verify_email(token)

    def generate_access_token_by_refresh(self, refresh_token):
        """
        Generates a new access token using a valid refresh token.
        """
        try:
            # Decode the refresh token
            token_payload = jwt.decode(refresh_token, options={"verify_signature": False})
            email = token_payload.get("email")
            access_token,refresh_token = do_generate_tokens(email)

            # Generate a new access token
           

            response = {"accessToken": access_token, "refreshToken": refresh_token}
            return api_response(success=True, data=response, message="Access token generated successfully", status=200)

        except Exception:
            return api_response(success=False, message="Invalid or expired refresh token", status=401)
