from fastapi import Depends
from fastapi_users import FastAPIUsers
from sqlalchemy.orm import Session, query
from sqlalchemy import update, Integer

from auth_dict.auth import auth_backend
from auth_dict.manager import get_user_manager
from models.models import User


def get_name():
    fastapi_users = FastAPIUsers[User, Integer](
        get_user_manager,
        [auth_backend],
    )
    current_user = fastapi_users.current_user()
    user = Depends(current_user)
    print(user.name)




def change_profile(profile, user_id, db: Session):
    value = db.query(User).filter(User.id == user_id).first()
    if profile.name is not None:
        value.name = profile.name
    if profile.last_name is not None:
        value.last_name = profile.last_name
    if profile.username is not None:
        value.username = profile.username
    if profile.email is not None:
        value.email = profile.email
    db.flush()
    db.commit()
    return {'ok'}
