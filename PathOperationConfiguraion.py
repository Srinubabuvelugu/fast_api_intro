from enum import Enum
from fastapi import (
    FastAPI, 
    status
)
from typing import Optional,Set
from pydantic import BaseModel

app = FastAPI()

##  video - 20 - Path Operation Confiuguration
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()

class Tags(Enum):
    items = "items"
    users = "users"


@app.post(
    "/items/", 
    response_model=Item, 
    status_code=status.HTTP_201_CREATED, 
    tags=[Tags.items],
    summary=" Create an Item",
    # description="Create an item with all the information:"
    #     "name; description; price; tax; and a set of unique tags",
    response_description="The Item created"
)
async def created_item(item: Item):
    """
    Create an item with all insformation:
    - **name**: Each item have a name
    - **description**: E long serciption
    - **price**: Required
    - **tax**: If the item deosn't have tax, you can omit this
    - **tags**: A set of unique tag strings for this item
    """
    return item

@app.get("/items",tags=[Tags.items, Tags.users])
async def read_items():
    return [{"name":"Foo", "price":45}]

@app.get("/users/", tags=[Tags.users])
async def read_users():
    return [{"username":"Srinubabu"}]

@app.get("/elements/", tags=[Tags.items],deprecated=True)
async def create_elements(element_id: str = "Foo"):
    return {"Element":element_id}
