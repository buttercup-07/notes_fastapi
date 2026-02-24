from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.orm import sessionmaker,DeclarativeBase
DATABASE_URL = "sqlite+aiosqlite:///./notes.db"
engine=create_async_engine(DATABASE_URL)
AsyncSessionLocal=sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)
#class_=AsyncSession is a parameter you pass to sessionmaker to tell it what type of session to create.
class Base(DeclarativeBase):
    pass
async def get_session():
    async with AsyncSessionLocal() as session:
        yield session