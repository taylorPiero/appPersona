from sqlalchemy import Column, Integer, String, DateTime,Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional
from datetime import date
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext


 
class TokenData(BaseModel):
    email: str | None = None
 
class PR_Persona_model(BaseModel):
    PR_Per_in_id: int |None = None
    PR_Per_ch_nomb: str | None = None
    PR_Per_ch_apeMat: str | None = None
    PR_Per_ch_apePat: str | None = None
    PR_Per_dt_nac: date | None = None
    PR_Per_ch_doc: str | None = None
    # FK_PR_Detal_Pers: int | None = None
    # FK_PR_Paramet_Pers: int | None = None
    
class PR_Detalle_Persona_model(BaseModel):

    PR_DetP_ch_tel: str | None = None
    PR_DetP_ch_email: str | None = None
    PR_DetP_ch_sexo: str | None = None
    FK_PR_Pers: int | None = None
    FK_PR_Paramet_Pers: int | None = None


class PR_Parametro_Persona_model(BaseModel):
    PR_Par_ch_nomb: str | None = None
    PR_Par_ch_descrip: str | None = None
    estado: str | None = None

# Modelo para DB_PRACTICAS_USUARIO
class PR_Rol_model(BaseModel):
    PR_Usu_rol_ch_nomb: str | None = None

class PR_Perfil_model(BaseModel):
    PR_Usu_perf_ch_nomb: str | None = None

class PR_Usuario_model(BaseModel):
    PR_Usu_ch_nomb: str | None = None
    PR_Usu_ch_pass: str | None = None
    PR_Usu_perid_fk: int | None = None
    PR_Usu_rolid_fk: int | None = None
    PR_Usu_perfid_fk: int | None = None

# Modelo para DB_PRACTICAS_GRUPOS
class PR_grupos_model(BaseModel):
    PR_Gru_ch_nomb: str | None = None
    PR_Gru_per_fk: str | None = None

class PR_segmentos_model(BaseModel):
    PR_Seg_ch_nomb: str | None = None
    PR_Seg_Gru_idfk: int | None = None

# Modelo para DB_PRACTICAS_MENSAJE
class PR_TMensaje_model(BaseModel):
    PR_TMens_ch_nombre: str | None = None

class PR_DetalleMensaje_model(BaseModel):
    PR_DetMen_ch_nomb: str | None = None
    PR_Per_fk: int | None = None
    TipoMen_fk: int | None = None

class Pr_Archivos_model(BaseModel):
    PR_Arch_ch_nombre: str | None = None
    PR_Per_fk: int | None = None
    PR_TipoArch_fk: int | None = None
    PR_NombreArchivo: str | None = None
    
class login_bm(BaseModel):
    email: str | None = None
    passs: str | None = None