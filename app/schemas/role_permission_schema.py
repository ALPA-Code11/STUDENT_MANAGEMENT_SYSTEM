from pydantic import BaseModel

class role_permission_create(BaseModel):
    role_id:str
    permission_id:str



    
class role_permission_response(BaseModel):
    role_id:int
    role:str
    permission_id:int
    permission:str    



class Config:
        from_attributes = True 

