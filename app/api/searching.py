from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import math  # 👈 Math import karna zaroori hai total_pages ke liye
from database import get_db

from app.models.user_model import User
from app.models.role_model import role_model

# 👈 Yeh line sabse zaroori hai (Router define karna)
router = APIRouter(prefix="/searching_users", tags=["Searching"])


@router.get("/")
def search_users(keyword: str, db: Session = Depends(get_db)):
    users = db.query(User).filter(User.username.ilike(f"%{keyword}%")).all()
    
    # Har user ka dictionary banakar password field ko pop (hata) kar dena
    result = []
    for user in users:
        user_data = user.__dict__.copy()
        user_data.pop("password", None) # Password uda diya
        user_data.pop("_sa_instance_state", None) # SQLAlchemy ka internal state hatane ke liye
        result.append(user_data)

    return {"search_keyword": keyword, "data": result}



# Iska matlab jab aap API call karenge,
#  toh URL banega: /searching_users/?keyword=rahul
