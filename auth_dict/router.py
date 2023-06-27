from fastapi import APIRouter, Depends, UploadFile, Query
from fastapi_users import FastAPIUsers
from sqlalchemy import Integer, select
from sqlalchemy.orm import Session

import auth_dict.auth_crud
import models.models
from auth_dict.auth import auth_backend, get_jwt_strategy
from auth_dict.shemas import UserRead, UserChange

from models.models import User, get_db
from auth_dict.manager import get_user_manager

fastapi_users = FastAPIUsers[User, Integer](
    get_user_manager,
    [auth_backend],
)

router_auth = APIRouter(
    prefix="/auth_dict",
    tags=["auth_dict"],
)

current_user = fastapi_users.current_user()


# роутер проверяет уровень доступа и аутентификацию.Берет токен из кукки
# Пока проверка только на обычного пользова
# Это часть фреймворка fastapi-users

def protected_route(user: User = Depends(current_user)):
    return user


@router_auth.put('/change_profile/')
def change(profile: UserChange = Depends(), user: User = Depends(current_user), db: Session = Depends(get_db)):
    return auth_dict.auth_crud.change_profile(profile=profile, user_id=user.id, db=db)
