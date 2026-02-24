from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
class Category(Base):
    __tablename__="categories"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    notes=relationship("Note",back_populates="category")
class Note(Base):
    __tablename__="notes"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    content=Column(String,default="")
    category_id=Column(Integer,ForeignKey("categories.id"))
    #foreignkey,relationship connects both the categories by an id 
    category=relationship("Category",back_populates="notes")