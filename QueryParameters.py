from fastapi import (
    FastAPI,
    Query, 
    Path,
)
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

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
async def read_items(q: list =Query(default=['hi','hello'],min_length=1, max_length=10,title='Simple query string',alias="query_item")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#hidden query
@app.get("/hidden_query")
async def hidden_query(q: Optional[str] = Query(None,include_in_schema=False)):
    if q:
        return {"q":q}
    return {"q":"Not Found"}

## video 6-  Queruy parameters and Numeric Validation
@app.get("/items_validation/{item_id}")
async def read_items_validation(
        q: str,
        item_id:int = Path(dafault = (...),title = "The ID of the item to get")
           
    ):
    result = {"item_id":item_id}
    if q:
        result.update({"q":q})
    return result
