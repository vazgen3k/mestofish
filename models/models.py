from datetime import datetime
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import MetaData, Integer, String, ForeignKey, Column, \
    DateTime, Boolean, create_engine, FLOAT, Index, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, expire_on_commit=False, autoflush=False, bind=engine)

metadata = MetaData()
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    last_name = Column(String(50))
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    datetime = Column(DateTime(), default=datetime.now, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    tags = relationship('Tags', backref='users', cascade='all, delete')
    descriptions = relationship('Descriptions', backref='users', cascade='all, delete')


class Geo(Base):
    __tablename__ = 'geo'
    id = Column(Integer, primary_key=True)
    coordinates_n = Column(DECIMAL(5, 7), nullable=False)
    coordinates_e = Column(DECIMAL(5, 7), nullable=False)
    tags = relationship('Tags', backref='tags', cascade='all, delete')


class Descriptions(Base):
    __tablename__ = 'description'
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    datetime = Column(DateTime(), default=datetime.now, nullable=False)
    user_id = Column(Integer, ForeignKey('profile.id'))
    tags = relationship('Tags', backref='description', uselist=False)
    photos = relationship('Photos', backref='description', cascade='all, delete')


class Tags(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    geo_id = Column(Integer, ForeignKey('geo.id'))
    user_id = Column(Integer, ForeignKey('profile.id'))
    description_id = Column(Integer, ForeignKey('description.id'))
    photos = relationship('Photos', backref='tag', cascade='all, delete')


class Photos(Base):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    photo_url = Column(String, nullable=False)
    tags_id = Column(Integer, ForeignKey('tag.id'))
    description_id = Column(Integer, ForeignKey('description.id'))
