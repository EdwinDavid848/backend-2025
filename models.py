from sqlalchemy import Column, Integer, String, Text, Enum, Float
from database import Base
import enum


class UserRole(enum.Enum):
    administrador = "administrador"
    profesor = "profesor"
    cliente = "cliente"

class category(enum.Enum):
    lana="lana"
    piedras="piedras"
    agujas="agujas"
    peluche="peluche"
    ropa="ropa"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telefono = Column(String(11))
    password = Column(String(255), nullable=False)
    rol = Column(Enum(UserRole), nullable=False)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Text, nullable=False)
    descripcion = Column(Text)
    precio = Column(Float, nullable=False)
    tipo_unidad = Column(String(50), nullable=False)
    color = Column(String(250), nullable=False)
    category = Column(Enum(category))
    imagen_url = Column(String(300))