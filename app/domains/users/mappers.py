from .schemas import UserResponse
from .models import User

class UserMapper:
    @staticmethod
    def to_user_response(user: User) -> UserResponse:
        return UserResponse(
            id = user.id,
            email = user.email,
            full_name = user.full_name,
            last_login = user.last_login,
            is_active = user.is_active,
            role = user.role
        )
