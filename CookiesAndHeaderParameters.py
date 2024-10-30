from fastapi import (
    FastAPI,
    Cookie,
    Header
)
from typing import Optional,List

app = FastAPI()

## video - 12- cookie and header Parameters
@app.put("/items")
async def read_items(
    cookie_id:Optional[str]=Cookie(None),
    accept_encoding: Optional[str] = Header(None),
    see_ch_ua: Optional[str] = Header(None),
    user_agent: Optional[str] = Header(None),
    x_token: Optional[List[str]] = Header(None)
):
    return {"cookie_id":cookie_id,
            "Accept-Encoding":accept_encoding,
            "sec-ch-ua":see_ch_ua,
            "User-Agent":user_agent,
            "X-token-values":x_token,
            }