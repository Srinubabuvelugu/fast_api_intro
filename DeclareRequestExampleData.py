from fastapi import (
    FastAPI,
    Body
)
from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime,time, timedelta


app = FastAPI()

## video - 10 - Declare request Example Data
class Item(BaseModel):
    name: str 
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    # to set the defualt values for basemodel item
    # class Config:
    #     json_schema_extra ={
    #         "example":{
    #             "name":"fufoo",
    #             "description": "A very nice item",
    #             "price": 46,
    #             # "tax":2.5
    #         }
    #     }

@app.put("/items/{item_id}")
async def update_item(
    item_id:int, 
    item:Item = Body(
        ...,
        examples={
            "normal":{
                "name":"fufoo",
                "description":"A very nice item",
                "price":15,
                "tax":1.5,
            },
            "converted":{
                "summary":"An example with converted data",
                "description":"FastAPI can convert price 'strings to normal form",
                "value":{"name":"buboo", "price":"15.65"},

            },
            "invalid":{
                "summary":"Invalid data is rejected eit an error",
                "description":"Hello learner",
                "value":{"name":"Pupoo","price":"fifteen point six five"},
            },
        },
    )
):
    results = {"item_id":item_id,"item":item}
    return results

## video -11 - Extra data types
@app.put("/items/{item_id}")
async def read_items(
    item_id:UUID, 
    start_date: Optional[datetime]=Body(None),
    end_date:Optional[datetime]=Body(None),
    repeat_at:Optional[time]=Body(None),
    process_after: Optional[timedelta] = Body(None)
    ):

    start_process = start_date + process_after
    duration = end_date - start_process

    return {
        "item_id":item_id,
        "start_date":start_date,
        "end_date":end_date,
        "repeat_at":repeat_at,
        "process_after":process_after,
        "start_process":start_process,
        "duration":duration,
        }
