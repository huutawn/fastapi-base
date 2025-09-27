import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession  # Quan trọng

from .models import User
# ❌ KHÔNG CÒN import db từ fastapi_sqlalchemy
from app.helpers.deps import get_current_user
from app.core.security import verify_password, get_password_hash
from .schemas import UserCreateReq, UserResponse, UpdateUserReq
from .mappers import UserMapper
from app.helpers.paging import PaginationParams, paginate, Page  # Giả sử paginate đã được sửa
from app.helpers.exception_handler import CustomException, ExceptionType


class UserService:
    def __init__(self):
        pass

    # THAY ĐỔI 1: Chuyển sang async def
    # THAY ĐỔI 2: Nhận db: AsyncSession làm tham số
    async def register(self, db: AsyncSession, data: UserCreateReq) -> UserResponse:
        print(">>> Bắt đầu hàm register...")

        # THAY ĐỔI 3: Dùng select() và await db.execute()
        query = select(User).filter(User.email == data.email)
        result = await db.execute(query)
        exits_user = result.scalars().first()

        if exits_user:
            raise CustomException(error_type=ExceptionType.EMAIL_IS_TAKEN)

        new_user = User(
            email=data.email,
            hash_password=get_password_hash(data.password),
            is_active=data.is_active,
            full_name=data.full_name,
            role=data.role
        )
        db.add(new_user)
        # THAY ĐỔI 4: Dùng await cho commit và refresh
        await db.commit()
        await db.refresh(new_user)
        return UserMapper.to_user_response(new_user)

    # LƯU Ý: Hàm này không tương tác DB nên không cần async
    def get_my_profile(self, user: User) -> UserResponse:
        logging.info(user.id)
        return UserMapper.to_user_response(user)

    async def update_me(self, db: AsyncSession, user: User, data: UpdateUserReq) -> UserResponse:
        user.email = user.email if data.email is None else data.email
        user.role = user.role if data.role is None else data.role
        user.full_name = user.full_name if data.full_name is None else data.full_name

        await db.commit()
        await db.refresh(user)
        return UserMapper.to_user_response(user)

    async def update(self, db: AsyncSession, user_id: int, data: UpdateUserReq) -> UserResponse:
        # THAY ĐỔI: Dùng await db.get() để lấy đối tượng theo ID
        user = await db.get(User, user_id)
        if not user:
            raise CustomException(error_type=ExceptionType.USER_NOT_EXITS)

        user.email = user.email if data.email is None else data.email
        user.role = user.role if data.role is None else data.role
        user.full_name = user.full_name if data.full_name is None else data.full_name

        await db.commit()
        await db.refresh(user)
        return UserMapper.to_user_response(user)

    async def get_all_user(self, db: AsyncSession, params: PaginationParams):
        # 1. Tạo câu lệnh select()
        _query = select(User)

        mapper = UserMapper.to_user_response

        # 2. Gọi hàm paginate bất đồng bộ với await
        users = await paginate(
            db=db,
            model=User,
            query=_query,
            params=params,
            mapper=mapper
        )

        return users
