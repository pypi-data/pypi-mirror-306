from fastapi import Request, HTTPException
from jwt_manager.domain.services import JWTManager
from jwt_manager.infrastructure.header_parser import extract_token_from_header

jwt_manager = JWTManager()

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