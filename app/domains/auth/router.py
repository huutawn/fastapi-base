from fastapi import APIRouter, Depends
from .schemas import Token, AuthReq
from .services import AuthService
from app.helpers.bases import DataResponse
from app.helpers.deps import get_current_user
import logging
from app.db.base import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.domains.users.models import User

router = APIRouter()

auth_service = AuthService()


@router.post('', response_model=DataResponse[Token])
async def authenticate(data: AuthReq,db:AsyncSession = Depends(get_db)):
    token = await auth_service.authenticate(db=db, data=data)
    return DataResponse(data=token)


@router.post('/refresh', response_model=DataResponse[Token])
async def refresh(token: str, db: AsyncSession = Depends(get_db)):
    token = await auth_service.refresh_token(db=db,token=token)
    return DataResponse(data=token)


@router.post('/logout', response_model=DataResponse)
async def logout(
    token: str,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    await auth_service.log_out(db=db, token=token)
    return DataResponse(message='success')
