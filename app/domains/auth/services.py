import logging

from .schemas import Token, AuthReq
from app.domains.users.models import User
from .models import InvalidateToken
from app.core.config import settings
from datetime import datetime
import jwt
from app.core.security import verify_password
from app.helpers.exception_handler import CustomException, ExceptionType
from app.core.security import create_access_token, create_refresh_token
from fastapi_sqlalchemy import db


class AuthService:
    def __init__(self):
        pass

    def authenticate(self, data: AuthReq) -> Token:
        user: User | None = db.session.query(User).filter_by(email=data.email).first()
        if not user:
            raise CustomException(error_type=ExceptionType.USER_NOT_EXITS)
        if not verify_password(data.password, user.hash_password):
            raise CustomException(error_type=ExceptionType.WRONG_PASSWORD)
        access_token = create_access_token(user=user)
        refresh_token = create_refresh_token(subject=user.id)
        return Token(access_token=access_token,
                     refresh_token=refresh_token)

    def refresh_token(self, token: str) -> Token:
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.SECRET_KEY,
                algorithms=[settings.SECURITY_ALGORITHM]
            )

            if payload.get('type') != 'refresh':
                raise CustomException(error_type=ExceptionType.INVALIDATE_TOKEN)

            user_id = int(payload.get('sub'))
            user: User | None = db.session.query(User).get(user_id)
            if not user:
                raise CustomException(error_type=ExceptionType.USER_NOT_EXITS)
            new_access_token = create_access_token(user=user)
            return Token(access_token=new_access_token, refresh_token=token)


        except (jwt.PyJWTError, CustomException) as e:
            logging.error(f"Failed to refresh token: {e}")
            raise CustomException(error_type=ExceptionType.INVALIDATE_TOKEN)

    def log_out(self, token: str):
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.SECURITY_ALGORITHM])

        jti = payload.get('jti')
        exp = payload.get('exp')
        invalidated_token = InvalidateToken(jti=jti, exp=datetime.fromtimestamp(exp))
        db.session.add(invalidated_token)
        db.session.commit()
        return 'success'
