from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 👈 1. Yeh import karein
from database import engine, Base  

from app.models.role_model import role_model
from app.models.user_model import User
from app.models.permission_model import permission_model
from app.models.role_permission_model import role_permission_model

# Routers import karein
from app.api.auth import router as auth_router  
from app.api.admin import router as admin_router  
from app.api.pagination import router as users_router

app = FastAPI(
    title="Student Management System API",
    description="Student Management Project with Role-Based Access Control (RBAC)",
    version="1.0.0"
)

# 👈 2. Yahan CORS Middleware add karein (App initialization ke turant baad)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174"],  # React ka URL allow kiya
    allow_credentials=True,
    allow_methods=["*"],  # Saare methods (GET, POST, etc.) allow hain
    allow_headers=["*"],  # Saare headers allow hain
)

# Dono routers link kiye
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(users_router)

@app.get("/")
def home():
    return {"message": "Welcome to Student Management System API! Server ekdam mast chal raha hai."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)