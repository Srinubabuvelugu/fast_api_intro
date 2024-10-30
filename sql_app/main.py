from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import *


app = FastAPI()
models.Base.metadata.create_all(bind= engine)

#Dependencies
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model= schemas.User,status_code=201)
async def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email = user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already regidtred")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
async def read_user (skip: int = 0, limit: int =100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip= skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model = schemas.User)
async def read_user(user_id: int, db:Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id = user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=" User not found")
    return db_user

@app.post("/users/{user_id}/items/", response_model = schemas.Item, status_code=201)
async def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.cerate_user_item(db, item=item, user_id=user_id)

@app.get("/items/", response_model=List[schemas.Item])
async def read_items(skip: int = 0, limit: int =100, db: Session = Depends(get_db)):
    items = crud.get_items(db,skip=skip, limit=limit)
    return items

# @app.delete("/items/{user_id}/delete",response_model=schemas.Item, status_code=200)
# async def delete_user_items(user_id: int, db: Session= Depends(get_db)):
#     del_user_items = crud.delete_user_items(db,user_id=user_id)
#     return del_user_items

@app.delete("/items/{item_id}/delete",response_model=schemas.Item, status_code=200)
async def delete_item(item_id: int, db: Session= Depends(get_db)):
    del_item = crud.delete_item(db,item_id=item_id)
    print(del_item)
    if del_item is None:
        print("hello")
        return HTTPException(status_code=404, detail="Items Not Found")
    db.delete(del_item)
    db.commit()
   
    return del_item