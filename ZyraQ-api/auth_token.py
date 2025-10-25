from functools import wraps
from flask import request
from jwt_utils import decode_token, JwtError

def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return {"error": "Missing Authorization header"}, 401

        # Expected format: "Bearer <token>"
        parts = auth_header.split(" ")
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return {"error": "Invalid Authorization header format"}, 401

        token = parts[1]

        try:
            decode_token(token)
        except JwtError as e:
            return {"error": str(e)}, 401

        return func(*args, **kwargs)
    return wrapper
