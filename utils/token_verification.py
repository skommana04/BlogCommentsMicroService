from functools import wraps
import os
from flask import request, jsonify,g
import jwt

SECRET_KEY = os.environ.get('SECRET_KEY')

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Missing token'}), 401

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            g.username = payload['username']  # Attach user_id to the request object
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Expired token'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        except IndexError:
            return jsonify({'message': 'Bearer token malformed'}), 400

        return f(*args, **kwargs)
    return decorated_function