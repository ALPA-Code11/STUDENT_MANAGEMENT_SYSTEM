from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import math  # 👈 Math import karna zaroori hai total_pages ke liye
from database import get_db

from app.models.user_model import User
from app.models.role_model import role_model

# 👈 Yeh line sabse zaroori hai (Router define karna)
router = APIRouter(prefix="/users", tags=["Pagination"])

@router.get("/")  # Agar prefix /users de diya hai, toh yahan sirf "/" rakh sakte hain
def get_paginated_users(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit

    # Data aur Total count nikalna
    users = db.query(User).offset(skip).limit(limit).all()
    total_count = db.query(User).count()

    total_pages = math.ceil(total_count / limit) if limit > 0 else 1

    return {
        "page": page,
        "limit": limit,
        "total_users": total_count,
        "total_pages": total_pages,
        "data": users
    }




    