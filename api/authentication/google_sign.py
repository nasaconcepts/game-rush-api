from google.oauth2 import id_token
from google.auth.transport import requests
from api.authentication.user_manager import UserManager
from api.db.repositoryimpl.user_athenticate_repo_impl import authenticate_repository
from api.util.utils import api_response
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
                signup_response = self.user_manager.signup_user(email,password=None,login_mode='google') 
                return signup_response  #  Note that no password is required for google
            response = self.user_manager.generate_tokens(user)
            return api_response(success=True, data=response,message="Sign In was successful",status=200)

        except Exception as ex:
            print(f"Error authenticating with google service {ex}")
            return api_response(success=False,message="Invalid token",status=400)