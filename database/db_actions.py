import datetime
from os import name
from sqlalchemy import (
    select,
    insert,
    delete,
    update
)

from .models.auth import *
from .models.user import *
from .session import session_obj
from .models.schemas.user import *
from .vars import MISSING

from typing import Union
from hashlib import sha256

#hasing function
def hash_password(password: str) -> Union[str, int]:
    '''
    Hashes the password using sha256 algorithm
    :param password: str: password to be hashed
    :return: str: hashed password
    '''
    return sha256(password.encode()).hexdigest()

async def return_user(email: str, via_id):
    """
    Get a user from the db
    :param user_id: E-Mail of the user
    :return: None or the user object
    """
    if via_id:
        query = select(User).where(
            User.invite_id == email
        )
    else:
        query = select(User).where(
                User.email == email
        )
    async with session_obj() as session:
        record = await session.execute(query)
        record = record.fetchone()
    return record

async def return_guests(_id: int):
    """
    Get a user from the db
    :param user_id: E-Mail of the user
    :return: None or the user object
    """
    query = select(User).where(
        Guest.id == _id
    )
    async with session_obj() as session:
        record = await session.execute(query)
        record = record.fetchone()
    return record

async def insert_session(user, token: str):
    """
    Insert a session into the database
    :param user_id: User ID
    :param token: Session token
    :return: None
    """
    async with session_obj() as session:
        query = insert(Session).values(
            user_as=user,
            token=token
        )
        await session.execute(query)
        await session.commit()

async def remove_session(token: str):
    """
    Remove a session from the database
    :param token: Session token
    :return: None
    """
    async with session_obj() as session:
        query = delete(Session).where(
            Session.token == token
        )
        await session.execute(query)
        await session.commit()

async def create_user(user: UserCreateSchema):
    """
    Insert a user into the database
    :param user: User object schema
    :return: None
    """
    guest_details = await return_guests(int(user.invite_id))
    async with session_obj() as session:
        query = insert(User).values(
            email=guest_details.email,
            password=hash_password(user.password),
            invite_id=user.invite_id,
            phone=guest_details.phone,
            name=guest_details.name,
            alt_email=guest_details.alt_email,
            organizations=guest_details.organizations
        )
        await session.execute(query)
        await session.commit()

async def create_invite(user: GuestCreateSchema) -> int:
    """
    Insert a user into the database
    :param user: User object schema
    :return: None
    """
    async with session_obj() as session:
        if user.organization_name is not MISSING:
            query = insert(Organization).values(
                name=user.organization_name,
                role=user.role,
                valid_till=user.valid_till
            ).returning(Organization.id)
            result = await session.execute(query)
            row = result.fetchone()
            await session.commit()
            
            query = insert(Guest).values(
                name=user.name,
                email=user.email,
                alt_email=user.alt_email,
                phone=user.phone,
                organizations=Organization(id=row.id, name=user.organization_name, role=user.role, valid_till=user.valid_till)
            ).returning(Guest.id)
        else:
            query = insert(Guest).values(
                name=user.name,
                email=user.email,
                alt_email=user.alt_email,
                phone=user.phone
            ).returning(Guest.id)
        result = await session.execute(query)
        row = result.fetchone()
        await session.commit()
        return int(row.id)

async def get_session(session_data: UserLogoutSchema, return_user: bool = False) -> Union[bool, int]:
    """
    Get a session from the database
    :param session_data: Session data
    :return: bool
    """
    async with session_obj() as session:
        query = select(Session).where(
            Session.token == session_data.jwt_token
        )
        record = await session.execute(query)
        record = record.fetchone()
    if return_user:
        return record.user_as.email
    return record is not None or record is not MISSING

async def delete_redundant_sessions():
    """
    Delete redundant sessions from the database
    :return: None
    """
    async with session_obj() as session:
        query = delete(Session).where(
            Session.valid_till < datetime.datetime.now() - datetime.timedelta(minutes=15)
        )
        await session.execute(query)
        await session.commit()

async def update_user(user: UserEditSchema):
    """
    Update a user in the database
    :param user: User object schema
    :return: None
    """
    async with session_obj() as session:
        query = update(User).where(
            User.email == user.email
        ).values(
            phone=user.phone,
            alt_email=user.alt_email,
            updated_at=datetime.datetime.now(),
            profile_photo=user.profile_photo_link,
            name=user.name
        )
        await session.execute(query)
        await session.commit()