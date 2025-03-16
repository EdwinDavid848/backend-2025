from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User
from schemas import UserCreate, UserLogin
from security import hash_password, verify_password, create_access_token
from fastapi.staticfiles import StaticFiles



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


    
@app.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    
    if not user_data.password:
        raise HTTPException(status_code=400, detail="La contraseña es obligatoria")
    
    hashed_password = hash_password(user_data.password)
    new_user = User(
        nombre=user_data.nombre,
        email=user_data.email,
        telefono=user_data.telefono,
        password=hashed_password,
        rol=user_data.rol
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario registrado correctamente"}



""""
@app.post("/register")
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    hashed_password = hash_password(user_data.password)
    new_user = User(email=user_data.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario registrado correctamente"}  
"""



@app.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=400, detail="Contraseña Incorrecta")

    token = create_access_token({"sub": user.email, "rol": user.rol.name})
    return {"access_token": token, "token_type": "bearer", "rol": user.rol.name}







app.mount("/images", StaticFiles(directory="img"), name="images")

@app.get("/mostrarimagenes_Categoria/ropa")
def obtener_imagenes():
    return [
        {"id":"lana","nombre": "Producto 1", "precio": 10000, "descripcion": "Descripcion de los Productos", "imagen_url": "http://localhost:8000/images/ProductosRopa 2.jpg"},
        {"id":"lana","nombre": "Producto 1", "precio": 10000,"descripcion": "Descripcion de los Productos", "imagen_url": "http://localhost:8000/images/ProductosRopa 2.jpg"},
        {"id":"lana","nombre": "Producto 2", "precio": 12000,"descripcion": "Descripcion de los Productos", "imagen_url": "http://localhost:8000/images/ProductosRopa 2.jpg"},
        {"id":"lana","nombre": "Producto 2", "precio": 12000,"descripcion": "Descripcion de los Productos", "imagen_url": "http://localhost:8000/images/ProductosRopa 2.jpg"},
        {"id":"lana","nombre": "Producto 3", "precio": 9000, "descripcion": "Descripcion de los Productos","imagen_url": "http://localhost:8000/images/ProductosRopa 2.jpg"},
        {"id":"peluche","nombre": "Producto 3", "precio": 9000, "descripcion": "Descripcion de los peluche","imagen_url": "http://localhost:8000/images/ProductosRopa 2.jpg"},
    ]


@app.get("/mostrarProductos/lana")
def obtener_productos():
    return [
        {"nombre": "Producto 1", "precio": 10000, "descripcion": "Descripcion de los lana", "imagen_url": "http://localhost:8000/images/Producto 2 part1.jpeg"},
        {"nombre": "Producto 1", "precio": 10000,"descripcion": "Descripcion de los lana", "imagen_url": "http://localhost:8000/images/Producto 2 part1.jpeg"},
        {"nombre": "Producto 2", "precio": 12000,"descripcion": "Descripcion de los lana", "imagen_url": "http://localhost:8000/images/Producto 2 part1.jpeg"},
        {"nombre": "Producto 2", "precio": 12000,"descripcion": "Descripcion de los lana", "imagen_url": "http://localhost:8000/images/Producto 2 part1.jpeg"},
        {"nombre": "Producto 3", "precio": 9000, "descripcion": "Descripcion de los lana","imagen_url": "http://localhost:8000/images/Producto 2 part1.jpeg"},
        {"nombre": "Producto 3", "precio": 9000, "descripcion": "Descripcion de los lana","imagen_url": "http://localhost:8000/images/Producto 2 part1.jpeg"},
    ]
@app.get("/mostrarProductos/piedras")
def obtener_productos():
    return [
        {"nombre": "Producto 1", "precio": 10000, "descripcion": "Descripcion de los piedras", "imagen_url": "http://localhost:8000/images/Producto 1 part1.jpeg"},
        {"nombre": "Producto 1", "precio": 10000,"descripcion": "Descripcion de los piedras", "imagen_url": "http://localhost:8000/images/Producto 1 part1.jpeg"},
        {"nombre": "Producto 2", "precio": 12000,"descripcion": "Descripcion de los piedras", "imagen_url": "http://localhost:8000/images/Producto 1 part1.jpeg"},
        {"nombre": "Producto 2", "precio": 12000,"descripcion": "Descripcion de los piedras", "imagen_url": "http://localhost:8000/images/Producto 1 part1.jpeg"},
        {"nombre": "Producto 3", "precio": 9000, "descripcion": "Descripcion de los piedras","imagen_url": "http://localhost:8000/images/Producto 1 part1.jpeg"},
        {"nombre": "Producto 3", "precio": 9000, "descripcion": "Descripcion de los piedras","imagen_url": "http://localhost:8000/images/Producto 1 part1.jpeg"},
    ]
@app.get("/mostrarProductos/agujas")
def obtener_productos():
    return [
        {"nombre": "Producto 1", "precio": 10000, "descripcion": "Descripcion de los agujas", "imagen_url": "http://localhost:8000/images/Producto 1 part1.jpeg"},
        {"nombre": "Producto 1", "precio": 10000,"descripcion": "Descripcion de los agujas", "imagen_url": "http://localhost:8000/images/Producto 1 part1.jpeg"},
        {"nombre": "Producto 2", "precio": 12000,"descripcion": "Descripcion de los agujas", "imagen_url": "http://localhost:8000/images/Producto 1 part1.jpeg"},
        {"nombre": "Producto 2", "precio": 12000,"descripcion": "Descripcion de los agujas", "imagen_url": "http://localhost:8000/images/Producto 1 part1.jpeg"},
        {"nombre": "Producto 3", "precio": 9000, "descripcion": "Descripcion de los agujas","imagen_url": "http://localhost:8000/images/Producto 1 part1.jpeg"},
        {"nombre": "Producto 3", "precio": 9000, "descripcion": "Descripcion de los agujas","imagen_url": "http://localhost:8000/images/Producto 1 part1.jpeg"},
    ]


@app.get("/productosNombre/{id}")
def obtener_imagenes(id: str):
    if id == "lana":
            return {
                "id": "lana",
                "nombre": "lanas",
                "descripcion": "descripcion de las lanas",
                "precio": 12200,
                "tipo_unidad": "unidades",
                "color": "azul",
                "category":"lana",
                "imagen_url": "http://localhost:8000/images/Producto 1 part1.jpeg"
                }
    elif id == "peluche":
        return {
                "id": "lana",
                "nombre": "peluches",
                "descripcion": "descripcion de las peluches",
                "precio": 90200,
                "tipo_unidad": "unidades",
                "color": "azul",
                "category":"lana",
                "imagen_url": "http://localhost:8000/images/Producto 2 part1.jpeg"
                }
    else:
        return {"error": "Producto no encontrado"}, 404
