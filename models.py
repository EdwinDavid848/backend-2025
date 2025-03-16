from sqlalchemy import Column, Integer, String, Text, Enum
from database import Base
import enum


class UserRole(enum.Enum):
    administrador = "administrador"
    profesor = "profesor"
    cliente = "cliente"
    
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(Text, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telefono = Column(String(11))
    password = Column(String(255), nullable=False)
    rol = Column(Enum(UserRole), nullable=False)
