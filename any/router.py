from fastapi import APIRouter, Depends, UploadFile
from fastapi_users import FastAPIUsers
from sqlalchemy import Integer
from sqlalchemy.orm import Session
import crud
from auth_dict.auth import auth_backend
from models.models import User
from auth_dict.manager import get_user_manager
from models.models import get_db
from tags import tag_shemas

router_any = APIRouter(
    prefix='/any',
    tags=['any']
)


@router_any.post("/description/", response_model=tag_shemas.Description)
def create_description(description: tag_shemas.DescriptionCreate, user_id: int, db: Session = Depends(get_db)):
    return crud.create_description(db=db, description=description, user_id=user_id)


@router_any.post("/tag/", response_model=tag_shemas.Tag)
def create_tag(tag: tag_shemas.TagCreate, db: Session = Depends(get_db)):
    return crud.create_tag(db=db, tag=tag)
