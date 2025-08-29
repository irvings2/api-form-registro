from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Formulario, FormularioDatosGenerales, FormularioInfoProyecto, FormularioEstadoTec
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
        
class FormularioDatosGeneralesCreate(BaseModel):
    formulario_proyecto_id: int
    nombre_proyecto: str
    integrantes: List[Integrante]
    enlace: Optional[str] = None
    empresa_constituida: str
    rfc_emp: Optional[str] = None
    institucion: str
    tiempo_desarrollo: str

    class Config:
        from_attributes = True  # (Pydantic v2) para mapear desde SQLAlchemy
        
class FormularioInfoProyectoCreate(BaseModel):
    formulario_proyecto_id: int
    resumen: str
    objetivo: str
    clasificacion: str
    nombre_producto: str
    descripcion: str
    proyecto_vida: str
    justificacion_proy_vida: str
    tipo_producto: str
    mejora_producto: str
    apoyo: str
    asesorias: List[str]
    asesoria_otro: str

    class Config:
        from_attributes = True  # (Pydantic v2) para mapear desde SQLAlchemy
        
class FormularioEstadoTec_Create(BaseModel):
    formulario_proyecto_id: int
    base_tecnologica: str
    base_tec_descripcion: str
    grado_avance: str
    innovacion: str
    innovacion_justificacion: str
    intensidad: str
    tiene_instalaciones: str
    instalaciones_descripcion: str
    tiene_equipo: str
    equipo_actual: str
    equipo_necesario: str

    class Config:
        from_attributes = True  # (Pydantic v2) para mapear desde SQLAlchemy
        
def make_folio(id_: int, prefix: str = "DIET", width: int = 5) -> str:
    year = datetime.utcnow().year
    return f"{prefix}-{year}-{id_:0{width}d}"

@app.get("/")
def read_root():
    return {"mensaje": "Hola Mundo desde FastAPI 🚀"}

@app.get("/formularios/")
def get_formularios(db: Session = Depends(get_db)):
    return db.query(Formulario).all()

@app.get("/formulario/{user_id}")
def get_formulario(user_id: int, db: Session = Depends(get_db)):
    
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
def get_datos_generales(formulario_id: int, db: Session = Depends(get_db)):
    
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

    nuevo = FormularioDatosGenerales(**data,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/formulario/info_proyecto/{formulario_id}")
def get_info_proyecto(formulario_id: int, db: Session = Depends(get_db)):
    
    dato = db.query(FormularioInfoProyecto).filter(FormularioInfoProyecto.formulario_proyecto_id == formulario_id).first()
    
    if dato:
        try:
            dato.asesorias = json.loads(dato.integrantes)
        except Exception:
            dato.asesorias = []
    
    return dato

@app.post("/formulario/info_proyecto/")
def create_info_proyecto(payload: FormularioInfoProyectoCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    
    data["asesorias"] = json.dumps(payload.asesorias, ensure_ascii=False)

    nuevo = FormularioInfoProyecto(**data,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.get("/formulario/estado_tec/{formulario_id}")
def get_estado_tec(formulario_id: int, db: Session = Depends(get_db)):
    
    return db.query(FormularioEstadoTec).filter(FormularioEstadoTec.formulario_proyecto_id == formulario_id).first()

@app.post("/formulario/estado_tec/")
def create_estado_tec(payload: FormularioEstadoTec_Create, db: Session = Depends(get_db)):
    data = payload.model_dump()

    nuevo = FormularioEstadoTec(**data,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo
