from fastapi import FastAPI
from database import engine, Base  

from app.models.role_model import role_model
from app.models.user_model import User
from app.models.permission_model import permission_model
from app.models.role_permission_model import role_permission_model



# Routers import karein
from app.api.auth import router as auth_router  
from app.api.admin import router as admin_router  # 👈 Ab admin router yahan properly import kar liya hai

# Database me tables create karne ke liye

app = FastAPI(
    title="Student Management System API",
    description="Student Management Project with Role-Based Access Control (RBAC)",
    version="1.0.0"
)

# Dono routers link kiye
app.include_router(auth_router)
app.include_router(admin_router)

@app.get("/")
def home():
    return {"message": "Welcome to Student Management System API! Server ekdam mast chal raha hai."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)