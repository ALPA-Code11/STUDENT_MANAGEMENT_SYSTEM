from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from app.core.redis_client import redis_client
import json


from app.models.user_model import User
from deps import check_role


router = APIRouter(prefix="/students", tags=["Student_Info"])


@router.get("/get_students")
def get_students(db: Session = Depends(get_db)):

    # 1. Redis cache check karo
    cached_students = redis_client.get("students:all")

    if cached_students:
        return {
            "data": json.loads(cached_students),
            "source": "cache"
        }

    # 2. Cache nahi mila → Database se data lao
    students = db.query(User).filter(User.role_id == 3).all()

    result = []

    for student in students:
        student_data = student.__dict__.copy()
        student_data.pop("password", None)
        student_data.pop("_sa_instance_state", None)
        result.append(student_data)

    # 3. Database se mila data Redis mein 60 seconds ke liye save karo
    redis_client.set(
        "students:all",
        json.dumps(result),
        ex=180
    )

    return {
        "data": result,
        "source": "database"
    }