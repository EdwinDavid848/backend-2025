from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User
from schemas import UserCreate, UserLogin
from security import hash_password, verify_password, create_access_token
from fastapi.staticfiles import StaticFiles



app = FastAPI()

# Permitir peticiones desde el frontend Vue
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Cambia al puerto correcto de Vue
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Crear las tablas si no existen
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

    hashed_password = hash_password(user_data.password)
    new_user = User(email=user_data.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario registrado correctamente"}  


@app.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}



app.mount("/images", StaticFiles(directory="img"), name="images")

@app.get("/mostrarimagenes_Categoria/ropa")
def obtener_imagenes():
    return [
        {"nombre": "Producto 1", "precio": 10000, "imagen_url": "http://localhost:8000/images/ProductosRopa 2.jpeg"},
        {"nombre": "Producto 1", "precio": 10000, "imagen_url": "http://localhost:8000/images/ProductosRopa 2.jpeg"},
        {"nombre": "Producto 2", "precio": 12000, "imagen_url": "http://localhost:8000/images/ProductosRopa 2.jpeg"},
        {"nombre": "Producto 2", "precio": 12000, "imagen_url": "http://localhost:8000/images/ProductosRopa 2.jpeg"},
        {"nombre": "Producto 3", "precio": 9000, "imagen_url": "http://localhost:8000/images/ProductosRopa 2.jpeg"},
        {"nombre": "Producto 3", "precio": 9000, "imagen_url": "http://localhost:8000/images/ProductosRopa 2.jpeg"},
    ]

