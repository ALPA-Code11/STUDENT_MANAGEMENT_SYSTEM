from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from jose import jwt
import os
from datetime import datetime, timedelta
from app.core.rate_limiter import rate_limit


from app.models.user_model import User
from app.models.role_model import role_model
from app.models.refresh_token_model import RefreshToken

from app.schemas.refresh_token_schema import RefreshRequest

from deps import check_role
from deps import create_access_token, create_refresh_token
from app.schemas.users_schema import userregister, userlogin


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register/admin", status_code=status.HTTP_201_CREATED)
def register_first_admin(ud: userregister, db: Session = Depends(get_db)):
    # Check if admin already exists
    existing_user = db.query(User).filter(User.username == ud.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken!")

    admin_role = db.query(role_model).filter(role_model.role_name == "admin").first()
    if not admin_role:
        raise HTTPException(status_code=400, detail="Admin role not found in database! Pehle roles insert karo.")

    admin_user = User(
        username=ud.username,
        email=ud.email,
        password=ud.password,
        role_id=admin_role.role_id
    )

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    return {"message": "First Admin registered successfully!"}


@router.post("/register/teacher",status_code=status.HTTP_201_CREATED,dependencies=[Depends(check_role(["admin"]))])
def register_teacher(ud:userregister,db: Session = Depends(get_db)):

    existing_user=db.query(User).filter(User.username==ud.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken!")

    teacher_role=db.query(role_model).filter(role_model.role_name=="teacher").first()
    if not teacher_role:
        raise HTTPException(status_code=400, detail="Teacher role not found!")


    teacher_assign=User(
        username=ud.username,
        email=ud.email,
        password=ud.password,
        role_id=teacher_role.role_id
    )

    db.add(teacher_assign)
    db.commit()
    db.refresh(teacher_assign)

    return {"message": "Teacher registered!"}



@router.post("/register/student", status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_role(["admin"]))])
def register_student(ud:userregister, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.username == ud.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken!")

    # Database se 'student' role ko dhundhein
    student_role = db.query(role_model).filter(role_model.role_name=="student").first()
    if not student_role:
        raise HTTPException(status_code=400, detail="Student role not found!")

    student_assign = User(
        username=ud.username,
        email=ud.email,
        password=ud.password,
        role_id=student_role.role_id  # Yahan student ka role_id assign hoga
    )

    db.add(student_assign)
    db.commit()
    db.refresh(student_assign)

    return {"message": "Student registered successfully!"}



@router.post("/login",dependencies=[Depends(rate_limit)])
def login(form_data: userlogin, db: Session = Depends(get_db)):
    # 1. User ko database mein dhundhein
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # 2. Plain text password check (Abhi hashing nahi ki hai toh yehi chalega)
    if user.password != form_data.password:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    # 3. Access Token aur Refresh Token generate karein (deps.py ke functions use karke)
    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})

    user_role = user.role.role_name.lower() if user.role else "student"
    
    # 4. Refresh Token ko Database mein save karein (Expiry date ke sath - maan lijiye 7 din)
    expires_at = datetime.utcnow() + timedelta(days=7)
    db_refresh_token = RefreshToken(
        user_id=user.user_id,
        token=refresh_token,
        expires_at=expires_at,
        is_revoked=False
    )
    db.add(db_refresh_token)
    db.commit()


    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user_role,
        "message": "Login successful!"
    }


@router.post("/refresh-token")
def refresh_access_token(body: RefreshRequest, db: Session = Depends(get_db)):
    try:
        # Token decode karke check karein
        payload = jwt.decode(body.refresh_token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM", "HS256")])
        username: str = payload.get("sub")
        token_type = payload.get("type")
        
        if username is None or token_type != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token type")
    except:
        raise HTTPException(status_code=401, detail="Refresh token expired or invalid")
    
    # Database mein check karein ki token valid hai aur revoke (logout) nahi hua hai
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == body.refresh_token, 
        RefreshToken.is_revoked == False
    ).first()
    
    if not db_token:
        raise HTTPException(status_code=401, detail="Refresh token has been revoked or does not exist")
    
    # User ko verify karein
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Naya Access Token generate karke de dein
    new_access_token = create_access_token({"sub": user.username})
    
    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }



@router.post("/logout")
def logout(body: RefreshRequest, db: Session = Depends(get_db)):
    # Database mein refresh token dhundhein
    db_token = db.query(RefreshToken).filter(RefreshToken.token == body.refresh_token).first()
    
    if db_token:
        # Token ko revoke (inactive) kar dein
        db_token.is_revoked = True
        db.commit()
        
    return {"message": "Logged out successfully!"}    



