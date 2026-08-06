from sqlalchemy import create_engine, Column, Integer,String,Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session,relationship
from database import Base


class permission_model(Base):

    __tablename__="Permission_Details"


    permission_id=Column(Integer,primary_key=True)
    permission_name=Column(String)


    role_permissions = relationship("role_permission_model", back_populates="permission", cascade="all, delete-orphan")


    


