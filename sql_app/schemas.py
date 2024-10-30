from pydantic import BaseModel
from typing import Optional, List

class ItemBase(BaseModel):
    title: str
    description : Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class USerBase(BaseModel):
    email: str

class UserCreate(USerBase):
    password: str

class User(USerBase):
    id: int
    is_active: bool
    items: List[Item] = []

    class Config:
        orm_mode = True