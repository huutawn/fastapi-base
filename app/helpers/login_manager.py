from fastapi import Depends, HTTPException, status
from app.domains.users.models import User
# Giả sử get_current_user đã được định nghĩa chuẩn ở đây
from .deps import get_current_user


# BỎ HOÀN TOÀN HÀM login_required

def permission_required(*required_roles: str):
    def check_permissions(current_user: User = Depends(get_current_user)) -> User:
        # Lấy vai trò của người dùng hiện tại
        user_role = getattr(current_user, 'role', None)

        # Nếu có yêu cầu role và role của user không nằm trong danh sách được phép
        if required_roles and user_role not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không có quyền truy cập tài nguyên này."
            )

        return current_user

    return check_permissions
