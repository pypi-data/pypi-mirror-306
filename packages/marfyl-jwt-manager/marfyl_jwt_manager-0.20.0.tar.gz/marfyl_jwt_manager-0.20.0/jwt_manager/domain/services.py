from jwt import decode, encode, ExpiredSignatureError, InvalidTokenError
from jwt_manager.application.config import SECRET_KEY, ALGORITHM, EXPIRATION_MINUTES
from jwt_manager.domain.models import UserData
from jwt_manager.exceptions.custom_exceptions import TokenExpiredException, InvalidTokenException
from datetime import datetime, timedelta

class JWTManager:
    def __init__(self, secret_key=SECRET_KEY, algorithm=ALGORITHM, expires_in=EXPIRATION_MINUTES):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_in = expires_in

    def create_token(self, user_data: UserData) -> str:
        """
        Create a JWT using UserData model.
        :param user_data: An instance of UserData
        :return: token
        """
        payload = user_data.__dict__.copy()  # Convert UserData to dictionary
        payload['exp'] = datetime.utcnow() + timedelta(minutes=self.expires_in)
        token = encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def decode_token(self, token: str) -> UserData:
        """
        Main Function to decode a JWT token
        :param token: JWT token
        :return: UserData
        :raises TokenExpiredException:
        :raises InvalidTokenException:
        """
        try:
            payload = decode(token, self.secret_key, algorithms=[ALGORITHM])
            return UserData(payload)
        except ExpiredSignatureError:
            raise TokenExpiredException("Token has expired")
        except InvalidTokenError:
            raise InvalidTokenException("Invalid token")