# from typing import List
#
# from fastapi import APIRouter, Depends, Response
# from sqlalchemy.orm import Session
#
# from ..database import crud
# from ..exception.handler import handler
# from ..schema import schemas
# from ..database.conn import db
#
#
# router = APIRouter()
#
#
# @router.post("/users/", response_model=schemas.User)
# async def create_user(user: schemas.UserCreate, res: Response, db: Session = Depends(db.get_db)):
#     db_user = crud.get_user_by_email(db, email=user.email)
#     res.status_code = 201
#     if db_user:
#         handler.code(400)
#     return crud.create_user(db=db, user=user)
#
#
# @router.get("/users/", response_model=List[schemas.User])
# async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users
#
#
# @router.get("/users/{user_id}", response_model=schemas.User)
# async def read_user(user_id: int, db: Session = Depends(db.get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         handler.code(404)
#     return db_user
#
#
# @router.post("/users/{user_id}/items/", response_model=schemas.Item)
# async def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(db.get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
#
#
# @router.get("/items/", response_model=List[schemas.Item])
# async def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(db.get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
