from google.oauth2 import id_token
from google.auth.transport import requests
from api.authentication.user_manager import UserManager
from api.authentication.user_athenticate_repo_impl import authenticate_repository
import os
import jwt
class GoogleSignIn:
    google_api_key = os.getenv("GOOGLE_CLIENT_ID")
    user_manager = UserManager()
    user_repo = authenticate_repository()

    def google_auth(self,token):
        try:

            idinfo = id_token.verify_oauth2_token(token,requests.Request(),self.google_api_key)

            email = idinfo["email"]

            user = self.user_repo.fetch_user(email)
            print(f"Show user -> {user}")
            if not user:
                print(f"Show user 2 -> {user}")
                return self.user_manager.signup_user(email,password=None,login_mode='google')  #  Note that no password is required for google
            return self.user_manager.generate_tokens(user)

        except Exception as ex:
            print(f"Error authenticating with google service {ex}")
            return None