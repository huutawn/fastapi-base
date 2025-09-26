from app.helpers.bases import BareBaseModel
from sqlalchemy import String, Column, DateTime


class InvalidateToken(BareBaseModel):
    jti = Column(String,unique=True,nullable=False,index=True)
    exp = Column(DateTime)
