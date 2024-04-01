from fastapi import FastAPI

from database.utility import *
from database.vars import MISSING
from database.sync_session import get_db
from database.models.auth import *
from database.models.user import *
from database.models.schemas.user import *
from database.db_actions import *
import sys, asyncio

try:
    import uvloop  # type: ignore
except ImportError:
    if sys.platform.startswith(("win32", "cygwin")):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    uvloop.install()

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm

app = FastAPI()
# mount AdminSite instance
site.mount_app(app)

run = asyncio.new_event_loop().run_until_complete


def query_user(email: str, via_id: bool = False):
    """
    Get a user from the db
    :param user_id: E-Mail of the user
    :return: None or the user object
    """
    return run(return_user(email, via_id))


@app.get("/")
def home():
    return {
        "Hello": "World",
        "description": "This is the backend work for the IEEE GEMS Backend Task, Instructions to host locally is given in README.md. This has been developed using python language and FastAPI framework.",
        "author": "Dhruva Shaw",
        "documentation": "http://127.0.0.1:80/docs",
        "admin panel for the scheduler": "http://127.0.0.1:80/admin",
    }


@app.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = query_user(email)
    if not user:
        # you can return any response or error of your choice
        raise InvalidCredentialsException
    if hash_password(password) != user["password"]:
        raise InvalidCredentialsException

    access_token = create_access_token(
        data={"sub": email, "pwd": hash_password(password)}
    )
    run(insert_session(user, access_token))
    return {
        "status": 200,
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "User.id": user["id"],
        "User.email": user["email"],
        "User.name": user["name"],
        "User.profile_photo": user["profile_photo"],
        "User.created_at": user["created_at"],
        "User.updated_at": user["updated_at"],
        "User.organizations": user["organizations"],
        "User.phone": user["phone"],
        "User.alt_email": user["alt_email"],
    }


@app.post("/logout")
def logout(user: UserLogoutSchema, db=Depends(get_db)):
    if user.jwt_token is MISSING:
        raise HTTPException(status_code=400, detail="No token provided")
    if not run(get_session(user)):
        raise HTTPException(status_code=400, detail="Invalid session")
    run(remove_session(user.jwt_token))
    return {"status": 200, "message": "Logout successful"}


@app.post("/signup")
def register(user: UserCreateSchema, db=Depends(get_db)):
    if query_user(user.invite_id, True) is not None:
        raise HTTPException(
            status_code=400, detail="A user with this invite id already exists"
        )
    run(create_user(user))
    return {
        "status": 200,
        "message": "User created successfully",
    }


@app.post("/invitation")
def invitation(invite: GuestCreateSchema, db=Depends(get_db)):
    if invite.jwt_token is MISSING:
        raise HTTPException(status_code=400, detail="No token provided")
    if not run(get_session(invite)):
        raise HTTPException(status_code=400, detail="Invalid session")
    if query_user(invite.email) is not None:
        raise HTTPException(
            status_code=400, detail="A user with this email already exists"
        )
    unique_id = run(create_invite(invite))
    return {
        "status": 200,
        "message": "Invite created successfully",
        "invitation_id": unique_id,
    }


@app.post("/edituser")
def edituser(user: UserEditSchema, db=Depends(get_db)):
    if user.jwt_token is MISSING:
        raise HTTPException(status_code=400, detail="No token provided")
    if not run(get_session(user)):
        raise HTTPException(status_code=400, detail="Invalid session")
    run(update_user(user))
    return {
        "status": 200,
        "message": "User updated successfully",
    }
