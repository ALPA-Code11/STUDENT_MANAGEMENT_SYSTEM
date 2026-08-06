from sqlalchemy import create_engine, Column, Integer, String,Float,ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, Session,relationship
from database import Base


class role_permission_model(Base):
    __tablename__="Role_Permission_Details"

    id=Column(Integer,primary_key=True,autoincrement=True)

    role_id=Column(Integer,ForeignKey("Role_Details.role_id",ondelete="CASCADE"),nullable=False)

    permission_id = Column(Integer,ForeignKey("Permission_Details.permission_id", ondelete="CASCADE"), nullable=False)


    role = relationship("role_model", back_populates="role_permissions")
    permission = relationship("permission_model", back_populates="role_permissions")


    

