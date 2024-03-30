from sqlalchemy import (
    select,
    insert,
    delete
)

from .models.auth import *
from .models.user import *
from .session import session_obj
from .utility import hash_password
from .models.schemas.user import *

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