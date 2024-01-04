from fastapi import FastAPI

app = FastAPI()

@app.get("/",description="This the first api get route")
async def BADE_GET_ROUTE():
    return {"message":"Hello from get"}

@app.post("/")
async def post():
    return {"message":"Hello from post"}

@app.put("/")
async def put():
    return {"message":"Hello from put"}