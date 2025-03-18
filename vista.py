from fastapi import FastAPI, Depends, HTTPException, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User,Product, Cart, DetailsCart, OrderDetail 
from schemas import UserCreate, UserLogin, CarritoAgregar, CarritoResponseModel, Usuario, UpdateRequest, UpdatePassword
from security import hash_password, verify_password, create_access_token,verify_token
from fastapi.staticfiles import StaticFiles
import os




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

    token = create_access_token({"sub": user.email, "email": user.email, "rol": user.rol.name})
    return {"access_token": token, "token_type": "bearer", "email": user.email, "rol": user.rol.name}



@app.get("/usuarios", response_model=Usuario)  
async def obtener_usuario(token: str = Depends(verify_token), db: Session = Depends(get_db)):
    email_user = token.get("sub") 
    if not email_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")  
    db_user = db.query(User).filter(User.email == email_user).first()  
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos") 
    
    return db_user 

@app.put("/usuarios/{campo}/{email}")
async def update_user_data(campo: str,email: str,data: UpdateRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

    if campo not in ['nombre','email', 'telefono', ]:
        raise HTTPException(status_code=400, detail="Campo no válido")

    if campo == 'email':
        db_user.email = data.value
    elif campo == 'telefono':
        db_user.telefono = data.value
    elif campo == 'nombre':
        db_user.nombre = data.value

    db.commit()
    db.refresh(db_user)

    return {"message": f"{campo.capitalize()} actualizado exitosamente", "user": db_user}


@app.put("/password/")
async def update_password(data: UpdatePassword, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == data.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="El correo no está registrado")  
    
    if verify_password(data.original, db_user.password):  # Verifica la contraseña actual
        db_user.password = hash_password(data.nuevo)  # Hashea la nueva contraseña
        
        db.commit()
        db.refresh(db_user)
        
        return {"message": "Contraseña actualizada exitosamente"}
    else:
        raise HTTPException(status_code=400, detail="La contraseña original no es correcta")






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




@app.get("/ver_carrito/{email}", response_model=list[CarritoResponseModel])
def ver_carrito(email: str, session: Session = Depends(get_db)):
    cliente = session.query(User).filter(User.email == email).first()
    
    if not cliente:
        raise HTTPException(status_code=404, detail="El cliente no existe")
    
    carrito = session.query(DetailsCart).join(Cart).filter(Cart.cliente_id == cliente.id).all()

    if not carrito:
        raise HTTPException(status_code=404, detail="El carrito está vacío")

    carrito_respuesta = []
    for item in carrito:
        producto = session.query(Product).filter_by(id=item.producto_id).first()
        if producto:
            carrito_respuesta.append({
                "product_id": item.producto_id,
                "product_name": producto.nombre,
                "cantidad": item.cantidad,
                "precio": producto.precio,
                "total": producto.precio * item.cantidad,
                "imagen_url": f"http://localhost:8000{producto.imagen_url}"  # Añadir URL completa para la imagen
            })
    
    return carrito_respuesta

@app.post("/agregar_al_carrito/{email_cliente}")
def agregar_al_carrito(carrito_data: CarritoAgregar, email_cliente: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email_cliente).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

    carrito = db.query(Cart).filter_by(cliente_id=db_user.id).first()
    if carrito is None:
        carrito = Cart(cliente_id=db_user.id)
        db.add(carrito)
        db.commit()
        db.refresh(carrito) 

    detalle_existente = db.query(DetailsCart).filter_by(carrito_id=carrito.id, producto_id=carrito_data.producto_id).first()

    if detalle_existente:
        detalle_existente.cantidad += carrito_data.cantidad
        message = f'Cantidad actualizada del producto {carrito_data.producto_id} en el carrito para el cliente {db_user.id}'
    else:
        nuevo_detalle = DetailsCart(
            carrito_id=carrito.id,
            producto_id=carrito_data.producto_id,
            cantidad=carrito_data.cantidad
        )
        db.add(nuevo_detalle)
        message = f'Producto {carrito_data.producto_id} agregado al carrito para el cliente {db_user.id}'

    db.commit()

    return {"message": message}

@app.put("/actualizar_producto_carrito/{email_cliente}")
def actualizar_producto_carrito(email_cliente: str,producto_data: CarritoAgregar, db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.email == email_cliente).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

    carrito = db.query(Cart).filter_by(cliente_id=db_user.id).first()
    if carrito is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado para el usuario")

    detalle_existente = db.query(DetailsCart).filter_by(
        carrito_id=carrito.id,
        producto_id=producto_data.producto_id
    ).first()

    if detalle_existente is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")

    detalle_existente.cantidad = producto_data.cantidad
    db.commit()

    return {
        "message": f"Cantidad del producto {producto_data.producto_id} actualizada a {producto_data.cantidad}"
    }



@app.delete("/eliminar_del_carrito/{email_cliente}/{producto_id}")
def eliminar_del_carrito(email_cliente: str, producto_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email_cliente).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

    carrito = db.query(Cart).filter_by(cliente_id=db_user.id).first()
    if carrito is None:
        raise HTTPException(status_code=404, detail="Carrito no encontrado para el usuario")

    detalle_existente = db.query(DetailsCart).filter_by(carrito_id=carrito.id, producto_id=producto_id).first()
    if detalle_existente is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado en el carrito")

    db.delete(detalle_existente)
    db.commit()

    detalles_restantes = db.query(DetailsCart).filter_by(carrito_id=carrito.id).count()
    if detalles_restantes == 0:
        db.delete(carrito)
        db.commit()
        return {"message": f"Producto {producto_id} eliminado y carrito vacío eliminado para el cliente {db_user.id}"}

    return {"message": f"Producto {producto_id} eliminado del carrito para el cliente {db_user.id}"}





@app.get("/informacionTabla")
def obtener_imagenes(db: Session = Depends(get_db)):
    productos = db.query(Product).all()  
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


@app.get("/informacionTabla/{category}")
def obtener_imagenes(category: str, db: Session = Depends(get_db)):
    productos = db.query(Product).filter(Product.category == category).all()
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





@app.post("/insertardos")
async def registrar_cliente(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: float = Form(...),
    tipo_unidad: str = Form(...),
    color: str = Form(...),
    category: str = Form(...), 
    url: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if url.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Formato de archivo no soportado")

    # Verificar si ya existe un producto con el mismo nombre y color
    existing_product = db.query(Product).filter(Product.nombre == nombre, Product.color == color).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Ya existe un producto con el mismo nombre y color")

    folder_path = "img"
    file_location = os.path.join(folder_path, url.filename)
    
    os.makedirs(folder_path, exist_ok=True)

    with open(file_location, "wb") as buffer:
        buffer.write(await url.read())

    # Crear una URL accesible para la imagen
    imagen_url = f"/images/{url.filename}"

    # Crear una instancia del modelo con los datos
    producto_data = Product(
        nombre=nombre,
        descripcion=descripcion,
        precio=precio,
        tipo_unidad=tipo_unidad,
        color=color,
        category=category,  # Este debe coincidir con tu Enum definido
        imagen_url=imagen_url  # Guardar la URL accesible en lugar de la ruta local
    )

    # Guardar producto_data en la base de datos
    db.add(producto_data)
    db.commit()
    db.refresh(producto_data)

    return {"status": "Producto registrado exitosamente", "data": {
        "nombre": producto_data.nombre,
        "descripcion": producto_data.descripcion,
        "precio": producto_data.precio,
        "tipo_unidad": producto_data.tipo_unidad,
        "color": producto_data.color,
        "category": producto_data.category,
        "imagen_url": producto_data.imagen_url
    }}

@app.put("/productosActualizar/{product_id}")
async def actualizar_cliente(
    product_id: int,
    nombre: str = Form(None),
    descripcion: str = Form(None),
    precio: float = Form(None),
    tipo_unidad: str = Form(None),
    color: str = Form(None),
    category: str = Form(None),  
    url: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Buscar el producto a actualizar
    producto_data = db.query(Product).filter(Product.id == product_id).first()
    if not producto_data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verificar si ya existe otro producto con el mismo nombre y color (excepto el actual)
    existing_product = db.query(Product).filter(Product.nombre == nombre, Product.color == color).filter(Product.id != product_id).first()
    if existing_product:
        raise HTTPException(status_code=400, detail="Ya existe un producto con el mismo nombre y color")

    # Actualizar los campos si no son None
    if nombre is not None:
        producto_data.nombre = nombre
    if descripcion is not None:
        producto_data.descripcion = descripcion
    if precio is not None:
        producto_data.precio = precio
    if tipo_unidad is not None:
        producto_data.tipo_unidad = tipo_unidad
    if color is not None:
        producto_data.color = color
    if category is not None:
        producto_data.category = category

    # Si se sube una nueva imagen, actualizarla
    if url:
        if url.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Formato de archivo no soportado")

        folder_path = "img"
        file_location = os.path.join(folder_path, url.filename)
        os.makedirs(folder_path, exist_ok=True)

        with open(file_location, "wb") as buffer:
            buffer.write(await url.read())

        producto_data.imagen_url = f"/images/{url.filename}"

    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(producto_data)

    return {"status": "Producto actualizado exitosamente", "data": {
        "nombre": producto_data.nombre,
        "descripcion": producto_data.descripcion,
        "precio": producto_data.precio,
        "tipo_unidad": producto_data.tipo_unidad,
        "color": producto_data.color,
        "category": producto_data.category,
        "imagen_url": producto_data.imagen_url
    }}


@app.delete("/productosEliminar/{product_id}")
async def eliminar_producto(product_id: int, db: Session = Depends(get_db)):
    producto_data = db.query(Product).filter(Product.id == product_id).first()
    if not producto_data:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto_data)
    db.commit()

    return {"status": "Producto eliminado exitosamente", "product_id": product_id}
@app.delete("/productos/{producto_id}", response_model=dict)
async def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    order_details = db.query(OrderDetail).filter(OrderDetail.producto_id == producto_id).all()
    for order_detail in order_details:
        db.delete(order_detail)  

    producto = db.query(Product).filter(Product.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(producto)  
    db.commit()
    
    return {"detail": "Producto eliminado exitosamente"}



@app.delete("/productos/{producto_id}", response_model=dict)
async def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    order_details = db.query(OrderDetail).filter(OrderDetail.producto_id == producto_id).all()
    for order_detail in order_details:
        db.delete(order_detail)  

    producto = db.query(Product).filter(Product.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    db.delete(producto)  
    db.commit()
    
    return {"detail": "Producto eliminado exitosamente"}
