from functools import wraps
from flask import request
from jwt_utils import secret


def require_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token.lower() != secret.lower():
            return 'Unauthorized', 401
        return func(*args, **kwargs)
    return wrapper
