from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db

from app.core.redis_client import redis_client
import json

from app.models.user_model import User
from deps import check_role


router = APIRouter(prefix="/teacher", tags=["Teacher_Info"])


@router.get("/get_teachers")
def get_teachers(db: Session = Depends(get_db)):

    # 1. Redis mein teachers ka cached data check karo
    cached_teachers = redis_client.get("teachers:all")

    if cached_teachers:
        return {
            "data": json.loads(cached_teachers),
            "source": "cache"
        }

    # 2. Cache nahi mila → Database se teachers lao
    teachers = db.query(User).filter(User.role_id == 2).all()

    result = []

    for teacher in teachers:
        teacher_data = teacher.__dict__.copy()
        teacher_data.pop("password", None)
        teacher_data.pop("_sa_instance_state", None)
        result.append(teacher_data)

    # 3. Database se mila data Redis mein 210 seconds ke liye save karo
    redis_client.set(
        "teachers:all",
        json.dumps(result),
        ex=180
    )

    return {
        "data": result,
        "source": "database"
    }