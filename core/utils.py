from datetime import timedelta, datetime
import jwt
from django.conf import settings
from random import randint
from kavenegar import *
from config.settings import env


JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_LIFETIME = timedelta(minutes=300)
REFRESH_TOKEN_LIFETIME = timedelta(days=7)


def create_jwt_token(user_id, is_refresh=False):

    expiration_time = datetime.utcnow() + (REFRESH_TOKEN_LIFETIME if is_refresh else ACCESS_TOKEN_LIFETIME)
    payload = {
        "user_id": user_id,
        "exp": expiration_time,
        "type": "refresh" if is_refresh else "access",
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_jwt_token(token):

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def decode_jwt_token(token):
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])



def generate_otp_code():
    return str(randint(100000, 999999))


def send_sms_otp_code(mobile_number, code):
    try:
        api = KavenegarAPI(env.kavenegar_api_key)
        params = {
            'sender': '',
            'receptor': mobile_number,
            'message': f'کد تایید شما: {code}'
        }
        response = api.sms_send(params)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)

