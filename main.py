from typing import Union

from fastapi import FastAPI
from fastapi_login import LoginManager

from database.utility import site
from database.vars import envConfig
import sys, asyncio

try:
    import uvloop  # type: ignore
except ImportError:
    if sys.platform.startswith(("win32", "cygwin")):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    uvloop.install()

app = FastAPI()
# mount AdminSite instance
site.mount_app(app)

manager = LoginManager(envConfig.SECRET_KEY, "/login")

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}