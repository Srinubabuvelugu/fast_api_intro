from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from typing import Optional,List
from pydantic import BaseModel

app = FastAPI()

## video - 21 - JSON Compatible encoder and Body
fake_db = {}

class Item(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    tax: float= 10.6
    tags: List[str] = list()

items = {
    "foo": {"name":"Foo", "Description": "This is Foo Item", "price":150},
    "bar": {
        "name":"Bar", 
        "description":"The barteners", 
        "price":2000, 
        "tax":12.5
    },
    "baz":{
        "name":"Baz",
        "description":None,
        "price":100,
        "tax":5.5,
        "tags":["items","users"]
    },
}

@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id:str):
    return items.get(item_id)

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id:str, item: Item):
    update_item_encoded = jsonable_encoder(item)
    items[item_id] = update_item_encoded
    return update_item_encoded

@app.patch("/items/{item_id}", response_model=Item)
async def patch_item(item_id: str, item:Item):
    stored_item_data = items.get(item_id)
    if stored_item_data is not None:
        stored_item_model = Item(**stored_item_data)
    else:
        stored_item_model = Item()
    # print(stored_item_model)
    update_data = item.dict(exclude_unset=True)
    updated_item = stored_item_model.copy(update=update_data)
    items[item_id] = jsonable_encoder(updated_item)
    print(items[item_id])
    return updated_item
