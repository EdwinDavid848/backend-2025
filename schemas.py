from pydantic import BaseModel, EmailStr, validator

from datetime import date,time
from typing import Optional
from enum import Enum

class UpdatePassword(BaseModel):
    original: str
    nuevo: str
    email: str

class UpdateRequest(BaseModel):
    value: str



class CarritoResponseModel(BaseModel):
    product_id: int
    product_name: str
    cantidad: int
    precio: float
    total: float
    imagen_url: str  

class Usuario(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    password: str
    rol: str

    class Config:
        orm_mode = True


class Login(BaseModel):
    email: str
    password: str

class ProductCreate(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    tipo_unidad: str  
    color: str  
    category: str



class ProductResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    tipo_unidad: str
    color: str 
    category: str

    class Config:
        orm_mode = True


class ProductUpdate(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    precio: Optional[float]
    tipo_unidad: Optional[str]
    color: Optional[str]
    category: Optional[str]
    

class CategoryResponse(BaseModel):
    id: int
    descripcion: str
    tipo: str

    class Config:
        orm_mode = True


class ProductDetailResponse(BaseModel):
    id: int  # ID del producto
    nombre: str  # Nombre del producto
    descripcion: str  # Descripción del producto
    precio: float  # Precio del producto
    stock: int  # Stock del producto
    categoria: CategoryResponse  # Incluir la categoría del producto
    tipo_unidad: str  # Agregado para el tipo de unidad del producto

    class Config:
        orm_mode = True


class ProductWithCategoryResponse(BaseModel):
    id: int
    nombre: str
    descripcion: str
    precio: float
    stock: int
    categoria: CategoryResponse  # Incluye la categoría como parte de la respuesta

    class Config:
        orm_mode = True


class ProductTypeEnum(str, Enum):
    lana = "lana"
    aguja = "aguja"
    piedra = "piedra"

# Esquema para la categoría
class CategorySchema(BaseModel):
    id: int
    descripcion: Optional[str]
    tipo: ProductTypeEnum

    class Config:
        orm_mode = True

# Esquema para el producto con categoría
class ProductSchema(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    precio: float
    stock: int
    tipo_unidad: str
    color: str
    categoria: CategorySchema  # Relación con la categoría

    class Config:
        orm_mode = True

# Esquema para actualizar el producto (input)
class ProductUpdateSchema(BaseModel):
    nombre: Optional[str]
    descripcion: Optional[str]
    precio: Optional[float]
    stock: Optional[int]
    tipo_unidad: Optional[str]
    color: Optional[str]
    categoria_id: Optional[int]  
    
    


class carritoAgregar(BaseModel):
    producto_id: int
    cantidad: int

    @validator('cantidad')
    def cantidad_positiva(cls, v):
        if v <= 0:
            raise ValueError('La cantidad debe ser mayor que cero')
        return v


#DANIELA===========================================================================================

class editUsu(BaseModel):
    nombre: Optional[str] = None
    email:Optional[str] = None
    password:Optional[str] = None
    rol:Optional[str] = None
    telefono:Optional[str] = None



class Hisotial_Email(BaseModel):
    email_client:str


class Classmodel(BaseModel):
    titulo: str
    descripcion: str
    profesor: str
    fecha: str  
    comienzo: time
    final: time
    precio:float
    habilitado : Optional[bool]=None

    class Config:
        orm_mode = True
        

        
class ReservationClass(BaseModel):
    titulo_clase: str
    email_user :str
    date_class: date
    status: Optional[str]=None
    class Config:
        from_attributes = True 
    
        
class PayClass(BaseModel):
    reservation_id: int 
    metodo_pago: str  # tipo 'str' ya que es un Enum ('nequi', 'daviplata', 'presencial')
    monto: float
    fecha_pago: date

    class Config:
        from_attributes = True


class mural(BaseModel):
    id: int
    id_user: int
    email: str
    titulo: str  # Cambiado de 'titulo' a 'title'
    descripcion: str  # Cambiado de 'descripcion' a 'description'
    foto: str 
    class Config:
        orm_mode = True
    
class metodoPay(BaseModel):
    nombre:str
    descripcion:str