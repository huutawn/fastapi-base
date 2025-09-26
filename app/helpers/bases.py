from datetime import datetime
from typing import Optional, Any, TypeVar, Generic, List
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import as_declarative, declared_attr

T = TypeVar('T')


@as_declarative()
class Base:
    """
    Lớp base mà tất cả các model khác sẽ kế thừa.
    """
    __abstract__ = True

    # Tự động tạo tên bảng dựa trên tên class
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BareBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)  # Nên dùng utcnow
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ResponseSchemaBase(BaseModel):
    code: str = '000'
    message: str = 'Thành công'


# Lớp chứa dữ liệu linh hoạt (kế thừa từ Base)
class DataResponse(ResponseSchemaBase, Generic[T]):
    data: Optional[T] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True
    )


class MetadataSchema(BaseModel):
    current_page: int
    page_size: int
    total_items: int
