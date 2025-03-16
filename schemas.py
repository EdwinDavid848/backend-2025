from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    password: str
    rol: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


