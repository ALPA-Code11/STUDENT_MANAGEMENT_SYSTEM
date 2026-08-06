from pydantic import BaseModel

class rolecreate(BaseModel):
     role_name:str


class roleresponse(BaseModel):
    role_id:int
    role_name:str
    
         
class Config:
        from_attributes = True 

