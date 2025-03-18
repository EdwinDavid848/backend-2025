from pydantic import BaseModel, EmailStr, validator
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


class Usuario(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    password: str
    rol: str

    class Config:
        orm_mode = True

class UpdateRequest(BaseModel):
    value: str

class UpdatePassword(BaseModel):
    original: str
    nuevo: str
    email: str


class CarritoResponseModel(BaseModel):
    product_id: int
    product_name: str
    cantidad: int
    precio: float
    total: float
    imagen_url: str  


class CarritoAgregar(BaseModel):
    producto_id: int
    cantidad: int

    @validator('cantidad')
    def cantidad_positiva(cls, v):
        if v <= 0:
            raise ValueError('La cantidad debe ser mayor que cero')
        return v


