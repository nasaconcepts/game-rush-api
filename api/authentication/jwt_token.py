import jwt
import datetime
from typing import Tuple
import os

# Secret keys for signing tokens
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
REFRESH_TOKEN_SECRET = os.getenv('REFRESH_TOKEN_SECRET')

def do_generate_tokens(email: str) -> Tuple[str, str]:
    """
    Generate access and refresh tokens for a given email.

    Args:
        email (str): The email for which tokens are generated.

    Returns:
        Tuple[str, str]: A tuple containing the access token and refresh token.
    """
    # Define expiration times
    access_token_exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    refresh_token_exp = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    iat_time = datetime.datetime.utcnow()

    # Create payloads
    access_token_payload = {
        "email": email,
        "iat": iat_time,
        "exp": access_token_exp,
        "type": "access"
    }
    refresh_token_payload = {
        "email": email,
        "iat": iat_time,
        "exp": refresh_token_exp,
        "type": "refresh"
    }

    # Generate tokens
    access_token = jwt.encode(access_token_payload, ACCESS_TOKEN_SECRET, algorithm="HS256")
    refresh_token = jwt.encode(refresh_token_payload, REFRESH_TOKEN_SECRET, algorithm="HS256")

    return access_token, refresh_token
