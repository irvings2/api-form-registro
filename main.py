from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Formulario, FormularioDatosGenerales
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import json

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

@app.get("/")
def read_root():
    return {"mensaje": "Hola Mundo desde FastAPI 🚀"}

@app.get("/formularios/")
def get_usuarios(db: Session = Depends(get_db)):
    return db.query(Formulario).all()

@app.get("/formulario/{user_id}")
def get_usuarios(user_id: int, db: Session = Depends(get_db)):
    
    return db.query(Formulario).filter(Formulario.user_id == user_id).first()

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

