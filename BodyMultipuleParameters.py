from fastapi import (
    FastAPI,
    Path,
    Body,
)
from pydantic import BaseModel
from typing import Optional

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