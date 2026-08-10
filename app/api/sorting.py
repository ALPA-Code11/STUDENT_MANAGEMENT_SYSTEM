from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import math  
from database import get_db

from app.models.user_model import User
from app.models.role_model import role_model

# 👈 Yeh line sabse zaroori hai (Router define karna)
router = APIRouter(prefix="/users", tags=["Sorting"])

@router.get("/sorting")
def sorting_users(sort_by:str="username",order:str="asc",db: Session = Depends(get_db)):
    query=db.query(User)

    if sort_by=="email":
        sort_column=User.email

    else:
        sort_column=User.username



    if order == "desc":
        users = query.order_by(sort_column.desc()).all()
    else:
        users = query.order_by(sort_column.asc()).all()

    result = []
    for user in users:
        user_data = user.__dict__.copy()  # User object ko dictionary mein badla
        user_data.pop("password", None)       # Password field uda di
        user_data.pop("_sa_instance_state", None) # SQLAlchemy ka internal tag hataya
        result.append(user_data)

    return {
        "sorted_by": sort_by,
        "order": order,
        "data": result  # 👈 Yahan cleaned data bhej diya
    }
