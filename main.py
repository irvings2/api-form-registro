from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Formulario, FormularioDatosGenerales
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import json
from datetime import datetime
from fastapi import status

app = FastAPI()

origins = [
    "http://localhost:8000",  # React local
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # quién puede consumir la API
    allow_credentials=True,  # si se permite el uso de cookies/autenticación
    allow_methods=["*"],  # qué métodos HTTP se permiten (GET, POST, PUT, etc.)
    allow_headers=["*"],  # qué headers se permiten
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class Integrante(BaseModel):
    nombre: str
    rfc: str
    curp: str
    direccion: str
    telefono_cel: str
    email: EmailStr
        
class FormularioDatosGeneralesCreate(BaseModel):
    formulario_proyecto_id: int
    nombre_proyecto: str
    integrantes: List[Integrante]
    enlace: Optional[str] = None
    empresa_constituida: str
    rfc_emp: Optional[str] = None
    institucion: str
    tiempo_desarrollo: str
    
class FormularioCreate(BaseModel):
    user_id: int
    completado: bool = False
    
class FormularioRead(BaseModel):
    id: int
    user_id: int
    folio: str
    completado: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # (Pydantic v2) para mapear desde SQLAlchemy
        
def make_folio(id_: int, prefix: str = "DIET", width: int = 5) -> str:
    year = datetime.utcnow().year
    return f"{prefix}-{year}-{id_:0{width}d}"

@app.get("/")
def read_root():
    return {"mensaje": "Hola Mundo desde FastAPI 🚀"}

@app.get("/formularios/")
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(Formulario).all()

@app.get("/formulario/{user_id}")
def get_usuarios(user_id: int, db: Session = Depends(get_db)):
    
    return db.query(Formulario).filter(Formulario.user_id == user_id).first()

@app.post("/formulario/", response_model=FormularioRead, status_code=status.HTTP_201_CREATED)
def create_formulario(payload: FormularioCreate, db: Session = Depends(get_db)):
    now = datetime.now()

    # 1) Crear el registro sin folio para obtener el id
    nuevo = Formulario(
        user_id=payload.user_id,
        folio="",                 # temporal
        completado=payload.completado,
        created_at=now,
        updated_at=now,
    )
    db.add(nuevo)
    db.flush()                   # obtiene nuevo.id SIN cerrar la transacción

    # 2) Generar folio con el id ya asignado
    nuevo.folio = make_folio(nuevo.id)

    # 3) Confirmar
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/formulario/datos_generales/{formulario_id}")
def get_usuarios(formulario_id: int, db: Session = Depends(get_db)):
    
    dato = db.query(FormularioDatosGenerales).filter(FormularioDatosGenerales.formulario_proyecto_id == formulario_id).first()
    
    if dato:
        try:
            dato.integrantes = json.loads(dato.integrantes)
        except Exception:
            dato.integrantes = []
    
    return dato

@app.post("/formulario/datos_generales/")
def create_datos_generales(payload: FormularioDatosGeneralesCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()

    # Serializar lista de integrantes a string
    data["integrantes"] = json.dumps([i.model_dump() for i in payload.integrantes], ensure_ascii=False)

    nuevo = FormularioDatosGenerales(**data)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

