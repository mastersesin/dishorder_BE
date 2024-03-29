from dishorder.views.models import *
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from dishorder import app
from functools import wraps
from flask import request, jsonify
import cv2, re, pytz, time
from datetime import datetime
from math import log, ceil


def deduplicate_image(img1_path, img2_path):
    original = cv2.imread(img1_path)
    duplicated = cv2.imread(img2_path)
    if original.shape == duplicated.shape:
        difference = cv2.subtract(original, duplicated)
        b, g, r = cv2.split(difference)
        if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
            return True
        else:
            return False
    else:
        return False


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


def decode_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'], expires_in=60 * 60 * 2)
    try:
        data = s.loads(token)
        print(data, 'hihi')
        user_id = data['id']
        user_profile = data['profile']
        data = {'user_id': user_id, 'user_profile': user_profile}
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    return data


def login_required(f):
    @wraps(f)
    def decorated_function():
        try:
            auth_header = request.headers.get('Authorization')
            if auth_header:
                auth_header = auth_header.split()
                user_token = auth_header[1]
                s = Serializer(app.config['SECRET_KEY'], expires_in=60 * 60 * 2)
                token_loaded = s.loads(user_token)
                user_id = token_loaded['id']
                user_profile = token_loaded['profile']
                return f({'guard_msg': {'user_id': user_id, 'user_profile': user_profile}})
            else:
                return f({'guard_msg': 'Authorization header not present'})
        except SignatureExpired:
            return f({'guard_msg': 'Token Expired'})
        except BadSignature:
            return f({'guard_msg': 'Warning'})

    return decorated_function


def hour_minute_to_timestamp(string_hour_minute):
    if string_hour_minute:
        hour, minute = string_hour_minute.split(':')
        total_second = (int(hour) * 60 * 60) + (int(minute) * 60)
        return total_second
    else:
        return 0


def timestamp_to_hour_minute(int_second):
    base_hour_with_odd = int_second / 60
    base_hour = base_hour_with_odd / 60
    base_minute = base_hour_with_odd % 60
    return '{}:{}'.format(int(base_hour), int(base_minute))


def validate_input(string, **kwargs):
    is_space = kwargs.get('is_space')
    if not is_space:
        re_default = re.compile('^[a-zA-Z0-9]+[a-zA-Z0-9]$')
        return re_default.match(string)
    if is_space:
        re_with_space_between = re.compile('^[a-zA-Z0-9 ]+[a-zA-Z0-9 ]$')
        return re_with_space_between.match(string)


def get_timestamp_now():
    return int(datetime.now(pytz.timezone('Asia/Saigon')).timestamp())


def get_timestamp_by(month, day):
    dt = datetime.strptime('2019-{}-{}'.format(month, day), '%Y-%m-%d')
    return time.mktime(dt.timetuple())


def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default


def bytes_needed(n):
    if n == 0 or n == 1:
        return 1
    return ceil(log(n*2 + 1, 256))
