from fastapi import FastAPI, status

app = FastAPI()

## video - 15 - Response Status Codes
# created http status code 201
@app.post("/items/",status_code=status.HTTP_201_CREATED)
async def create_item(name:str):
    return {"name":name}

# no content status code 204
@app.delete("/items/{pk}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(pk:str):
    print("pk", pk)
    return pk

@app.get("/items/",status_code=status.HTTP_305_USE_PROXY)
async def read_items_redirect():
    return {"hello":"world"}
