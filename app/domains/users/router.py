from fastapi import APIRouter, Depends, Path
from typing import Any
from app.helpers.bases import DataResponse
from .schemas import UserCreateReq, UserResponse, UpdateUserReq
from .services import UserService
from .models import User
from app.helpers.deps import get_current_user
from app.helpers.paging import Page, PaginationParams
from app.helpers.login_manager import permission_required
import logging

router = APIRouter()

user_service = UserService()
require_admin_role = permission_required('admin')

@router.post('', response_model=DataResponse[UserResponse])
def register(register_data: UserCreateReq
             ):
    register_user = user_service.register(data=register_data)
    return DataResponse(data=register_user)


@router.get('', response_model=DataResponse[UserResponse])
def get_current_info(
        user: User = Depends(get_current_user)
):
    response = user_service.get_my_profile(user)
    return DataResponse(data=response)


@router.put('', response_model=DataResponse[UserResponse])
def update_me(update_data: UpdateUserReq, user: User = Depends(get_current_user)
              ):
    user_updated = user_service.update_me(user=user, data=update_data)
    return DataResponse(data=user_updated)


@router.put('/{user_id}', response_model=DataResponse[UserResponse])
def update(data: UpdateUserReq, user_id: int = Path()):
    user_updated = user_service.update(id=user_id, data=data)
    return DataResponse(data=user_updated)


@router.get('/all', response_model=Page[UserResponse])
def get_all(params: PaginationParams = Depends(),
            current_admin: User = Depends(require_admin_role)) -> Any:
    users_page = user_service.get_all_user(params=params)
    return users_page
