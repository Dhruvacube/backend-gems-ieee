from pydantic import BaseModel
from typing import Optional
import datetime

class OrganizationSchema(BaseModel):
    name: str
    role: str
    valid_till: datetime.datetime

class GuestSchema(BaseModel):
    name: str
    email: str
    alt_email: Optional[str]
    phone: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    

class GuestCreateSchema(GuestSchema):
    organization_name: Optional[str]
    role: Optional[str]
    valid_till: Optional[datetime.datetime]

class UserCreateSchema(BaseModel):
    unique_id: str
    password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str

class UserLogoutSchema(UserLoginSchema):
    jwt_token: str

class UserEditSchema(GuestCreateSchema):
    profile_photo_link: Optional[str]