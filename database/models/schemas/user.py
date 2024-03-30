from pydantic import BaseModel, EmailStr
from typing import Optional
import datetime

class OrganizationSchema(BaseModel):
    name: str
    role: str
    valid_till: datetime.datetime

class GuestSchema(BaseModel):
    name: str
    email: EmailStr
    alt_email: Optional[EmailStr]
    phone: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    

class GuestCreateSchema(GuestSchema):
    organization_name: Optional[str]
    role: Optional[str]
    valid_till: Optional[datetime.datetime]

class UserCreateSchema(BaseModel):
    invite_id: str
    password: str

class UserLoginSchema(BaseModel):
    email: str
    password: str

class UserLogoutSchema(BaseModel):
    jwt_token: str

class UserEditSchema(GuestCreateSchema):
    profile_photo_link: Optional[str]