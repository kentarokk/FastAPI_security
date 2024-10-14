from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, Security
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return fake_decode_token(token)


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


current_user = Annotated[User, Security(get_current_user)]


def fake_decode_token(token: str) -> User:
    return User(
        username=token + "fakedecoded",
        email="john@example.com",
        full_name="John Doe",
    )


@app.get("/users/me")
async def read_users_me(current_user: current_user) -> User:
    return current_user
