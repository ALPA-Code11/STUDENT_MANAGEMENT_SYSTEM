from sqlalchemy import create_engine, Column, Integer, String,Float,ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session,relationship
from database import Base


class User(Base):
    __tablename__="user_details"

    user_id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String)
    role_id=Column(Integer,ForeignKey("Role_Details.role_id",ondelete="RESTRICT"), nullable=False)


    role=relationship("role_model",back_populates="users")
    refresh_tokens = relationship("RefreshToken",back_populates="user",cascade="all, delete-orphan")






    