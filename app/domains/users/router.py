from fastapi import APIRouter, Depends, Path
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession  # ✅ Thêm import

from app.db.base import get_db  # ✅ Thêm import
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
# Lưu ý: permission_required cũng cần được viết lại dưới dạng async nếu nó có truy cập DB
require_admin_role = permission_required('admin')


@router.post('', response_model=DataResponse[UserResponse])
# ✅ Chuyển sang async và nhận db session
async def register(register_data: UserCreateReq,
                   db: AsyncSession = Depends(get_db)
                   ):
    # ✅ Dùng await và truyền db vào service
    register_user = await user_service.register(db=db, data=register_data)
    return DataResponse(data=register_user)


@router.get('', response_model=DataResponse[UserResponse])
# ✅ Chuyển sang async (vì get_current_user là async)
async def get_current_info(
        user: User = Depends(get_current_user)
):
    # Hàm service này không cần db và không phải là async
    response = user_service.get_my_profile(user)
    return DataResponse(data=response)


@router.put('', response_model=DataResponse[UserResponse])
# ✅ Chuyển sang async và nhận db session
async def update_me(update_data: UpdateUserReq,
                    user: User = Depends(get_current_user),
                    db: AsyncSession = Depends(get_db)
                    ):
    # ✅ Dùng await và truyền db vào service
    user_updated = await user_service.update_me(db=db, user=user, data=update_data)
    return DataResponse(data=user_updated)


@router.put('/{user_id}', response_model=DataResponse[UserResponse])
# ✅ Chuyển sang async và nhận db session
async def update(data: UpdateUserReq,
                 user_id: int = Path(),
                 db: AsyncSession = Depends(get_db)
                 ):
    # ✅ Dùng await và truyền db vào service
    user_updated = await user_service.update(db=db, id=user_id, data=data)
    return DataResponse(data=user_updated)


@router.get('/all', response_model=Page[UserResponse])
# ✅ Chuyển sang async và nhận db session
async def get_all(params: PaginationParams = Depends(),
                  db: AsyncSession = Depends(get_db),
                  current_admin: User = Depends(require_admin_role)
                  ) -> Any:
    # ✅ Dùng await và truyền db vào service
    users_page = await user_service.get_all_user(db=db, params=params)
    return users_page
