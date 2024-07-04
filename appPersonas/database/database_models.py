from sqlalchemy import Column, Integer, String, DateTime,Float,ForeignKey, Date,Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Date
from decimal import Decimal
from sqlalchemy.orm import relationship



# Creamos una base declarativa para cada motor (una por cada base de datos)
Base = declarative_base()

# Modelo para DB_PRACTICAS_PERSONA
class PR_Persona_base(Base):
    __tablename__ = 'PR_Persona'
    PR_Per_in_id = Column(Integer, primary_key=True)
    PR_Per_ch_nomb = Column(String(50), nullable=False)
    PR_Per_ch_apeMat = Column(String(25), nullable=False)
    PR_Per_ch_apePat = Column(String(25), nullable=False)
    PR_Per_dt_nac = Column(Date)
    PR_Per_ch_doc = Column(String(8), nullable=False)
    estado = Column(Boolean, nullable=False, default=1)
    date_create = Column(DateTime, nullable=False)
    date_update = Column(DateTime, nullable=False)
    date_delete = Column(DateTime)
    PR_grupo_id_fk = Column(Integer)  # Referencia al grupo
    per_detalle_persona = relationship("PR_Detalle_Persona_base", backref="PR_Persona_base",uselist=False)

    
class PR_Detalle_Persona_base(Base):
    __tablename__ = 'PR_Detalle_Persona'
    PR_DetP_id = Column(Integer, primary_key=True)
    PR_DetP_ch_tel = Column(String(8), nullable=False)
    PR_DetP_ch_email = Column(String(40), nullable=False)
    PR_DetP_ch_sexo = Column(String(1), nullable=False)
    estado = Column(Boolean, nullable=False, default=1)
    date_create = Column(DateTime, nullable=False)
    date_update = Column(DateTime, nullable=False)
    date_delete = Column(DateTime)
    FK_PR_Pers = Column(Integer, ForeignKey('PR_Persona.PR_Per_in_id'))
    FK_PR_Paramet_Pers = Column(Integer, ForeignKey('PR_Parametro_Persona.PR_Par_in_id'))
    per_persona = relationship("PR_Persona_base", backref="PR_Detalle_Persona")
    per_parametro_persona = relationship("PR_Parametro_Persona_base", backref="PR_Detalle_Persona")


class PR_Parametro_Persona_base(Base):
    __tablename__ = 'PR_Parametro_Persona'
    PR_Par_in_id = Column(Integer, primary_key=True)
    PR_Par_ch_nomb = Column(String(25), nullable=False)
    PR_Par_ch_descrip = Column(String(25), nullable=False)
    estado = Column(Boolean, nullable=False, default=1)
    date_create = Column(DateTime, nullable=False)
    date_update = Column(DateTime, nullable=False)
    date_delete = Column(DateTime)
    

# Modelo para DB_PRACTICAS_USUARIO
class PR_Rol_base(Base):
    __tablename__ = 'PR_Rol'
    PR_Usu_rol_id = Column(Integer, primary_key=True)
    PR_Usu_rol_ch_nomb = Column(String(25), nullable=False)
    

class PR_Perfil_base(Base):
    __tablename__ = 'PR_Perfil'
    PR_Usu_perf_id = Column(Integer, primary_key=True)
    PR_Usu_perf_ch_nomb = Column(String(25), nullable=False)

class PR_Usuario_base(Base):
    __tablename__ = 'PR_Usuario'
    PR_Usu_in_id = Column(Integer, primary_key=True)
    PR_Usu_ch_nomb = Column(String(25), nullable=False)
    PR_Usu_ch_pass = Column(String(100), nullable=False)
    estado = Column(Boolean, nullable=False, default=1)
    PR_Usu_perid_fk = Column(Integer)  # Debería referenciar a una tabla 'Personas' y llamar a email
    PR_Usu_rolid_fk = Column(Integer, ForeignKey('PR_Rol.PR_Usu_rol_id'))
    PR_Usu_perfid_fk = Column(Integer, ForeignKey('PR_Perfil.PR_Usu_perf_id'))
    rol = relationship("PR_Rol_base", backref="PR_Usuario")
    perfil = relationship("PR_Perfil_base", backref="PR_Usuario")

# Modelo para DB_PRACTICAS_GRUPOS
class PR_grupos_base(Base):
    __tablename__ = 'PR_grupos'
    PR_Gru_id = Column(Integer, primary_key=True)
    PR_Gru_ch_nomb = Column(String(25))
    PR_Gru_per_fk = Column(Integer)

class PR_segmentos_base(Base):
    __tablename__ = 'PR_segmentos'
    PR_Seg_id = Column(Integer, primary_key=True)
    PR_Seg_ch_nomb = Column(String(25))
    PR_Seg_Gru_idfk = Column(Integer, ForeignKey('PR_grupos.PR_Gru_id'))
    grupo = relationship("PR_grupos_base", backref="PR_segmentos")

# Modelo para DB_PRACTICAS_MENSAJE
class PR_TMensaje_base(Base):
    __tablename__ = 'PR_TMensaje'
    PR_TMens_id = Column(Integer, primary_key=True)
    PR_TMens_ch_nombre = Column(String(25))

class PR_DetalleMensaje_base(Base):
    __tablename__ = 'PR_DetalleMensaje'
    PR_DetMen_id = Column(Integer, primary_key=True)
    PR_DetMen_ch_nomb = Column(String(25))
    PR_Per_fk = Column(Integer)
    TipoMen_fk = Column(Integer, ForeignKey('PR_TMensaje.PR_TMens_id'))
    tipo_mensaje = relationship("PR_TMensaje_base", backref="PR_DetalleMensaje")

class Pr_Archivos_base(Base):
    __tablename__ = 'PR_Archivos'
    PR_Arch_id = Column(Integer, primary_key=True)
    PR_Arch_ch_nombre = Column(String(25))
    PR_Per_fk = Column(Integer)
    PR_TipoArch_fk = Column(Integer)
    PR_NombreArchivo = Column(String(25))