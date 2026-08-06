from sqlalchemy import create_engine, Column, Integer, String,Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session,relationship
from database import Base



class role_model(Base):
    __tablename__="Role_Details"

    role_id=Column(Integer,primary_key=True,index=True)
    role_name=Column(String)


    users = relationship("User", back_populates="role")
    role_permissions = relationship("role_permission_model", back_populates="role", cascade="all, delete-orphan")


