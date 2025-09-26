from fastapi import APIRouter, Depends
from .schemas import Token, AuthReq
from .services import AuthService
from app.helpers.bases import DataResponse
from app.helpers.deps import get_current_user
import logging

router = APIRouter()

auth_service = AuthService()


@router.post('', response_model=DataResponse[Token])
def authenticate(data: AuthReq):
    token = auth_service.authenticate(data)
    return DataResponse(data=token)


@router.post('/refresh', response_model=DataResponse[Token])
def refresh(token: str):
    token = auth_service.refresh_token(token)
    return DataResponse(data=token)


@router.post('/logout', response_model=DataResponse)
def logout(token: str, user = Depends(get_current_user)):
    auth_service.log_out(token)
    return DataResponse(message='success')
