from typing import Annotated, Optional

from pydantic import BaseModel


# Схемы для модели Geo, чтение, загрузка, полное чтение
class GeoBase(BaseModel):
    coordinates_n: float
    coordinates_e: float


class GeoCreate(GeoBase):
    coordinates_n: float
    coordinates_e: float

    class Config:
        orm_mode = True


class Geo(GeoBase):
    id: int

    class Config:
        orm_mode = True


class MapGeo(BaseModel):
    left_up_coordinates_n: float = 56.05261
    left_up_coordinates_e: float = 35.95288
    right_down_coordinates_n: float = 55.10487
    right_down_coordinates_e: float = 38.73244

    class Config:
        orm_mode = True


# Схемы для модели Tags, чтение, загрузка, полное чтение
class TagBase(BaseModel):
    geo_id: int
    user_id: int
    description_id: int


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int

    class Config:
        orm_mode = True


class DescriptionBase(BaseModel):
    description: str


class DescriptionCreate(DescriptionBase):
    pass


class Description(DescriptionBase):
    description: str

    class Config:
        orm_mode = True


class PhotoBase(BaseModel):
    tags_id: int
    description_id: int

    class Config:
        orm_mode = True


class CatchCreate(BaseModel):
    coordinates_n: float
    coordinates_e: float
    description: str

    # user_id: int = 9

    class Config:
        orm_mode = True


class CatchBase(CatchCreate):
    description_id: int
    geo_id: int
    user_id: int

    class Config:
        orm_mode = True
