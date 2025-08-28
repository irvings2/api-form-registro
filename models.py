from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from database import Base

class Formulario(Base):
    __tablename__ = "formulario_proyecto"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    folio = Column(String(50), nullable=False)
    completado = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    datos_generales = relationship("FormularioDatosGenerales", back_populates="formulario", uselist=False)
    
class FormularioDatosGenerales(Base):
    __tablename__ = "formulario_datos_generales"

    id = Column(Integer, primary_key=True, index=True)
    formulario_proyecto_id = Column(Integer, ForeignKey('formulario_proyecto.id') ,nullable=False)
    nombre_proyecto = Column(String(100), nullable=False)
    integrantes = Column(Text, nullable=False)
    enlace = Column(String(255), nullable=True)
    empresa_constituida = Column(String(50), nullable=False)
    rfc_emp = Column(String(13), nullable=True)
    institucion = Column(String(100), nullable=False)
    tiempo_desarrollo = Column(String(50), nullable=False)
    medio = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    formulario = relationship("Formulario", back_populates="datos_generales")
