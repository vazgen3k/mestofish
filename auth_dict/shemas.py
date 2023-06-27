from typing import Optional

from fastapi import Query
from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserChange(BaseModel):
    name: Optional[str] = Query(default=None, min_length=2, max_length=25)
    last_name: Optional[str] = Query(default=None, min_length=2, max_length=25)
    username: Optional[str] = Query(default=None, min_length=2, max_length=25)
    email: Optional[str] = Query(default=None, min_length=2, max_length=50)



class UserCreate(schemas.BaseUserCreate):
    name: str
    last_name: str
    username: str
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    pass
