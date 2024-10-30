from fastapi import FastAPI
from typing import Optional,List, Literal, Union
from pydantic import BaseModel, EmailStr

app = FastAPI()

## video-13 -Responce Model
class Item(BaseModel):
    name:str
    description:Optional[str] = None
    price: float
    tax:float = 10.5
    togs: List[str] = []

items = {
    "foo": {"name":"Foo","price":25},
    "bar": {"name":"Bar","description":"this is Bar Item", "price":215,"tax":25},
    "baz": {"name":"Baz", "description":"This is a Baz item","price":150, "tax":15, "tags":[]}
}
@app.post("/items/{item_id}",response_model=Item,response_model_exclude_unset=True)
async def read_item(item_id:Literal["foo", "bar", "baz"]):
    return items[item_id]

@app.post("/items/{item_id}/private/",response_model=Item,response_model_include={"name","description"})
async def read_item_private(item_id:Literal["foo", "bar", "baz"]):
    return items[item_id]

@app.post("/items/{item_id}/public/",response_model=Item,response_model_exclude={"tax","price"})
async def read_item_public(item_id:Literal["foo", "bar", "baz"]):
    return items[item_id]

class UserBase(BaseModel):
    username:str
    email: EmailStr
    full_name:Optional[str] = None

class UserIn(UserBase):
    password:str
   
class UserOut(UserBase):
    pass

@app.post("/user/",response_model = UserOut)
async def crete_user(user:UserIn):
    return user

## video - 14 - Extra Models
class UserBase(BaseModel):
    username:str
    email:EmailStr
    full_name: Optional[str] = None

class UserIn(UserBase):
    password:str

class UserOut(UserBase):
    pass
class UserInDB(UserBase):
    hashed_password:str

def fake_password_hasher(raw_password:str):
    return f"supersecret{raw_password}"
def fake_save_user(user_in:UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password= hashed_password)
    print("user saved")
    return user_in_db

@app.post("/user/",response_model=UserOut)
async def create_user(user_in:UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

class BaseItem(BaseModel):
    description: str
    type:str
class CarItem(BaseItem):
    type = "car"
class PlaneItem(BaseItem):
    type = "plane"
    size : int

items = {
    "item1": {"description":"All my friends drive slowly", "type":"Car"},
    "item2": {"description":"I like to drive airzets", "type":"Plane", "size":19}
}

@app.get("/items/{item_id}/", response_model= Union[PlaneItem, CarItem])
async def read_items(item_id:Literal["item1","item2"]):
    return items[item_id]

class ListItems(BaseModel):
    name: str
    description:str

list_items = [
    {"name":"Foo", "description":"This is Foo Item"},
    {"name":"Bar", "description":"This is a Bar item"},
]

@app.get("/list_items/",response_model=List[ListItems])
async def read_items():
    return items