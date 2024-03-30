from sqlalchemy.orm import declarative_base
from hashlib import sha256
from typing import Union
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_scheduler import SchedulerAdmin

from .vars import envConfig

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
