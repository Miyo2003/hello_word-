from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./hello.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy model
class Hello(Base):
    __tablename__ = "hello"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    message = Column(String, index=True)

# Pydantic models
class HelloResponse(BaseModel):
    id: int
    name: Optional[str] = None
    message: str
    class Config:
        orm_mode = True

class HelloRequest(BaseModel):
    name: Optional[str] = None