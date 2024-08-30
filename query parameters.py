## query parameters

fake_items_db = [
    {"item_name": "Bist"},
    {"item_name": "Regular"},
    {"item_name": "Buzz"},
    {"item_name": "Rock"},
    {"item_name": "Pop"},
    {"item_name": "Drum"}
]

@app.get("/items")
async def list_items(skip: int=0, limit: int = 5):
    return fake_items_db[skip : skip + limit]

## implementing with the optional parameters
@app.get("/items/{item_id}")
async def get_item(item_id:str, q: Optional[str] = None, short: bool=False):
    item = {"item_id":item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {"discription":"Here q:none and Shot:False"}
        )
    return item

@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(user_id:int, item_id:str, q: Optional[str] = None, short: bool=False):
    item = {"user_id":user_id, "item_id":item_id}
    if q:
        item.update({"q":q})
    if not short:
        item.update(
            {"discription":"Here q:none and Shot:False"}
        )
    return item