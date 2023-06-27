from typing import List

from fastapi import FastAPI, UploadFile, Depends, Form, File
from fastapi_users import FastAPIUsers
from sqlalchemy import Integer
from sqlalchemy.orm import Session

import crud
import tags.tag_shemas
from any.router import router_any
from auth_dict.auth import auth_backend
from models.models import User, get_db
from auth_dict.manager import get_user_manager
from auth_dict.router import router_auth
from auth_dict.shemas import UserRead, UserCreate
from tags import tag_shemas
from tags.get_tags.router import router_tags

fastapi_users = FastAPIUsers[User, Integer](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth_dict/jwt",
    tags=["auth_dict"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth_dict",
    tags=["auth_dict"],
)

current_user = fastapi_users.current_user()

# роутер проверяет уровень доступа и аутентификацию.Берет токен из кукки
# Пока проверка только на обычного пользова
# Это часть фреймворка fastapi-users
app.include_router(router_auth)

# Тут все по меткам на карте
app.include_router(router_tags)

'''
@app.post("/get_geo", response_model=list[tags.tag_shemas.Geo])
def read_geo(map_geo: tags.tag_shemas.MapGeo, db: Session = Depends(get_db)):
    db_geo = crud.get_geo(map_geo=map_geo, db=db)
    return db_geo
'''
'''
@app.post("/geo/", response_model=tags.tag_shemas.GeoCreate)
def create_geo(geo: tags.tag_shemas.GeoCreate, db: Session = Depends(get_db)):
    return crud.create_geo(db=db, geo=geo)
'''
# бесполезные роутеры
app.include_router(router_any)
'''
@app.post("/description/", response_model=tags.tag_shemas.Description)
def create_description(description: tags.tag_shemas.DescriptionCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_description(db=db, description=description, user_id=user_id)


@app.post("/tag/", response_model=tags.tag_shemas.Tag)
def create_tag(tag: tags.tag_shemas.TagCreate, db: Session = Depends(get_db)):
    return crud.create_tag(db=db, tag=tag)
'''
'''
@app.post('/catch/almost whole')
async def create_catch(catch: tags.tag_shemas.CatchCreate, files: list[UploadFile], user: User = Depends(current_user),
                       db: Session = Depends(get_db)):
    if not files:
        return {"message": "No upload file sent"}
    for file in files:
        if file.content_type != "image/jpeg":
            return {"message": 'incorrect file'}
    return crud.create_catch(db=db, uploaded_file=files, id=user.id, catch=catch)

'''
'''
@app.post('/test/almost whole')
async def create_catch(catch: tags.tag_shemas.CatchCreate, files: list[UploadFile], user: User = Depends(current_user),
                       db: Session = Depends(get_db)):
    if not files:
        return {"message": "No upload file sent"}
    for file in files:
        if file.content_type != "image/jpeg":
            return {"message": 'incorrect file'}
    return crud.create_test(db=db, uploaded_file=files, id=user.id, catch=catch)
'''
