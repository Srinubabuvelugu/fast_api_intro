from fastapi import (
    FastAPI,
    Path,
    Body,
)
from typing import Optional,List,Set
from pydantic import BaseModel,Field,HttpUrl

app = FastAPI()

## video 7 - Body -Multiple parameters
class Item(BaseModel):
    name: str
    description:Optional[str] = None
    price: float
    tax: Optional[float] = None

class User(BaseModel):
    username: str
    full_name: Optional[str] = None

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(...,title="The id of the item to get", ge=0, le=150),
    q:Optional[str] = None,
    item: Optional[Item] = None,
    user: User,
    importance: int = Body(...)
):
    results = {"item_id":item_id}
    if q:
        results.update({"q":q})
    if item:
        results.update({"item":item})
    if user:
        results.update({"user": user})
    if importance:
        results.update({"importance":importance})
    return results


# ## video - 8 Body Fields
class Item(BaseModel):
    name: str
    description: Optional[str] = Field(None, title = "This idescription of item", max_lenagth = 300)
    price: float = Field(...,gt=0,description = "This price must be greater than zero")
    tax:Optional[float] = None
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item =Body(...,embed= True) ):
    results = {"item_id":item_id, "item":item}
    return results


## video - 9 Body- Nested Models
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()
    image: List[Image] = None

class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]

@app.put("/items/{item_id}")
async def update_item(item_id: int, item:Item):
    result = {"item_id":item_id,"item":item}
    return result

@app.post("/offers")
async def create_offer(offer : Offer = Body(...,embed=True)):
    return offer