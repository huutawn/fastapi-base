from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import jwt
from pydantic import ValidationError
from app.core.config import settings
from fastapi_sqlalchemy import db
from ..domains.users.models import User
from ..domains.auth.models import InvalidateToken
from ..domains.users.schemas import TokenPayload
from ..helpers.exception_handler import CustomException, ExceptionType
import logging

reusable_oauth2 = HTTPBearer(scheme_name='Authorization')


def get_current_user(http_authorization_credentials=Depends(reusable_oauth2)) -> User:
    """
    Decode JWT token to get user_id => return User info from DB query
    """
    logging.warning('token')
    try:
        payload = jwt.decode(
            http_authorization_credentials.credentials, settings.SECRET_KEY,
            algorithms=[settings.SECURITY_ALGORITHM]
        )
        token_data = TokenPayload(sub=payload.get('sub'), jti=payload.get('jti'),type=payload.get('type'))
        if token_data.type == 'refresh':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='user is not authenticated'

            )
        token_jti = token_data.jti
        logging.info(token_jti)
        if not token_jti:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='could not get jti'
            )
        is_valid = db.session.query(InvalidateToken).filter(InvalidateToken.jti == token_jti).first()
        logging.info(is_valid)
        if is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='user is not authenticated'
            )
        int_token = int(token_data.sub)
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate credentials",
        )
    user = db.session.query(User).get(int_token)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
