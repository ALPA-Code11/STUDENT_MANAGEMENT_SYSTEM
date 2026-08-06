from pydantic import BaseModel

class permissioncreate(BaseModel):
    permission_name:str


class permissionresponse(BaseModel):
    permission_id:int
    permission_name:str

    
class Config:
        from_attributes = True 



