from fastapi import APIRouter, Depends, UploadFile, File
from fastapi_users import FastAPIUsers
from sqlalchemy import Integer
from sqlalchemy.orm import Session
import crud
from auth_dict.auth import auth_backend
from models.models import User
from auth_dict.manager import get_user_manager
from models.models import get_db
from tags import tag_shemas

fastapi_users = FastAPIUsers[User, Integer](
    get_user_manager,
    [auth_backend],
)

router_tags = APIRouter(
    prefix='/tags',
    tags=['Tags']
)

current_user = fastapi_users.current_user()


@router_tags.post('/get_geo')
def read_geo(map_geo: tag_shemas.MapGeo, db: Session = Depends(get_db)):
    db_geo = crud.get_geo(map_geo=map_geo, db=db)
    return db_geo


@router_tags.post('/catch/almost whole')
async def create_catch(catch: tag_shemas.CatchCreate = Depends(), files: list[UploadFile] = File(...),
                       user: User = Depends(current_user),
                       db: Session = Depends(get_db)):
    if not files:
        return {"message": "No upload file sent"}
    for file in files:
        if file.content_type != "image/jpeg":
            return {"message": 'incorrect file'}
    return crud.create_test(db=db, uploaded_file=files, id=user.id, catch=catch)


@router_tags.delete('photo/delete')
def delete_photo(tags_id: int, photo_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)):
    return crud.delete_photo(tags_id=tags_id, photo_id=photo_id, user_id=user.id, db=db)

