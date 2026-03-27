from  typing import Optional

from pydantic import BaseModel, EmailStr, Field




class UserSchema(BaseModel):
    username:str = Field(min_length=3, max_length=70)
    email: EmailStr
    password:str = Field(min_length=1, max_length=8)

class UserResetSchema(BaseModel):
    email: EmailStr
    password1:str = Field(min_length=1, max_length=8)
    password2:str = Field(min_length=1, max_length=8)



class UserResponse(BaseModel):
    id: int = 1
    username: str
    email: str
    avatar: str
    class Config:
        from_attributes = True

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    email: EmailStr