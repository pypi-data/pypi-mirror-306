from jwt import decode, ExpiredSignatureError, InvalidTokenError
from jwt_manager.application.config import SECRET_KEY
from jwt_manager.domain.models import UserData
from jwt_manager.exceptions.custom_exceptions import TokenExpiredException, InvalidTokenException

class JWTManager:
    def __init__(self, secret_key=SECRET_KEY):
        self.secret_key = secret_key

    def decode_token(self, token: str) -> UserData:
        """
        Main Function to decode a JWT token
        :param token: JWT token
        :return: UserData
        :raises TokenExpiredException:
        :raises InvalidTokenException:
        """
        try:
            payload = decode(token, self.secret_key, algorithms=["HS256"])
            return UserData(payload)
        except ExpiredSignatureError:
            raise TokenExpiredException("Token has expired")
        except InvalidTokenError:
            raise InvalidTokenException("Invalid token")