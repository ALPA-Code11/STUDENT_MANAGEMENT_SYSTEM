import os
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import get_db
from app.models.user_model import User

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 2     # Access token 15 minutes ke liye
REFRESH_TOKEN_EXPIRE_DAYS = 7         # Refresh token 7 din ke liye

# 1. Access Token banane ka function
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 2. Refresh Token banane ka function (Naya add kiya hai)
def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# 3. Bodyguard Function (Access Token verify karne ke liye)
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials 
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        token_type = payload.get("type")
        
        # Check karein ki yeh 'access' token hi hai na, kahin koi galti se refresh token toh nahi bhej raha
        if username is None or token_type != "access":
            raise HTTPException(status_code=401, detail="Invalid Token Type")
    except:
        raise HTTPException(status_code=401, detail="Could not validate credentials or Token Expired")

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
        
    return user

# 4. Role Checker Function (Permissions check karne ke liye)
def check_role(allowed_roles: list[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role.role_name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="No Access! Tumhare paas iski permission nahi hai."
            )
        return current_user
    return role_checker


