##You can reffere this  youtube channel for all about FastAPI - https://www.youtube.com/@JVPDesign



from enum import Enum
from fastapi import (
    BackgroundTasks,
    FastAPI,
    Query, 
    Path,
    Body,
    Cookie,
    Header, 
    status, 
    Form, 
    File, 
    UploadFile,
    Depends,
)
from fastapi import HTTPException,Request
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from typing import Optional,List,Set, Literal, Union
import regex
from pydantic import BaseModel,Field,HttpUrl, EmailStr
from uuid import UUID
import time
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext
from jose import JWTError, jwt

app = FastAPI()

# @app.get("/",description="This the first api get route")
# async def root():
#     return {"message":"Hello from get"}

# @app.post("/")
# async def post():
#     return {"message":"Hello from post"}

# @app.put("/")
# async def put():
#     return {"message":"Hello from put"}

# ##  PAth parameters

# @app.get("/users")
# async def list_iusers():
#     return {"message":"list of iusers route"}

# @app.get("/users/me")
# async def get_current_user():
#     return {"message":"This is the current user"}

# @app.get("/users/{user_id}")
# async def get_item(user_id: int):
#     return {"user_id":user_id}


# class FoodEnum(str,Enum):
#     fruits = "fruits"
#     vegtables = "vegtables"
#     dairy = "dairy"

# @app.get("/foods/{food_name}")
# async def get_food(food_name: FoodEnum):
#     if food_name == FoodEnum.vegtables:
#         return {"food_name":food_name,"message":"you are healthy"}
    
#     if food_name.value =="fruits":
#         return {
#             "food_name" :food_name,
#             "message":"You are still healthy, but like sweet things"
#         }
#     return {
#         "foof_name":food_name,
#         "message":"I Like chocolate milk"
#     }
# ## query parameters

# fake_items_db = [
#     {"item_name": "Bist"},
#     {"item_name": "Regular"},
#     {"item_name": "Buzz"},
#     {"item_name": "Rock"},
#     {"item_name": "Pop"},
#     {"item_name": "Drum"}
# ]

# @app.get("/itemslist")
# async def list_items(skip: int=0, limit: int = 5):
#     return fake_items_db[skip : skip + limit]

# ## implementing with the optional parameters
# @app.get("/itemslist/{item_id}")
# async def get_item(item_id:str, q: Optional[str] = None, short: bool=False):
#     item = {"item_id":item_id}
#     if q:
#         item.update({"q":q})
#     if not short:
#         item.update(
#             {"discription":"Here q:none and Shot:False"}
#         )
#     return item

# @app.get("/users/{user_id}/itemslist/{item_id}")
# async def get_user_item(user_id:int, item_id:str, q: Optional[str] = None, short: bool=False):
#     item = {"user_id":user_id, "item_id":item_id}
#     if q:
#         item.update({"q":q})
#     if not short:
#         item.update(
#             {"discription":"Here q:none and Shot:False"}
#         )
#     return item

# ## body request
# class Item(BaseModel):
#     name: str
#     discription: Optional[str] = None  # making the parameter as optional or 
#     price: float
#     tax: Optional[float] = None  # by this also we can make as parameter as optinal (i.e it is works if the python version is below 3.5)

# @app.post("/items")
# async def items(item:Item):
#     return item

# ## video5 query parameters and String validation
# @app.get("/items2")
# async def read_items(q: list =Query(default=['hi','hello'],min_length=1, max_length=10,title='Simple query string',alias="query_item")):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results

# #hidden query
# @app.get("/hidden_query")
# async def hidden_query(q: Optional[str] = Query(None,include_in_schema=False)):
#     if q:
#         return {"q":q}
#     return {"q":"Not Found"}

# ## video 6-  Queruy parameters and Numeric Validation
# # @app.get("/items_validation/{item_id}")
# # async def read_items_validation(
# #         q: str,
# #         item_id:int = Path(dafault = (...),title = "The ID of the item to get")
           
# #     ):
# #     result = {"item_id":item_id}
# #     if q:
# #         result.update({"q":q})
# #     return result/

## video 7 - Body -Multiple parameters
# class Item(BaseModel):
#     name: str
#     description:Optional[str] = None
#     price: float
#     tax: Optional[float] = None

# class User(BaseModel):
#     username: str
#     full_name: Optional[str] = None

# @app.put("/items/{item_id}")
# async def update_item(
#     *,
#     item_id: int = Path(...,title="The id of the item to get", ge=0, le=150),
#     q:Optional[str] = None,
#     item: Optional[Item] = None,
#     user: User,
#     importance: int = Body(...)
# ):
#     results = {"item_id":item_id}
#     if q:
#         results.update({"q":q})
#     if item:
#         results.update({"item":item})
#     if user:
#         results.update({"user": user})
#     if importance:
#         results.update({"importance":importance})
#     return results


# ## video - 8 Body Fields
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = Field(None, title = "This idescription of item", max_lenagth = 300)
#     price: float = Field(...,gt=0,description = "This price must be greater than zero")
#     tax:Optional[float] = None
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item =Body(...,embed= True) ):
#     results = {"item_id":item_id, "item":item}
#     return results


## video - 9 Body- Nested Models
# class Image(BaseModel):
#     url: HttpUrl
#     name: str

# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: Set[str] = set()
#     image: List[Image] = None

# class Offer(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     items: List[Item]

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item:Item):
#     result = {"item_id":item_id,"item":item}
#     return result

# @app.post("/offers")
# async def create_offer(offer : Offer = Body(...,embed=True)):
#     return offer

## video - 10 - Declare request Example Data
# class Item(BaseModel):
#     name: str 
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     # to set the defualt values for basemodel item
#     # class Config:
#     #     json_schema_extra ={
#     #         "example":{
#     #             "name":"fufoo",
#     #             "description": "A very nice item",
#     #             "price": 46,
#     #             # "tax":2.5
#     #         }
#     #     }

# @app.put("/items/{item_id}")
# async def update_item(
#     item_id:int, 
#     item:Item = Body(
#         ...,
#         examples={
#             "normal":{
#                 "name":"fufoo",
#                 "description":"A very nice item",
#                 "price":15,
#                 "tax":1.5,
#             },
#             "converted":{
#                 "summary":"An example with converted data",
#                 "description":"FastAPI can convert price 'strings to normal form",
#                 "value":{"name":"buboo", "price":"15.65"},

#             },
#             "invalid":{
#                 "summary":"Invalid data is rejected eit an error",
#                 "description":"Hello learner",
#                 "value":{"name":"Pupoo","price":"fifteen point six five"},
#             },
#         },
#     )
# ):
#     results = {"item_id":item_id,"item":item}
#     return results

## video -11 - Extra data types
# @app.put("/items/{item_id}")
# async def read_items(
#     item_id:UUID, 
#     start_date: Optional[datetime]=Body(None),
#     end_date:Optional[datetime]=Body(None),
#     repeat_at:Optional[time]=Body(None),
#     process_after: Optional[timedelta] = Body(None)
#     ):

#     start_process = start_date + process_after
#     duration = end_date - start_process

#     return {
#         "item_id":item_id,
#         "start_date":start_date,
#         "end_date":end_date,
#         "repeat_at":repeat_at,
#         "process_after":process_after,
#         "start_process":start_process,
#         "duration":duration,
#         }

## video - 12- cookie and header Parameters
# @app.put("/items")
# async def read_items(
#     cookie_id:Optional[str]=Cookie(None),
#     accept_encoding: Optional[str] = Header(None),
#     see_ch_ua: Optional[str] = Header(None),
#     user_agent: Optional[str] = Header(None),
#     x_token: Optional[List[str]] = Header(None)
# ):
#     return {"cookie_id":cookie_id,
#             "Accept-Encoding":accept_encoding,
#             "sec-ch-ua":see_ch_ua,
#             "User-Agent":user_agent,
#             "X-token-values":x_token,
#             }

## video-13 -Responce Model
# class Item(BaseModel):
#     name:str
#     description:Optional[str] = None
#     price: float
#     tax:float = 10.5
#     togs: List[str] = []

# items = {
#     "foo": {"name":"Foo","price":25},
#     "bar": {"name":"Bar","description":"this is Bar Item", "price":215,"tax":25},
#     "baz": {"name":"Baz", "description":"This is a Baz item","price":150, "tax":15, "tags":[]}
# }
# @app.post("/items/{item_id}",response_model=Item,response_model_exclude_unset=True)
# async def read_item(item_id:Literal["foo", "bar", "baz"]):
#     return items[item_id]

# @app.post("/items/{item_id}/private/",response_model=Item,response_model_include={"name","description"})
# async def read_item_private(item_id:Literal["foo", "bar", "baz"]):
#     return items[item_id]

# @app.post("/items/{item_id}/public/",response_model=Item,response_model_exclude={"tax","price"})
# async def read_item_public(item_id:Literal["foo", "bar", "baz"]):
#     return items[item_id]

# class UserBase(BaseModel):
#     username:str
#     email: EmailStr
#     full_name:Optional[str] = None

# class UserIn(UserBase):
#     password:str
   
# class UserOut(UserBase):
#     pass

# @app.post("/user/",response_model = UserOut)
# async def crete_user(user:UserIn):
#     return user

## video - 14 - Extra Models
# class UserBase(BaseModel):
#     username:str
#     email:EmailStr
#     full_name: Optional[str] = None

# class UserIn(UserBase):
#     password:str

# class UserOut(UserBase):
#     pass
# class UserInDB(UserBase):
#     hashed_password:str

# def fake_password_hasher(raw_password:str):
#     return f"supersecret{raw_password}"
# def fake_save_user(user_in:UserIn):
#     hashed_password = fake_password_hasher(user_in.password)
#     user_in_db = UserInDB(**user_in.dict(), hashed_password= hashed_password)
#     print("user saved")
#     return user_in_db

# @app.post("/user/",response_model=UserOut)
# async def create_user(user_in:UserIn):
#     user_saved = fake_save_user(user_in)
#     return user_saved

# class BaseItem(BaseModel):
#     description: str
#     type:str
# class CarItem(BaseItem):
#     type = "car"
# class PlaneItem(BaseItem):
#     type = "plane"
#     size : int

# items = {
#     "item1": {"description":"All my friends drive slowly", "type":"Car"},
#     "item2": {"description":"I like to drive airzets", "type":"Plane", "size":19}
# }

# @app.get("/items/{item_id}/", response_model= Union[PlaneItem, CarItem])
# async def read_items(item_id:Literal["item1","item2"]):
#     return items[item_id]

# class ListItems(BaseModel):
#     name: str
#     description:str

# list_items = [
#     {"name":"Foo", "description":"This is Foo Item"},
#     {"name":"Bar", "description":"This is a Bar item"},
# ]

# @app.get("/list_items/",response_model=List[ListItems])
# async def read_items():
#     return items

## video - 15 - Response Status Codes
# # created http status code 201
# @app.post("/items/",status_code=status.HTTP_201_CREATED)
# async def create_item(name:str):
#     return {"name":name}

# # no content status code 204
# @app.delete("/items/{pk}",status_code=status.HTTP_204_NO_CONTENT)
# async def delete_item(pk:str):
#     print("pk", pk)
#     return pk

# @app.get("/items/",status_code=status.HTTP_305_USE_PROXY)
# async def read_items_redirect():
#     return {"hello":"world"}

## video - 16 - Form Fields
# @app.post("/login/")
# async def login(username:str = Form(...), password:str = Form(...)):
#     return {"username":username, "password":password}

# class User(BaseModel):
#     username: str
#     password: str

# @app.post("/login-json/")
# async def login_json(user:User):
#     return user

## video -17 - Request Files
# @app.post("/files/")
# async def create_file(file:bytes = File(...)):
#     return {"file length" :len(file)}

# @app.post("/uploadfile/")
# async def create_file(file: UploadFile):
#     return {"file name" :file.filename}

## video - 18 - Request Forms and Files
# @app.post("/files/")
# async def create_file(
#     file:bytes = File(...), 
#     fileb:UploadFile = File(...), 
#     token:str = Form(...),
#     hello:str = Body(...)
# ):
#     return {
#         "file_size": len(file),
#         "token":token,
#         "file_content_type" : fileb.content_type,
#         "helo":hello
#     }

## video -19 - Handling Errors
# items = {
#     "foo":"the Foo wrestlers"
# }
# @app.get("/items/{item_id}")
# async def read_item(item_id:str):
#     if item_id not in items:
#         raise HTTPException(
#             status_code=404,
#             detail = "Item not found", 
#             headers={"X-Error":"There goes my error"},
#         )
#     return {"item":items[item_id]}

# class UnicornException(Exception):
#     def __init__(self, name:str) -> None:
#         self.name = name

# @app.exception_handler(UnicornException)
# async def unicorn_exception_handler(request:Request, exc: UnicornException):
#     return JSONResponse(
#         status_code= 418,
#         content = {"message":f"Oops {exc.name} did something. There goes a rainbow..."}
#     )

# @app.get("/unicorn/{name}")
# async def read_unicorns(name:str):
#     if name == "yolo":
#         raise UnicornException(name=name)
#     return {"unicorn_name":name}

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handeler(request,exc):
#     return PlainTextResponse(str(exc),status_code=400)

# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request,exc):
#     return PlainTextResponse(str(exc.detail),status_code=exc.status_code)

# @app.get("/validation_items/{item_id}")
# async def read_validation_items(item_id:int):
#     if item_id == 3:
#         raise HTTPException(status_code = 418,detail="Nope! I don't like 3.")
#     return {"item_id":item_id}

# @app.exception_handler(RequestValidationError)
# async def validation_handler(reuqest: Request, exc: RequestValidationError):
#     return JSONResponse(
#         status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
#         content= jsonable_encoder({"detail":exc.errors(), "body":exc.body
#         })
#     )

# class Item(BaseModel):
#     title:str
#     size: int

# @app.post("/items")
# async def read_items(item:Item):
#     return item

# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request,exc):
#     print(f"OMG! An HTTP error!: {repr(exc)}")
#     return await http_exception_handler(request,exc)

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request,exc):
#     print(f"OMG! The client sent invalid data!: {exc}")
#     return await request_validation_exception_handler(request,exc)

# @app.get("/blah_item/{item_id}")
# async def read_item(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail= "Nope! I don't like 3.")
#     return {"item_id": item_id}

##  video - 20 - Path Operation Confiuguration
# class Item(BaseModel):
#     name: str
#     description: Optional[str] = None
#     price: float
#     tax: Optional[float] = None
#     tags: Set[str] = set()

# class Tags(Enum):
#     items = "items"
#     users = "users"


# @app.post(
#     "/items/", 
#     response_model=Item, 
#     status_code=status.HTTP_201_CREATED, 
#     tags=[Tags.items],
#     summary=" Create an Item",
#     # description="Create an item with all the information:"
#     #     "name; description; price; tax; and a set of unique tags",
#     response_description="The Item created"
# )
# async def created_item(item: Item):
#     """
#     Create an item with all insformation:
#     - **name**: Each item have a name
#     - **description**: E long serciption
#     - **price**: Required
#     - **tax**: If the item deosn't have tax, you can omit this
#     - **tags**: A set of unique tag strings for this item
#     """
#     return item

# @app.get("/items",tags=[Tags.items, Tags.users])
# async def read_items():
#     return [{"name":"Foo", "price":45}]

# @app.get("/users/", tags=[Tags.users])
# async def read_users():
#     return [{"username":"Srinubabu"}]

# @app.get("/elements/", tags=[Tags.items],deprecated=True)
# async def create_elements(element_id: str = "Foo"):
#     return {"Element":element_id}

## video - 21 - JSON Compatible encoder and Body
# fake_db = {}

# class Item(BaseModel):
#     name: Optional[str] = None
#     description: Optional[str] = None
#     price: Optional[float] = None
#     tax: float= 10.6
#     tags: List[str] = list()

# items = {
#     "foo": {"name":"Foo", "Description": "This is Foo Item", "price":150},
#     "bar": {
#         "name":"Bar", 
#         "description":"The barteners", 
#         "price":2000, 
#         "tax":12.5
#     },
#     "baz":{
#         "name":"Baz",
#         "description":None,
#         "price":100,
#         "tax":5.5,
#         "tags":["items","users"]
#     },
# }

# @app.get("/items/{item_id}", response_model=Item)
# async def read_item(item_id:str):
#     return items.get(item_id)

# @app.put("/items/{item_id}", response_model=Item)
# async def update_item(item_id:str, item: Item):
#     update_item_encoded = jsonable_encoder(item)
#     items[item_id] = update_item_encoded
#     return update_item_encoded

# @app.patch("/items/{item_id}", response_model=Item)
# async def patch_item(item_id: str, item:Item):
#     stored_item_data = items.get(item_id)
#     if stored_item_data is not None:
#         stored_item_model = Item(**stored_item_data)
#     else:
#         stored_item_model = Item()
#     # print(stored_item_model)
#     update_data = item.dict(exclude_unset=True)
#     updated_item = stored_item_model.copy(update=update_data)
#     items[item_id] = jsonable_encoder(updated_item)
#     print(items[item_id])
#     return updated_item

## video - 22 - Dependencies Intro
# async def hello():
#     return "World"
# async def common_parameters(q: Optional[str] = None, skip:int=0, limit:int=100, blah: str = Depends(hello)):
#     return {"q":q, "skip":skip,"limit":limit, "hello":blah}

# @app.get("/items/")
# async def read_items(commons:dict = Depends(common_parameters)):
#     return commons

# @app.get("/users/")
# async def read_users(commons:dict = Depends(common_parameters)):
#     return commons.q

##video - 23 - Classes as Dependencies
# fake_items_db = [
#     {"item_name":"Foo"}, 
#     {"item_name":"Bar"}, 
#     {"item_name":"Baz"},
#     {"item_name":"Poo"},
#     {"item_name":"Raa"},
# ]

# class CommonQueryParams:
#     def __init__(self, q: Optional[str] = None, skip: int= 0, limit: int= 100):
#         self.q = q 
#         self.skip = skip
#         self.limit = limit

# @app.get("/items/")
# async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
#     response = {}
#     if commons.q:
#         response.update({"q":commons.q})
#     items = fake_items_db[commons.skip: commons.skip + commons.limit]
#     response.update({"items":items})
#     return response

##video - 24 - Sub Dependecies
# def query_extractor(q: Optional[str] = None):
#     return q

# def query_or_body_extractior(
#     q: str = Depends(query_extractor),
#     last_query: Optional[str] = Body(None)
# ):
#     if q:
#         return q
#     return last_query
# @app.post("/items/")
# async def try_query(query_or_body: str = Depends(query_or_body_extractior)):
#     return {"query_or_body":query_or_body}

## video - 25 - Dependencies in Path Operation Decorators
# async def verify_token(x_token: str = Header(...)):
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-token header invalid")
#     return x_token

# async def verify_key(x_key:str = Header(...)):
#     if x_key != "fake-super-secret-key":
#         raise HTTPException(status_code= 400, detail="X-Key header invalid")
#     return x_key

# @app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
# async def read_items(blah:str = Depends(verify_key)):
#     return [{"item":"Foo"}, {"item":"Bar"}, {"X_key":blah}]

## video - 26 - Security, First steps
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

# fake_users_db = {
#     "johndoe":dict(
#         username = "johndoe",
#         full_name = "John Doe",
#         email = "Johndoe@example.com",
#         hashed_password = "fakehashedsecret",
#         disabled = False,
#     ),
#     "alice":dict(
#         username = "alice",
#         full_name = "Alice",
#         email = "alice@example.com",
#         hashed_password = "fakehashedsecret2",
#         disabled = True,
#     ),
# }

# def fake_hash_password(password: str):
#     return f"fakehashed{password}"

# class User(BaseModel):
#     username: str
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     disabled: Optional[str] = None

# class UserInDB(User):
#     hashed_password: str

# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
    
# async def fake_decode_token(token):
#     return get_user(fake_users_db, token)

# async def get_current_user(token:str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate":"Bearer"}
#         )
#     return user

# async def get_curent_active_user(current_user:User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# @app.post("/token")
# async def login(form_date: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_date.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect Username or Password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_date.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect Username or Password")
    
#     return {"access_token":user.username, "token_type":"bearer"}

# @app.get("/users/me")
# async def get_me(current_user: User = Depends(get_curent_active_user)):
#     return current_user

# @app.get("/items/")
# async def read_items(token:str =Depends(oauth2_scheme)):
#     return {"token":token}

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# fake_users_db = {
#     "johndoe": dict(
#         username="johndoe",
#         full_name="John Doe",
#         email="johndoe@example.com",
#         hashed_password="fakehashedsecret",
#         disabled=True,
#     ),
#     "alice": dict(
#         username="alice",
#         full_name="Alice Wonderson",
#         email="alice@example.com",
#         hashed_password="fakehashedsecret2",
#         disabled=True,
#     ),
# }


# def fake_hash_password(password: str):
#     return f"fakehashed{password}"


# class User(BaseModel):
#     username: str
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     disabled: Optional[str] = None


# class UserInDB(User):
#     hashed_password: str


# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)


# def fake_decode_token(token):
#     return get_user(fake_users_db, token)


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     user = fake_decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if not current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user


# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     user = UserInDB(**user_dict)
#     hashed_password = fake_hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(status_code=400, detail="Incorrect username or password")

#     return {"access_token": user.username, "token_type": "bearer"}


# @app.get("/users/me")
# async def get_me(current_user: User = Depends(get_current_active_user)):
#     return current_user


# @app.get("/items/")
# async def read_items(token: str = Depends(oauth2_scheme)):
#     return {"token": token}

## video - 27 - Security, OAuth2 with Password, Bearer with JWT(JSON Web Tokens)
# SECRET_KEY="thequickbrownfoxjumpsoverthelazydog"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30

# fake_user_db = {
#     "johndoe": dict(
#         username = "johndoe",
#         full_name = "John Doe",
#         email = "johndoe@example.com",
#         hashed_password = "$2b$12$GghkJyJfm6hq0DpqPnttVOS.hNcKOH5nhLGh7F5Wl9DmiK8FEM8pG",
#         disabled = False
#     ),
# }

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class TokenData(BaseModel):
#     username: Optional[str] = None

# class User(BaseModel):
#     username: str
#     email: Optional[str]= None
#     full_name: Optional[str] = None
#     disabled:bool = False

# class UserInDB(User):
#     hashed_password:str

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

# def get_user(db, username: str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)
    
# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(db=fake_db, username= username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

# def create_access_token(data:dict, expires_delta: Optional[timedelta] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.now(timezone.utc)+ expires_delta
#     else:
#         expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#     to_encode.update({"exp":expire})
#     encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm= ALGORITHM)
#     return encoded_jwt

# @app.post("/token", response_model= Token)
# async def login_for_access(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(fake_user_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail= "Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"}
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data = {"sub": user.username},
#         expires_delta = access_token_expires,
#         )
#     return {"access_token":access_token, "token_type":"bearer"}

# async def get_current_user(token:str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate":"Bearer"}
#     )

#     try:
#         payload = jwt.decode(token=token, key=SECRET_KEY,algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_user_db, username= token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user

# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# @app.get("/users/me", response_model=User)
# async def get_me(current_user: User = Depends(get_current_active_user)):
#     return current_user

# @app.get("/users/me/items")
# async def read_own_items(current_user:User = Depends(get_current_active_user)):
#     return [{"Item_id":"Foo", "Owner":current_user.username}]

## video - 28 - Middleware and CORS
# class MyMiddleware(BaseHTTPMiddleware):
#     async def dispatch(self, request:Request, call_next):
#         start_time = time.time()
#         response = await call_next(request)
#         process_time = time.time() - start_time
#         response.headers["X-Process-Time"] = str(process_time)
#         return response

# origins = ["http://localhost:8000","http://localhost:3000"]
# app.add_middleware(MyMiddleware)
# app.add_middleware(CORSMiddleware, allow_origins = origins)

# @app.get("/blah")
# async def blah():
#     return {"hello":"world"}

## video - 31 - Background Tasks
# async def write_notification(email: str,message= ""):
#     with open('log.txt', mode= 'w') as email_file:
#         content = f'notification for {email}: {message}'
#         time.sleep(5)
#         email_file.write(content)

# @app.post("/send-notification/{email}",status_code=202)
# async def send_notification(email:str, background_taks: BackgroundTasks):
#     background_taks.add_task(write_notification, email, message="some notifications")
#     return {"message": "Notification sent in the background"}


# async def write_log(message: str):
#     with open('log.txt', mode = 'a') as log:
#         log.write(message)

# async def get_query(background_tasks: BackgroundTasks, q: Optional[str] = None):
#     if q: 
#         message = f" Found Query: {q}\n"
#         background_tasks.add_task(write_log,message)

#     return q

# @app.post("/send-notification/{email}")
# async def send_notification(
#     email: str, background_tasks: BackgroundTasks, q:str = Depends(get_query)
# ):
#     if q is None:
#         message = f"No query message send to {email}  \n"
#         background_tasks.add_task(write_log, message)
#         return { "message": "No query Message ", "email":email}
#     message = f"message to {email} \n"
#     background_tasks.add_task(write_log, message)
#     return { "message": "Message was send to", "email":email}


## video- 32 - Metadata and Docs URLs
# description = """
# CimichangApp API helps you do awesome stuff

# ## Items

# You can **read items**

# ## Users

#  You will be able to:

#  * **Create usrs** (_not implemeted_).
#  * **Read users** (_not implemented_).
# """


# tags_metadata = [
#     dict(
#         name= "users",
#         description = " Operations with users. the **login** logic is also here",
#     ),
#     dict(
#         name= "items",
#         description = "Manage items. So _fancy_ they have their own docs.",
#         externalDocs = dict(
#             description = "Items external docs",
#             url = "https://www.jvp.design"
#         ),
#     ),
    
# ]
# app = FastAPI(
#     title= "ChimichangApp",
#     description = description,
#     version= "0.0.01",
#     terms_of_service="http://example.com/terms/",
#     contact=dict(
#         name="Srinu Babu",
#         url = "http://x-force.example.com/contact",
#         email = "babu.fastapi@example.com"
#     ),
#     license_info=dict(
#         name="Apache 2.0",
#         url = "https://wwww.apache.org/licenses/LICENSE-2.0.html"
#     ),
#     openapi_tags= tags_metadata,
#     openapi_url = "/api/v1/openapi.json"
# )


# @app.get("/users", tags=["users"])
# async def get_users():
#     return [{"name":"Balu"},{"name":"Mahi"}]

# @app.get("/items", tags=["items"])
# async def read_items():
#     return [
#         {"name":"Babu"},
#         {"name":"Siva"}
#     ]
    

## video - 33 - Static Files , Testing and Debugging

# app.mount("/static", StaticFiles(directory="static"), name = "static")

fake_secret_token = "coneofsilence"
fake_db = dict(
    foo = dict(
        id="foo",title="Foo", description="There goes hero"
    ),
    bar = dict(
        id="bar", title="Bar",description="The bartennders"
    )
)

class Item(BaseModel):
    id: str
    title: str 
    description : Optional[str] = None

@app.get("/items/{item_id}", response_model=Item)
async def read_main(item_id: str, x_token: str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return fake_db[item_id]

@app.post("/items/", response_model=Item)
async def create_item(item:Item, x_token:str = Header(...)):
    if x_token != fake_secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id in fake_db:
        raise HTTPException(status_code=404, detail="Item not found")
    fake_db[item.id] = item
    return item
