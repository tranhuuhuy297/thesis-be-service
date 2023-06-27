import hashlib
import time
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from util.logger_util import logger
from util.time_util import now
from util.const_util import JWT_SECRET_KEY, JWT_ALGORITHM


def encode_sha256(string):
    decode_string = hashlib.sha256(string.encode('utf-8')).hexdigest()
    return decode_string


def encode_token(result) -> str:
    expire = now() + timedelta(
        seconds=60 * 60 * 24 * 3  # Expired after 3 days
    )
    to_encode = {
        "expire_time": int(round(expire.timestamp())), **result
    }
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt, int(expire.timestamp())


def decode_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM], options={'verify_signature': False})
        return decoded_token if decoded_token["expire_time"] >= time.time() else None
    except Exception as e:
        logger.error(e, exc_info=True)
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True, check_admin=False):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.check_admin = check_admin
        self.credential = None

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            self.credential = self.verify_jwt(credentials.credentials)
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, token: str) -> bool:
        try:
            payload = decode_token(token)
        except:
            payload = None
        if self.check_admin and payload.get('role', '') != 'admin':
            logger.error('not admin permission', exc_info=True)
            return None
        return True
