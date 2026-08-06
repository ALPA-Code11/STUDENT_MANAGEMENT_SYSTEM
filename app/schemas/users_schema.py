from pydantic import BaseModel,EmailStr

class userregister(BaseModel):
    username:str
    email:EmailStr
    password:str


# class TeacherRegister(UserRegister):
#     teacher_id:str
#     teacher_name:str



# class StudentRegister(User)    


class userlogin(BaseModel):
    username:str
    password:str

