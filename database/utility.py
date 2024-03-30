from sqlalchemy.orm import declarative_base
from hashlib import sha256
from typing import Union, Optional, Collection
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_scheduler import SchedulerAdmin
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone

from .vars import envConfig

import jwt

Base = declarative_base()

# Create `AdminSite` instance
site = AdminSite(settings=Settings(database_url_async=envConfig.DATABASE_URL))

# Create an instance of the scheduled task scheduler `SchedulerAdmin`
scheduler = SchedulerAdmin.bind(site)


# Add scheduled tasks, refer to the official documentation: https://apscheduler.readthedocs.io/en/master/
# use when you want to run the job at fixed intervals of time
# @scheduler.scheduled_job('interval', seconds=60)
# def interval_task_test():
#     print('interval task is run...')


#hasing function
def hash_password(password: str) -> Union[str, int]:
    '''
    Hashes the password using sha256 algorithm
    :param password: str: password to be hashed
    :return: str: hashed password
    '''
    return sha256(password.encode()).hexdigest()

#compare password function
def comp_pwd(password: str, hashed_Db: str) -> bool:
    '''
    Compares the password with the hashed password
    :param password: str: password to be compared
    :param hashed_Db: str: hashed password from database
    :return: bool: True if password matches the hashed password, False otherwise
    '''
    return hash_password(password) == hashed_Db


InvalidCredentialsException = HTTPException(
    status_code=401,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def create_access_token(
        *,
        data: dict,
        expires: Optional[timedelta] = None,
        scopes: Optional[Collection[str]] = None
    ) -> str:
    """
    Helper function to create the encoded access token using
    the provided secret and the algorithm of the LoginManager instance
    
        
    Args:
        data (dict): The data which should be stored in the token
        expires (datetime.timedelta):  An optional timedelta in which the token expires.
            Defaults to 15 minutes
        scopes (Collection): Optional scopes the token user has access to.

    Returns:
        The encoded JWT with the data and the expiry. The expiry is
        available under the 'exp' key
    """
    to_encode = data.copy()
    
    if expires:
        expires_in = datetime.now(timezone.utc) + expires
    else:
        expires_in = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expires_in})

    if scopes is not None:
        unique_scopes = set(scopes)
        to_encode.update({"scopes": list(unique_scopes)})

    return jwt.encode(to_encode, envConfig.SECRECT_KEY, "HS256")