from enum import Enum
from fastapi import (
    FastAPI,
    Body,
    Header, 
    Depends,
)
from fastapi.exceptions import HTTPException
from typing import Optional


app = FastAPI()


## video - 22 - Dependencies Intro
async def hello():
    return "World"
async def common_parameters(q: Optional[str] = None, skip:int=0, limit:int=100, blah: str = Depends(hello)):
    return {"q":q, "skip":skip,"limit":limit, "hello":blah}

@app.get("/items/")
async def read_items(commons:dict = Depends(common_parameters)):
    return commons

@app.get("/users/")
async def read_users(commons:dict = Depends(common_parameters)):
    return commons.q

#video - 23 - Classes as Dependencies
fake_items_db = [
    {"item_name":"Foo"}, 
    {"item_name":"Bar"}, 
    {"item_name":"Baz"},
    {"item_name":"Poo"},
    {"item_name":"Raa"},
]

class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, skip: int= 0, limit: int= 100):
        self.q = q 
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q":commons.q})
    items = fake_items_db[commons.skip: commons.skip + commons.limit]
    response.update({"items":items})
    return response

#video - 24 - Sub Dependecies
def query_extractor(q: Optional[str] = None):
    return q

def query_or_body_extractior(
    q: str = Depends(query_extractor),
    last_query: Optional[str] = Body(None)
):
    if q:
        return q
    return last_query
@app.post("/items/")
async def try_query(query_or_body: str = Depends(query_or_body_extractior)):
    return {"query_or_body":query_or_body}

# video - 25 - Dependencies in Path Operation Decorators
async def verify_token(x_token: str = Header(...)):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-token header invalid")
    return x_token

async def verify_key(x_key:str = Header(...)):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code= 400, detail="X-Key header invalid")
    return x_key

@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items(blah:str = Depends(verify_key)):
    return [{"item":"Foo"}, {"item":"Bar"}, {"X_key":blah}]
