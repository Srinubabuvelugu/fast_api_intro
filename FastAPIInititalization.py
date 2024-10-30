from enum import Enum
from fastapi import FastAPI


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