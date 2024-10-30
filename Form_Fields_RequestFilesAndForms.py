from fastapi import (
    FastAPI,
    Body,
    Form, 
    File, 
    UploadFile,
)

from pydantic import BaseModel

app = FastAPI()

## video - 16 - Form Fields
@app.post("/login/")
async def login(username:str = Form(...), password:str = Form(...)):
    return {"username":username, "password":password}

class User(BaseModel):
    username: str
    password: str

@app.post("/login-json/")
async def login_json(user:User):
    return user

# video -17 - Request Files
@app.post("/files/")
async def create_file(file:bytes = File(...)):
    return {"file length" :len(file)}

@app.post("/uploadfile/")
async def create_file(file: UploadFile):
    return {"file name" :file.filename}

# video - 18 - Request Forms and Files
@app.post("/files/")
async def create_file(
    file:bytes = File(...), 
    fileb:UploadFile = File(...), 
    token:str = Form(...),
    hello:str = Body(...)
):
    return {
        "file_size": len(file),
        "token":token,
        "file_content_type" : fileb.content_type,
        "helo":hello
    }
