from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import get_db


from app.models.role_model import role_model
from app.models.permission_model import permission_model
from app.models.role_permission_model import role_permission_model


from app.schemas.role_schema import rolecreate,roleresponse
from app.schemas.permission_schema import permissioncreate,permissionresponse
from app.schemas.role_permission_schema import role_permission_create,role_permission_response

router = APIRouter(prefix="/admin", tags=["Admin Operations"]) # Prefix laga diya taaki main.py saaf rahe


#Roles create api  
@router.post("/roles",status_code=status.HTTP_201_CREATED)
def  roles_create(r:rolecreate,db:Session=Depends(get_db)):
    existing_role=db.query(role_model).filter(role_model.role_name==r.role_name).first()

    if existing_role:
        raise HTTPException(status_code=400,detail=f"Role '{r.role_name}' already exists")

    new_role=role_model(role_name=r.role_name)

    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    return {"message":f"Role '{new_role.role_name}' created successfully","role_id":new_role.role_id}


# Permission api create krna 
@router.post("/permission",status_code=status.HTTP_201_CREATED)
def permission_create(p:permissioncreate,db:Session=Depends(get_db)):
    existing_permission=db.query(permission_model).filter(permission_model.permission_name==p.permission_name).first()

    if existing_permission:
        raise HTTPException(status_code=400,detail="Permission already exists!")

    new_permission=permission_model(permission_name=p.permission_name)
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)

    return new_permission


# roles_Permission  api create 

@router.post("/roles/assign-permission", status_code=status.HTTP_200_OK)
def assign_permission_to_role(t: role_permission_create, db: Session = Depends(get_db)):
    # 🔍 CHECK 1: Kya woh Role database mein sach mein hai?
    role = db.query(role_model).filter(role_model.role_id == t.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found!")

    # 🔍 CHECK 2: Kya woh Permission database mein sach mein hai?
    permission = db.query(permission_model).filter(permission_model.permission_id == t.permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found!")

    # 🔍 CHECK 3: Kya yeh dono pehle se hi aapas mein linked hain? (Duplicate Check)
    existing_role_permission = db.query(role_permission_model).filter(
        role_permission_model.role_id == t.role_id,
        role_permission_model.permission_id == t.permission_id
    ).first()
    
    if existing_role_permission:
        raise HTTPException(status_code=400, detail="This permission is already assigned to this role!")

    # ✍️ AGAR SAB SAHI HAI, TOH DATABASE MEIN ENTRY DAALO
    new_mapping = role_permission_model(
        role_id=t.role_id, 
        permission_id=t.permission_id
    )
    db.add(new_mapping)
    db.commit()

    return {"message": f"Permission successfully assigned to Role '{role.role_name}'"}




