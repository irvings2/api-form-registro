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
    info_proyecto = relationship("FormularioInfoProyecto", back_populates="formulario", uselist=False)
    estado_tec = relationship("FormularioEstadoTec", back_populates="formulario", uselist=False)
    
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
    
class FormularioInfoProyecto(Base):
    __tablename__ = "formulario_info_proyecto"

    id = Column(Integer, primary_key=True, index=True)
    formulario_proyecto_id = Column(Integer, ForeignKey('formulario_proyecto.id') ,nullable=False)
    resumen = Column(Text, nullable=False)
    objetivo = Column(Text, nullable=False)
    clasificacion = Column(String(255), nullable=False)
    nombre_producto = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=False)
    proyecto_vida = Column(String(255), nullable=False)
    justificacion_proy_vida = Column(Text, nullable=False)
    tipo_producto = Column(String(255), nullable=False)
    mejora_producto = Column(Text, nullable=False)
    apoyo = Column(Text, nullable=False)
    asesorias = Column(Text, nullable=False)
    asesoria_otro = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    formulario = relationship("Formulario", back_populates="info_proyecto")
    
class FormularioEstadoTec(Base):
    __tablename__ = "formulario_estado_tecnologico"

    id = Column(Integer, primary_key=True, index=True)
    formulario_proyecto_id = Column(Integer, ForeignKey('formulario_proyecto.id') ,nullable=False)
    base_tecnologica = Column(String(255), nullable=False)
    base_tec_descripcion = Column(Text, nullable=False)
    grado_avance = Column(String(255), nullable=False)
    innovacion = Column(String(255), nullable=False)
    innovacion_justificacion = Column(Text, nullable=False)
    intensidad = Column(String(255), nullable=False)
    tiene_instalaciones = Column(String(255), nullable=False)
    instalaciones_descripcion = Column(Text, nullable=False)
    tiene_equipo = Column(String(255), nullable=False)
    equipo_actual = Column(Text, nullable=False)
    equipo_necesario = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    formulario = relationship("Formulario", back_populates="estado_tec")
