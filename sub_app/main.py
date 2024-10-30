from fastapi import FastAPI, Depends

from .dependencies import get_query_token, get_token_header


# todo: import routers
from .routers import users, items



app = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(router=users.router) # users router
app.include_router(router=items.router) # items router


@app.get('/')
async def root():
    return {"message":" Hello Bigger Application!"}