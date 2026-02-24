from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import engine,Base,get_session
from models import Category,Note
from schemas import CategoryCreate, CategoryResponse, NoteCreate, NoteUpdate, NoteResponse
from contextlib import asynccontextmanager
from typing import List

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app=FastAPI(lifespan=lifespan)

#CREATE CATEGORY 
@app.post("/categories",response_model=CategoryResponse)
async def create_categories(category:CategoryCreate,session:AsyncSession=Depends(get_session)):
    new_category =Category(**category.model_dump())
    session.add(new_category)
    await session.commit()
    await session.refresh(new_category)
    return new_category

#GET caTEGORY
@app.get("/categories",response_model=List[CategoryResponse])
async def get_categories(session:AsyncSession=Depends(get_session)):
    result= await session.execute(select(Category))
    return result.scalars().all()

    #scalars() — unwraps the package and extracts the actual Python objects (like your Category or Note objects) from the raw database rows. Without this you'd get weird tuple-like objects instead of clean Python objects.
    #.all() — converts everything into a Python list so you can return it.

#DELETE CATEGORY
@app.delete("/categories/{category_id}")
async def delete_category(category_id:int,session:AsyncSession=Depends(get_session)):
    category=await session.get(Category,category_id)
    if not category:
        raise HTTPException(status_code=404,detail="Category not found")
    await session.delete(category)
    await session.commit()
    return{"message":"Category deleted successfully"}

#CREATE NOTe
@app.post("/notes",response_model=NoteResponse)
async def create_note(note: NoteCreate,session:AsyncSession=Depends(get_session)):
    category =await session.get(Category,note.category_id)
    if not category:
        raise HTTPException(status_code=404,detail="Category not found")
    new_note=Note(**note.model_dump())
    session.add(new_note)
    await session.commit()
    await session.refresh(new_note)
    return new_note

#GET ALL NOTes
@app.get("/notes",response_model=List[NoteResponse])
async def get_notes(session:AsyncSession=Depends(get_session)):
    result=await session.execute(select(Note))
    return result.scalars().all()

#uptade note
@app.patch("/notes/{note_id}")
async def updtae_note(note_id:int,update:NoteUpdate,session:AsyncSession=Depends(get_session)):
    note=await session.get(Note,note_id)
    if not note:
        raise HTTPException(status_code=404 , detail="Note not found")
    for field,value in update.model_dump(exclude_unset=True).items():
        setattr(note,field,value)
    await session.commit()
    await session.refresh(note)
    return note

#delete note
@app.delete("/notes/{note_id}")
async def delete_note(note_id:int ,session:AsyncSession=Depends(get_session)):
    note=await session.get(Note,note_id)
    if not note:
        raise HTTPException(status_code=404,detail="Note not found")
    await session.delete(note)
    await session.commit()
    return {"message":"Note deleted successfully"}

#Get all notes in a category 
@app.get("/categories/{category_id}/notes",response_model=List[NoteResponse])
async def get_notes_by_category(category_id:int,session:AsyncSession=Depends(get_session)):
    category=await session.get(Category,category_id)
    if not category:
        raise HTTPException(status_code=404,detail="Category not found")
    result=await session.execute(select(Note).where(Note.category_id==category_id))
    return result.scalars().all()