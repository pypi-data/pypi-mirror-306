from fastapi import Request, HTTPException
from jwt_manager.domain import JWTManager
from jwt_manager.domain.models import UserData
from jwt_manager.infrastructure.header_parser import extract_token_from_header

jwt_manager = JWTManager()


def generate_token_for_user(user_data: dict) -> str:
    """
    Main Function to generate JWT token from user data dictionary.
    :param user_data: Dictionary containing user information
    :return: token
    """
    try:
        user_data_instance = UserData(user_data)
        return jwt_manager.create_token(user_data_instance)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


def get_current_user(request: Request):
    """
    Main Function to get current user
    :param request: info user
    :return: jwt_manager.decode_token(token)
    """
    token = extract_token_from_header(request)
    try:
        user_data = jwt_manager.decode_token(token)
        return user_data
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
