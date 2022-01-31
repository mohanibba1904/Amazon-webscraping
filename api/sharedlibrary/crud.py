from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_name(db: Session, user_name: str):
    return db.query(models.User).filter(models.User.user_name == user_name).first()


def get_movie_id(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first() 


# def like_a_join(db: Session, movie_id: int,user_id: int):
#     movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first() 
#     user = db.query(models.User).filter(models.User.id == user_id).first()
#     return [movie, user]       