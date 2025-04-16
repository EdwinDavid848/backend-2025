from pydantic import BaseModel, EmailStr, validator,ConfigDict
from typing import Optional
from datetime import date,time


class UserCreate(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    password: str
    rol: str

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Usuario(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    password: str
    rol: str

    model_config = ConfigDict(from_attributes=True)

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

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

class ForgotPasswordRequest(BaseModel):
    email: str

# DANIELA ==========================================================================

class editUsu(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    rol: Optional[str] = None
    telefono: Optional[str] = None

class Hisotial_Email(BaseModel):
    email_client: str

class Classmodel(BaseModel):
    titulo: str
    descripcion: str
    profesor: str
    fecha: str  
    comienzo: time
    final: time
    precio: float
    habilitado: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)

class ReservationClass(BaseModel):
    titulo_clase: str
    email_user: str
    date_class: date
    status: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class PayClass(BaseModel):
    reservation_id: int 
    metodo_pago: str
    monto: float
    fecha_pago: date

    model_config = ConfigDict(from_attributes=True)

class mural(BaseModel):
    id: int
    id_user: int
    email: str
    titulo: str
    descripcion: str
    foto: str

    model_config = ConfigDict(from_attributes=True)

class metodoPay(BaseModel):
    nombre:str
    descripcion:str