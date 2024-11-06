from fastapi import Request, HTTPException

def extract_token_from_header(request: Request) -> str:
    """
    to extract token from request header
    :param request: Request with token
    :return: auth_header separated by blank
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    return auth_header.split(" ")[1]