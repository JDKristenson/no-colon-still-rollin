from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str
    date_of_birth: Optional[date] = None
    cancer_type: Optional[str] = None
    diagnosis_date: Optional[date] = None
    height_inches: Optional[int] = None
    current_weight_lbs: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class User(UserResponse):
    pass

