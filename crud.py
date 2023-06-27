import shutil

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

import tags.tag_shemas
from models.models import Photos, Tags, Descriptions
from tags import tag_shemas
from models import models


def get_geo(map_geo: tags.tag_shemas.MapGeo, db: Session):
    stmt = select(models.Geo).where(map_geo.left_up_coordinates_n > models.Geo.coordinates_n,
                                    models.Geo.coordinates_n > map_geo.right_down_coordinates_n,
                                    map_geo.right_down_coordinates_e > models.Geo.coordinates_e,
                                    models.Geo.coordinates_e > map_geo.left_up_coordinates_e)
    result = []
    for geo_obj in db.execute(stmt):
        result += geo_obj
    return result


def create_geo_and_description(db, catch, id):
    db_geo = models.Geo(coordinates_n=catch.coordinates_n, coordinates_e=catch.coordinates_e)
    db_description = models.Descriptions(description=catch.description, user_id=id)
    db.add_all([db_geo, db_description])
    db.commit()
    db.refresh(db_geo)
    db.refresh(db_description)
    b = {'description_id': db_description.id, 'geo_id': db_geo.id}
    return b


def create_tag_new(db, geo_and_description, id):
    db_tag = models.Tags(description_id=geo_and_description['description_id'], geo_id=geo_and_description['geo_id'],
                         user_id=id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag.id


def create_image(db, uploaded_file, tag_id, geo_and_description):
    for file in uploaded_file:
        file_location = rf"C:\Users\v/{file.filename}"
        with open(file_location, 'wb+') as file_object:
            shutil.copyfileobj(file.file, file_object)
            db_photo = models.Photos(tags_id=tag_id, description_id=geo_and_description['description_id'],
                                     photo_url=file_location)
            db.add(db_photo)
        db.commit()
    return {'Ok'}


def create_test(db: Session, uploaded_file, id, catch: tag_shemas.CatchCreate):
    geo_and_description = create_geo_and_description(db, catch, id)
    tag_id = create_tag_new(db, geo_and_description, id)
    create_image(db, uploaded_file, tag_id, geo_and_description)
    return {'OOOOOkkkk'}


def get_tags(tags_id, db):
    return db.query(Tags).filter(Tags.id == tags_id)


def delete_tags_desc(tags_id, user_id, desc_id, db):
    tag = get_tags(tags_id, db)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tags not found")
    else:
        db.query(Tags).filter(Tags.id == tags_id, Tags.user_id == user_id).delete()
        db.query(Descriptions).filter(Descriptions.id == desc_id).delete()
        db.flush()
        db.commit()
    return desc_id

# функция получения id описания по id фотографии
def get_desc(photo_id, db):
    return db.query(Photos).filter(Photos.id == photo_id).first()


# функция получения фотографии по id
def get_photo(photo_id, db):
    return db.query(Photos).filter(Photos.id == photo_id).first()


# возвращаем количество записей с этим тегом
def count_tags_in_photo(tags_id, db):
    return db.query(Photos).filter(Photos.tags_id == tags_id).count()


# удаляем фото
def delete_photo(tags_id, photo_id, user_id, db):
    photo = get_photo(photo_id, db)  # ищем фото
    if photo is None:
        raise HTTPException(status_code=404, detail="Photo not found")
    # если осталась одна фотография с этим тегом, запрещаем удаление. (Мой каприз)
    else:
        db.query(Photos).filter(Photos.id == photo_id, Tags.id == tags_id, Tags.user_id == user_id).delete()
        db.flush()
        db.commit()
    tags_count = count_tags_in_photo(tags_id, db)  # вызываем функции проверки
    if tags_count == 0:
        desc_id = photo.description_id
        return delete_tags_desc(tags_id, user_id, desc_id, db)
    else:
        return {'Okay'}


