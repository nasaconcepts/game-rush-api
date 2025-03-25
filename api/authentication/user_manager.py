import uuid

from api.authentication.user_athenticate_repo_impl import authenticate_repository
from api.notifications.email_notification import email_notifier
from ..util.utils import api_response
import bcrypt
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager:
    email_service = email_notifier()
    authenticate_repo = authenticate_repository()

    def __init__(self):
        self.email_service = email_notifier()
        self.refresh = RefreshToken()

    def signup_user(self, email: str, password=None,login_mode='custom'):
        # create user with hashed password
        hashed_password =None

        print(f"show email in sign up user ->{email}")
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
            "verificationToken": str(uuid.uuid4()) if login_mode=='google' else None
        }
        if self.authenticate_repo.create_user(user_data):
            # send email verification
            # self.email_service.send_verification_email(user_data.get("email"), user_data["verificationToken"])
            return api_response(success=True, data={"email": email}, message="User has been created successfully",
                                status=200)

    def authenticate(self, email, password):
        # Authenticate user by checking the hash password
        user = self.authenticate_repo.fetch_user(email)
        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"].encode("utf-8")):
            return user  # Authentication successful
        return None

    def generate_tokens(self, user):
        self.refresh["email"] = user["email"]
        print(f"Show users {user}")

        return {
            "accessToken": str(self.refresh.access_token),
            "refreshToken": str(self.refresh),
            "user":{"userId":user["userId"],"isVerified":user["isVerified"]}
        }

    def verify_email(self, token):
        return self.authenticate_repo.verify_email(token)

    def generate_access_token_by_refresh(self, refresh_token):
        """
        Generates a new access token using a valid refresh token.
        """
        try:
            # Decode the refresh token
            refresh = RefreshToken(refresh_token)

            # Generate a new access token
            new_access_token = str(refresh.access_token)

            response = {"accessToken": new_access_token}
            return api_response(success=True, data=response, message="Access token generated successfully", status=200)

        except Exception:
            return api_response(success=False, message="Invalid or expired refresh token", status=401)
