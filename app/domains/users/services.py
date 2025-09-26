import logging

from fastapi.security import HTTPBearer
from app.helpers.exception_handler import CustomException, ExceptionType
from .models import User
from fastapi_sqlalchemy import db
from app.helpers.deps import get_current_user
from app.core.security import verify_password, get_password_hash
from .schemas import UserCreateReq, UserResponse, UpdateUserReq
from .mappers import UserMapper
from app.helpers.paging import PaginationParams, paginate, Page


class UserService:
    def __init__(self):
        pass

    def register(self, data: UserCreateReq) -> UserResponse:
        print(">>> Bắt đầu hàm register...")

        exits_user = db.session.query(User).filter(User.email == data.email).first()
        if exits_user:
            raise CustomException(error_type=ExceptionType.EMAIL_IS_TAKEN)
        new_user = User(
            email=data.email,
            hash_password=get_password_hash(data.password),
            is_active=data.is_active,
            full_name=data.full_name,
            role=data.role
        )
        db.session.add(new_user)
        db.session.commit()
        db.session.refresh(new_user)
        return UserMapper.to_user_response(new_user)

    def get_my_profile(self, user: User) -> UserResponse:
        logging.info(user.id)
        return UserMapper.to_user_response(user)

    def update_me(self, user: User, data: UpdateUserReq) -> UserResponse:
        user.email = user.email if data.email is None else data.email
        user.role = user.role if data.role is None else data.role
        user.full_name = user.full_name if data.full_name is None else data.full_name
        db.session.commit()
        db.session.refresh(user)
        return UserMapper.to_user_response(user)

    def update(self, id: int, data: UpdateUserReq) -> UserResponse:
        user: User = db.session.query(User).get(id)
        if not user:
            raise CustomException(error_type=ExceptionType.USER_NOT_EXITS)
        user.email = user.email if data.email is None else data.email
        user.role = user.role if data.role is None else data.role
        user.full_name = user.full_name if data.full_name is None else data.full_name
        db.session.commit()
        db.session.refresh(user)
        return UserMapper.to_user_response(user)

    def get_all_user(self, params: PaginationParams):
        _query = db.session.query(User)
        mapper = UserMapper.to_user_response
        users = paginate(model=User, query=_query, params=params, mapper=mapper)

        return users
