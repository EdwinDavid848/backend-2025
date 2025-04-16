from sqlalchemy import Column, Integer, String, Text, Enum, Float, TIMESTAMP, ForeignKey,Date,Time,Boolean
from database import Base
import enum
from datetime import datetime
from sqlalchemy.orm import relationship


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

class PaymentMethod(enum.Enum):
    nequi="nequi"
    daviplata="daviplata"
    presencial="presencial"

class dias(enum.Enum):
    lunes="lunes",
    martes="martes",
    miercoles="miercoles",
    jueves="jueves",
    viernes="viernes"



class OrderStatus(enum.Enum):
    reserved = "reserved"
    paid = "paid"
    cancelled = "cancelled"

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
    activo = Column(Boolean, default=True)

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey('users.id'))
    fecha_pedido = Column(TIMESTAMP, default=datetime.utcnow)
    estado = Column(Enum(OrderStatus))
    cliente = relationship('User')


class OrderDetail(Base):
    __tablename__ = 'order_details'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey('orders.id'))
    producto_id = Column(Integer, ForeignKey('products.id'))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    
    Orders=relationship('Order')
    Products=relationship('Product')


class Payment(Base):
    __tablename__ = 'payments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(Integer, ForeignKey('orders.id'))
    reservation_id = Column(Integer, ForeignKey('class_reservations.id'))
    metodo_pago = Column(Enum(PaymentMethod),nullable=False)
    monto = Column(Float, nullable=False)
    fecha_pago = Column(TIMESTAMP, default=datetime.utcnow)
    
    
    Orders=relationship('Order')
    Reservatons=relationship('ClassReservation')



class Cart(Base):
    __tablename__ = 'carts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('users.id'))
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow)
    
    cliente = relationship('User')
    detalles = relationship('DetailsCart', back_populates="cart")

class DetailsCart(Base):
    __tablename__ = 'details_cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    carrito_id = Column(Integer, ForeignKey('carts.id'))
    producto_id = Column(Integer, ForeignKey('products.id'))
    cantidad = Column(Integer, nullable=False)

    cart = relationship('Cart', back_populates="detalles")
    product = relationship('Product') 


class Class(Base):
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(255))
    descripcion = Column(String(255))
    profesor = Column(String(255))
    fecha = Column(Enum(dias), nullable=False)
    comienzo = Column(Time)
    final = Column(Time)
    precio = Column(Float)
    habilitado = Column(Boolean, default=True)
    imagen=Column(String(255))

    reservations = relationship("ClassReservation")

class ClassReservation(Base):
    __tablename__ = 'class_reservations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_clase = Column(Integer, ForeignKey('class.id'))
    id_user = Column(Integer, ForeignKey('users.id'))
    fecha_class = Column(Date)
    estado = Column(Enum(OrderStatus), default=OrderStatus.reserved)
    
    user = relationship('User')
    clase = relationship('Class')
    
# Tabla Publications (Mural)
class Publication(Base):
    __tablename__ = 'publications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'))
    titulo = Column(String(255))
    descripcion = Column(String(255))
    foto = Column(String(255))
    
    user = relationship('User')