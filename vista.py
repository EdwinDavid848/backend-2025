from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User,Product
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


@app.get("/mostrarimagenes")
def obtener_imagenes(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    productos = db.query(Product).offset(offset).limit(limit).all()  
    return [
        {
            "id": producto.id,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "tipo_unidad": producto.tipo_unidad,
            "color": producto.color,
            "category": producto.category,
            "imagen_url": f"http://localhost:8000{producto.imagen_url}"
        }
        for producto in productos
    ]


@app.get("/mostrarimagenes_Categoria/{category}")
def obtener_imagenes(category: str, limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    productos = db.query(Product).filter(Product.category == category).offset(offset).limit(limit).all()
    return [
        {
            "id": producto.id,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "tipo_unidad": producto.tipo_unidad,
            "color": producto.color,
            "category": producto.category,
            "imagen_url": f"http://localhost:8000{producto.imagen_url}"
        }
        for producto in productos
    ]



@app.get("/buscar_producto/{id}")
def obtener_imagenes(id: int, db: Session = Depends(get_db)):
    producto = db.query(Product).filter(Product.id == id).first()
    if producto:  
        return {
            "id": producto.id,
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "tipo_unidad": producto.tipo_unidad,
            "color": producto.color,
            "category": producto.category,
            "imagen_url": f"http://localhost:8000{producto.imagen_url}"
        }
    else:
        return {"error": "Producto no encontrado"}, 404

