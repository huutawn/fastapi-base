from sqlalchemy import  Column, String,Boolean, DateTime
from app.helpers.bases import BareBaseModel

class User(BareBaseModel):
    full_name = Column(String)
    email = Column(String,unique=True,index=True)
    hash_password = Column(String(255))
    is_active = Column(Boolean,default=True)
    role = Column(String, default='user')
    last_login = Column(DateTime)