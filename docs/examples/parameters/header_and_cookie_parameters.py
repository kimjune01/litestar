from pydantic import BaseModel
from typing_extensions import Annotated

from litestar import Litestar, get
from litestar.exceptions import NotAuthorizedException
from litestar.params import CookieParameter, HeaderParameter

USER_DB = {
    1: {
        "id": 1,
        "name": "John Doe",
    },
}

VALID_TOKEN = "super-secret-secret"
VALID_COOKIE_VALUE = "cookie-secret"


class User(BaseModel):
    id: int
    name: str


@get(path="/users/{user_id:int}/")
async def get_user(
    user_id: int,
    token: Annotated[str, HeaderParameter(name="X-API-KEY")],
    cookie: Annotated[str, CookieParameter(name="my-cookie-param")],
) -> User:
    if token != VALID_TOKEN or cookie != VALID_COOKIE_VALUE:
        raise NotAuthorizedException
    return User.model_validate(USER_DB[user_id])


app = Litestar(route_handlers=[get_user])
