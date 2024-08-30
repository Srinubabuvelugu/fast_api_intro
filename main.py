from enum import Enum
from fastapi import FastAPI,Query
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/",description="This the first api get route")
async def root():
    return {"message":"Hello from get"}

@app.post("/")
async def post():
    return {"message":"Hello from post"}

@app.put("/")
async def put():
    return {"message":"Hello from put"}

##  PAth parameters

@app.get("/users")
async def list_iusers():
    return {"message":"list of iusers route"}

@app.get("/users/me")
async def get_current_user():
    return {"message":"This is the current user"}

@app.get("/users/{user_id}")
async def get_item(user_id: int):
    return {"user_id":user_id}


class FoodEnum(str,Enum):
    fruits = "fruits"
    vegtables = "vegtables"
    dairy = "dairy"

@app.get("/foods/{food_name}")
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegtables:
        return {"food_name":food_name,"message":"you are healthy"}
    
    if food_name.value =="fruits":
        return {
            "food_name" :food_name,
            "message":"You are still healthy, but like sweet things"
        }
    return {
        "foof_name":food_name,
        "message":"I Like chocolate milk"
    }
## query parameters

fake_items_db = [
    {"item_name": "Bist"},
    {"item_name": "Regular"},
    {"item_name": "Buzz"},
    {"item_name": "Rock"},
    {"item_name": "Pop"},
    {"item_name": "Drum"}
]

@app.get("/itemslist")
async def list_items(skip: int=0, limit: int = 5):
    return fake_items_db[skip : skip + limit]

## implementing with the optional parameters
@app.get("/itemslist/{item_id}")
async def get_item(item_id:str, q: Optional[str] = None, short: bool=False):
    item = {"item_id":item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {"discription":"Here q:none and Shot:False"}
        )
    return item

@app.get("/users/{user_id}/itemslist/{item_id}")
async def get_user_item(user_id:int, item_id:str, q: Optional[str] = None, short: bool=False):
    item = {"user_id":user_id, "item_id":item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {"discription":"Here q:none and Shot:False"}
        )
    return item

## body request
class Item(BaseModel):
    name: str
    discription: Optional[str] = None  # making the parameter as optional or 
    price: float
    tax: Optional[float] = None  # by this also we can make as parameter as optinal (i.e it is works if the python version is below 3.5)

@app.post("/items")
async def items(item:Item):
    return item

## video5 query parameters and String validation
@app.get("/items2")
async def read_items(q:Optional[str] = Query(default="fixedquery",min_length=3, max_length=10,regex="^fi")):
    result = {
        "items":[
            {"item_id":"Foo"},
            {"item_id":"Bar"}
        ]
    }
    if q:
        result.update({"q":q})
    return result