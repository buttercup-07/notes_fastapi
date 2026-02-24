from pydantic import BaseModel
from typing import Optional,List
class CategoryCreate(BaseModel):
    name:str
class CategoryResponse(BaseModel):
    id:int
    name:str
    class Config:
        from_attributes=True
class NoteCreate(BaseModel):
    title:str
    content:str=""
    category_id:int
class NoteUpdate(BaseModel):
    title:str |None=None
    content:str|None=None
    category_id:int|None=None
class NoteResponse(BaseModel):
    id:int
    title:str
    content:str
    category_id:int
    class Config:
        from_attributes=True
        #tells pydantic its okay to read data from sqlalchemy object instead of plain dict
#pydantic - data validation library 
#make sure the data coming into your api is exactly the shape and type u expect