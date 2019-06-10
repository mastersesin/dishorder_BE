from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from dishorder import app
from functools import wraps
from flask import request


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def generate_auth_token(**kwargs):
    user_id = kwargs.get('user_id')
    profile = kwargs.get('profile')
    s = Serializer(app.config['SECRET_KEY'], expires_in=60 * 60 * 2)
    return (s.dumps({'id': str(user_id), 'profile': str(profile)})).decode("utf-8")


def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'], expires_in=60 * 60 * 2)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    return True


def login_required(f):
    @wraps(f)
    def decorated_function():
        try:
            auth_header = request.headers.get('Authorization').split()
            user_token = auth_header[1]
            s = Serializer(app.config['SECRET_KEY'], expires_in=60 * 60 * 2)
            token_loaded = s.loads(user_token)
            user_id = token_loaded['id']
            user_profile = token_loaded['profile']
            return f({'guard_msg': {'user_id': user_id, 'user_profile': user_profile}})
        except SignatureExpired:
            return f({'guard_msg': 'Token Expired'})
        except BadSignature:
            return f({'guard_msg': 'Warning'})

    return decorated_function
