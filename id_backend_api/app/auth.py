import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify

SECRET_KEY = os.getenv("SECRET_KEY", "changeme")

# PUBLIC_INTERFACE
def encode_auth_token(user_id, expires_in=3600):
    """Generates JWT token for generic user (no roles/RBAC)"""
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=expires_in)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# PUBLIC_INTERFACE
def decode_auth_token(token):
    """Decode JWT token and return payload, else raise exception"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# PUBLIC_INTERFACE
def jwt_required():
    """
    Decorator to protect endpoints (authentication only, not authorization).
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            auth_header = request.headers.get("Authorization", "")
            if not auth_header.startswith("Bearer "):
                return jsonify({"message": "Missing auth header"}), 401
            token = auth_header[7:]
            data = decode_auth_token(token)
            if not data:
                return jsonify({"message": "Invalid or expired token"}), 401
            request.user = {"id": data["sub"]}
            return f(*args, **kwargs)
        return wrapper
    return decorator
