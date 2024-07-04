from tkinter import CHAR, NUMERIC
from unicodedata import numeric
from click import FLOAT
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from fastapi import FastAPI, HTTPException,APIRouter,Depends,status, Form, BackgroundTasks, Request
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData,ForeignKey, Float,Numeric,func, Date
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship, joinedload
from datetime import datetime, timedelta
from typing import List,Dict,Optional
from dotenv import load_dotenv
from pydantic import BaseModel,ConfigDict, EmailStr, Field
from appPersonas.config.db import engines
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from appPersonas.database.database_models import PR_Persona_base, PR_Detalle_Persona_base, PR_Parametro_Persona_base, PR_Rol_base, PR_Perfil_base, PR_Usuario_base, PR_grupos_base, PR_segmentos_base, PR_TMensaje_base, PR_DetalleMensaje_base, Pr_Archivos_base
from appPersonas.database.models import PR_Persona_model, PR_Detalle_Persona_model, PR_Parametro_Persona_model, PR_Rol_model, PR_Perfil_model, PR_Usuario_model, PR_grupos_model, PR_segmentos_model, PR_TMensaje_model, PR_DetalleMensaje_model, Pr_Archivos_model,login_bm,TokenData
from appPersonas.database.crud import get_usuario_by_email
import telegram
import os
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import sqlite3
from sqlalchemy.ext.declarative import declarative_base
from passlib.context import CryptContext
from telegram import Bot
import requests
from .login import create_access_token ,get_current_user

from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator

from telegram.constants import ParseMode
from telegram.ext import Updater,ApplicationBuilder


from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from fastapi.templating import Jinja2Templates
import pywhatkit as kit

SessionLocal_pers = sessionmaker(autocommit=False, autoflush=False, bind=engines['persona'])

def get_db_pers():
    db = SessionLocal_pers()
    try:
        yield db
    finally:
        db.close()
        
SessionLocal_user = sessionmaker(autocommit=False, autoflush=False, bind=engines['usuario'])

def get_db_user():
    db = SessionLocal_user()
    try:
        yield db
    finally:
        db.close()

SessionLocal_grup = sessionmaker(autocommit=False, autoflush=False, bind=engines['grupos'])

def get_db_grup():
    db = SessionLocal_grup()
    try:
        yield db
    finally:
        db.close()    

        

appTO1_rout_personas = APIRouter()
app_rout_usuarios = APIRouter()
app_rout_rol = APIRouter()
app_rout_grupo = APIRouter()
appgestion = APIRouter()


# }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
# whatsapp


# load_dotenv()  # Cargar variables de entorno desde .env


# Credenciales de Twilio (deben estar en tu archivo .env)
TWILIO_ACCOUNT_SID = 'ACca03a3c9d31e0a6d05b196d75a97d3fb'
TWILIO_AUTH_TOKEN = 'b139d0a41bd657ba19429b8acd7a0e32'
TWILIO_PHONE_NUMBER = 'whatsapp:+14155238886'  # Reemplaza con tu número de WhatsApp de Twilio
                                
# Validador de solicitudes de Twilio (opcional, pero recomendado)
request_validator = RequestValidator(TWILIO_AUTH_TOKEN)

# Modelo Pydantic para la solicitud de envío de mensajes
class WhatsAppMessage(BaseModel):
    phone_numbers: list[str] = Field(..., description="Lista de números de teléfono (con código de país)")
    message: str = Field(..., description="Mensaje a enviar")

# ... (otras importaciones)

@appgestion.post("/send_whatsapp_message")
async def send_whatsapp_message(message_data: WhatsAppMessage):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for phone_number in message_data.phone_numbers:
        try:
            message = client.messages.create(
                from_=TWILIO_PHONE_NUMBER,  # Asegúrate de que el formato sea correcto
                body=message_data.message,
                to=f"whatsapp:{phone_number}"
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al enviar mensaje a {phone_number}: {e}")

    return {"message": f"Mensajes enviados exitosamente a {len(message_data.phone_numbers)} números"}



@appgestion.post("/incoming-messages")
async def incoming_messages(request: Request) -> str:  # Cambio: str como tipo de retorno
    # Validar la solicitud de Twilio (opcional)
    if not request_validator.validate(
        str(request.url), request.form, request.headers.get("X-Twilio-Signature")
    ):
        raise HTTPException(status_code=400, detail="Invalid request")

    # Obtener datos del mensaje entrante
    from_number = request.form["From"]
    message_body = request.form["Body"]

    # Procesar el mensaje (aquí va tu lógica de chatbot)
    response_message = "Gracias por tu mensaje. ¡Pronto te responderemos!"

    # Crear una respuesta TwiML
    twiml = MessagingResponse()
    twiml.message(response_message)

    # Devolver la respuesta TwiML como cadena de texto
    return str(twiml) 

# }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
# whatsapp


# }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}

# sms

# Credenciales de Twilio (reemplaza con tus datos)
account_sid = "AC38ebd1270f9b5f3014bbf31c066e0666"
auth_token = "67b1da453a3a73121f36b72043f7b27c"
twilio_phone_number = "+19253579993"

# Cliente de Twilio
client = Client(account_sid, auth_token)

# Modelo para los datos del SMS
class SMSData(BaseModel):
    recipients: List[int] | None = None
    message: str

# Ruta para enviar el SMS
@appgestion.post("/send_sms/")
async def send_sms(sms_data: SMSData, db: Session = Depends(get_db_pers)):
    recipients = sms_data.recipients  # Lista de IDs de personas a quienes enviar el SMS

    # Consulta para obtener los números de teléfono de los destinatarios
    phone_numbers = (
        db.query(PR_Detalle_Persona_base.PR_DetP_ch_tel)
        .filter(PR_Detalle_Persona_base.PR_DetP_id.in_(recipients))
        .all()
    )

    if not phone_numbers:
        raise HTTPException(status_code=404, detail="No se encontraron Contactos.")

    # Enviar SMS a cada número de teléfono
    for phone_number, in phone_numbers:  # Desempaquetamos la tupla (phone_number,)
        try:
            message = client.messages.create(
                body=sms_data.message,
                from_=twilio_phone_number,
                to=phone_number 
            )
            print(f"SMS enviado a {phone_number}: {message.sid}")
        except Exception as e:
            print(f"Error sending to {phone_number}: {e}")

    return {"message": f"Mensaje SMS enviados a {len(phone_numbers)} contacto."}
# }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}


# Reemplaza con tus credenciales de Telegram
TELEGRAM_API_TOKEN = '7104813241:AAHhCfbDYwiGpelUc7fWNziLf7aTLNunoyA'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage'
bot = Bot(token="7104813241:AAHhCfbDYwiGpelUc7fWNziLf7aTLNunoyA")

@appgestion.post("/send_message/")
async def send_message(user_id: int, message: str):
    # Envía el mensaje al usuario especificado
    await bot.send_message(chat_id=user_id, text=message)
    return {"status": "message sent"}
# }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}


# ***** LISTADO POR ID **********
@appTO1_rout_personas.get("/pi001TO1_personas_list_id/{personas_id}", response_model=PR_Persona_model)
def read_persona_by_id(personas_id: int, db: Session = Depends(get_db_pers)):
    persona = db.query(PR_Persona_base).filter(
        PR_Persona_base.PR_Per_in_id == personas_id, 
        PR_Persona_base.estado == True
    ).first()
    if not persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada")
    return persona

@appTO1_rout_personas.get("/pi001TO1_personasdetalle_list_id/{detalle_id}", response_model=List[PR_Detalle_Persona_model])
def read_persona_detalle_by_id(detalle_id: int, db: Session = Depends(get_db_pers)):
    detalles = db.query(PR_Detalle_Persona_base).filter(
        PR_Detalle_Persona_base.FK_PR_Pers == detalle_id, 
        PR_Detalle_Persona_base.estado == True
    ).all()
    if not detalles:
        raise HTTPException(status_code=404, detail="Detalles de persona no encontrados")
    return detalles

# ***** LISTADO GENERAL POR PAGINADO **********
@appTO1_rout_personas.get("/pi002TO1_personas_listget/", response_model=List[PR_Persona_model])
async def list_personas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_pers)):
    try:
        personas = db.query(PR_Persona_base).filter(
            PR_Persona_base.estado == True
        ).order_by(PR_Persona_base.PR_Per_in_id).offset(skip).limit(limit).all()
        return personas
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        db.close()

@appTO1_rout_personas.get("/pi002TO1_personasdetalle_listget/", response_model=List[PR_Detalle_Persona_model])
async def list_personas_detalle(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_pers)):
    try:
        detalles = db.query(PR_Detalle_Persona_base).filter(
            PR_Detalle_Persona_base.estado == True
        ).order_by(PR_Detalle_Persona_base.PR_DetP_id).offset(skip).limit(limit).all()
        return detalles
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        db.close()

# ***** CREAR PERSONAS **********
@appTO1_rout_personas.post("/pi003TO1_personas_add/", response_model=PR_Persona_model)
def create_persona(persona: PR_Persona_model, db: Session = Depends(get_db_pers)):
    try:
        persona_db = PR_Persona_base(**persona.dict())
        persona_db.date_create = datetime.now()
        persona_db.date_update = datetime.now()
        db.add(persona_db)
        db.commit()
        db.refresh(persona_db)
        return persona_db
    except Exception as e:
        db.rollback()
        error_detail = {"error": "Error al agregar Persona", "error_message": str(e)}
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)

@appTO1_rout_personas.post("/pi003TO1_personasdetalle_add/", response_model=PR_Detalle_Persona_model)
def create_persona_detalle(detalle: PR_Detalle_Persona_model, db: Session = Depends(get_db_pers)):
    try:
        detalle_db = PR_Detalle_Persona_base(**detalle.dict())
        detalle_db.date_create = datetime.now()
        detalle_db.date_update = datetime.now()
        db.add(detalle_db)
        db.commit()
        db.refresh(detalle_db)
        return detalle_db
    except Exception as e:
        db.rollback()
        error_detail = {"error": "Error al agregar Detalle de Persona", "error_message": str(e)}
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)

# ***** ACTUALIZAR PERSONA **********
@appTO1_rout_personas.put("/pi005TO1_personas_update/{personas_id}", response_model=PR_Persona_model)
def update_persona(personas_id: int, persona: PR_Persona_model, db: Session = Depends(get_db_pers)):
    try:
        persona_db = db.query(PR_Persona_base).filter(
            PR_Persona_base.PR_Per_in_id == personas_id,
            PR_Persona_base.estado == True
        ).first()

        if not persona_db:
            raise HTTPException(status_code=404, detail="Persona no encontrada")

        for field, value in persona.dict(exclude_unset=True).items():
            setattr(persona_db, field, value)

        persona_db.date_update = datetime.now()
        db.commit()
        db.refresh(persona_db)
        return persona_db
    except Exception as e:
        db.rollback()
        error_detail = {"error": "Error al actualizar Persona", "error_message": str(e)}
        raise HTTPException(status_code=500, detail=error_detail)
    finally:
        db.close()

@appTO1_rout_personas.put("/pi005TO1_personasdetalle_update/{detalle_id}", response_model=PR_Detalle_Persona_model)
def update_persona_detalle(detalle_id: int, detalle: PR_Detalle_Persona_model, db: Session = Depends(get_db_pers)):
    try:
        detalle_db = db.query(PR_Detalle_Persona_base).filter(
            PR_Detalle_Persona_base.PR_DetP_id == detalle_id,
            PR_Detalle_Persona_base.estado == True
        ).first()

        if not detalle_db:
            raise HTTPException(status_code=404, detail="Detalle de persona no encontrado")

        for field, value in detalle.dict(exclude_unset=True).items():
            setattr(detalle_db, field, value)

        detalle_db.date_update = datetime.now()
        db.commit()
        db.refresh(detalle_db)
        return detalle_db
    except Exception as e:
        db.rollback()
        error_detail = {"error": "Error al actualizar Detalle de Persona", "error_message": str(e)}
        raise HTTPException(status_code=500, detail=error_detail)
    finally:
        db.close()

# ***** ELIMINAR PERSONA **********
@appTO1_rout_personas.delete("/pi004TO1_personas_delete/{personas_id}", response_model=dict)
def delete_persona(personas_id: int, db: Session = Depends(get_db_pers)):
    try:
        persona_db = db.query(PR_Persona_base).filter(
            PR_Persona_base.PR_Per_in_id == personas_id,
            PR_Persona_base.estado == True
        ).first()

        if not persona_db:
            raise HTTPException(status_code=404, detail="Persona no encontrada")

        persona_db.estado = False
        persona_db.date_delete = datetime.now()
        db.commit()
        return {"message": "Persona eliminada"}
    except Exception as e:
        db.rollback()
        error_detail = {"error": "Error al eliminar Persona", "error_message": str(e)}
        raise HTTPException(status_code=500, detail=error_detail)
    finally:
        db.close()
        
@appTO1_rout_personas.get("/pi002T01_personas_listget_inactive/", response_model=List[PR_Persona_model])
async def list_personas_inactive(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_pers)):
    try:
        # Consulta para obtener personas con estado inactivo (estado == 0)
        personas = (
            db.query(PR_Persona_base)
            .filter(PR_Persona_base.estado == 0)
            .options(joinedload(PR_Persona_base.per_detalle_persona))
            .order_by(PR_Persona_base.PR_Per_in_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

        # Combinar los datos de personas y detalles en una lista de diccionarios
        personas_con_detalles = []
        for persona in personas:
            detalle = persona.per_detalle_persona 
            persona_dict = persona.__dict__
            if detalle:
                persona_dict.update(detalle.__dict__)

            personas_con_detalles.append(persona_dict)

        return personas_con_detalles
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        db.close()
        
from sqlalchemy import update

@appTO1_rout_personas.put("/pi002T01_personas_update_estado/", response_model=dict)
async def update_personas_estado(personas_ids: List[int], db: Session = Depends(get_db_pers)):
    try:
        # Actualizar estado y fecha de actualización
        db.execute(
            update(PR_Persona_base)
            .filter(PR_Persona_base.PR_Per_in_id.in_(personas_ids))
            .values(estado=1, date_update=datetime.now())
        )

        db.commit()
        return {"message": "Estado de personas actualizado"}

    except Exception as e:
        db.rollback()
        error_detail = {"error": "Error al actualizar el estado de personas", "error_message": str(e)}
        raise HTTPException(status_code=500, detail=error_detail)

    finally:
        db.close()

@appTO1_rout_personas.delete("/pi004TO1_personasdetalle_delete/{detalle_id}", response_model=dict)
def delete_persona_detalle(detalle_id: int, db: Session = Depends(get_db_pers)):
    try:
        detalle_db = db.query(PR_Detalle_Persona_base).filter(
            PR_Detalle_Persona_base.PR_DetP_id == detalle_id,
            PR_Detalle_Persona_base.estado == True
        ).first()

        if not detalle_db:
            raise HTTPException(status_code=404, detail="Detalle de persona no encontrado")

        detalle_db.estado = False
        detalle_db.date_delete = datetime.now()
        db.commit()
        return {"message": "Detalle de Persona eliminado"}
    except Exception as e:
        db.rollback()
        error_detail = {"error": "Error al eliminar Detalle de Persona", "error_message": str(e)}
        raise HTTPException(status_code=500, detail=error_detail)
    finally:
        db.close()


#---- Usuario---

# ***** LISTADO POR ID **********
@app_rout_usuarios.get("/pi001TO1_usuario_list_id/{usuario_id}", response_model=PR_Usuario_model)
def read_usuario_by_id(usuario_id: int, db: Session = Depends(get_db_user)):
    usuario = db.query(PR_Usuario_base).filter(
        PR_Usuario_base.PR_Usu_in_id == usuario_id,
        PR_Usuario_base.estado == True
    ).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Detalle de usuario no ubicado")
    return usuario

# ***** LISTADO GENERAL POR PAGINADO **********
@app_rout_usuarios.get("/pi002TO1_usuario_listget/", response_model=List[PR_Usuario_model])
async def list_usuario(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_user)):
    try:
        usuarios = db.query(PR_Usuario_base).filter(
            PR_Usuario_base.estado == True
        ).order_by(PR_Usuario_base.PR_Usu_in_id).offset(skip).limit(limit).all()
        return usuarios
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        db.close()

# ***** CREAR usuario  **********
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    roles: List[str] = []

# Nuevo endpoint para agregar usuarios
# ***** AGREGAR USUARIO **********
@app_rout_usuarios.post("/pi003TO1_usuario_add/")
def api30a_alerv_add(usuario: PR_Usuario_model, db: Session = Depends(get_db_user), current_user: User = Depends(get_current_user)):
    try:
        hashed_password = pwd_context.hash(usuario.PR_Usu_ch_pass)
        usuario.PR_Usu_ch_pass = hashed_password

        usuario_db = PR_Usuario_base(**usuario.dict())
        db.add(usuario_db)
        db.commit()
        db.refresh(usuario_db)

        return usuario_db

    except Exception as e:
        error_detail = {"error": "Error al agregar usuario", "error_message": str(e)}
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)
    
    try:
        hashed_password = pwd_context.hash(usuario.PR_Usu_ch_pass)
        usuario.PR_Usu_ch_pass = hashed_password

        usuario_db = PR_Usuario_base(**usuario.dict())
        db.add(usuario_db)
        db.commit()
        db.refresh(usuario_db)

        return usuario_db

    except Exception as e:
        error_detail = {"error": "Error al agregar usuario", "error_message": str(e)}
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)
    

from fastapi import HTTPException

# ***** ACTUALIZAR USUARIO **********
@app_rout_usuarios.put("/pi005TO1_usuario_update/{usuario_id}", response_model=PR_Usuario_model)
def update_usuario(usuario_id: int, usuarios: PR_Usuario_model, db: Session = Depends(get_db_user)):
    try:
        # Buscar el usuario por su ID
        usuario_db = db.query(PR_Usuario_base).filter(
            PR_Usuario_base.PR_Usu_in_id == usuario_id,
            PR_Usuario_base.estado == True
        ).first()

        if not usuario_db:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Actualizar los campos proporcionados en la solicitud
        for field, value in usuarios.dict(exclude_unset=True).items():
            setattr(usuario_db, field, value)

        # Guardar los cambios en la base de datos
        db.commit()
        db.refresh(usuario_db)

        return usuario_db

    except Exception as e:
        # En caso de errores, revertir los cambios y levantar una excepción HTTP
        db.rollback()
        error_detail = {"error": "Error al actualizar usuario", "error_message": str(e)}
        raise HTTPException(status_code=500, detail=error_detail)

    finally:
        # Cerrar la conexión a la base de datos al finalizar
        db.close()

# ***** ELIMINAR USUARIO **********
@app_rout_usuarios.delete("/pi004TO1_usuarios_delete/{usuario_id}", response_model=dict)
def delete_usuario(usuario_id: int, db: Session = Depends(get_db_user)):
    usuario_db = db.query(PR_Usuario_base).filter(PR_Usuario_base.PR_Usu_in_id == usuario_id).first()
    if usuario_db:
        # Cambiar el estado del usuario a False en lugar de eliminar físicamente
        usuario_db.estado = False
        db.commit()
        return {"message": "Usuario eliminado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

#**********************LISTA DE USUARIOS INACTIVOS***************
@app_rout_usuarios.get("/usuario_listget_inactive/", response_model=List[PR_Usuario_model])
async def list_usuarios_inactive(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_user)):
    try:
        # Consulta para obtener usuarios con estado inactivo (estado == 0)
        usuarios = (
            db.query(PR_Usuario_base)
            .filter(PR_Usuario_base.estado == 0)
            .order_by(PR_Usuario_base.PR_Usu_in_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return usuarios
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        db.close()
        
#********************* ACTUALIZAR ESTADO**************
@app_rout_usuarios.put("/usuario_update_estado/", response_model=dict)
async def update_usuarios_estado(usuarios_ids: List[int], db: Session = Depends(get_db_user)):
    try:
        # Actualizar estado y fecha de actualización
        db.execute(
            update(PR_Usuario_base)
            .filter(PR_Usuario_base.PR_Usu_in_id.in_(usuarios_ids))
            .values(estado=1, date_update=datetime.now())
        )

        db.commit()
        return {"message": "Estado de usuarios actualizado"}

    except Exception as e:
        db.rollback()
        error_detail = {"error": "Error al actualizar el estado de usuarios", "error_message": str(e)}
        raise HTTPException(status_code=500, detail=error_detail)

    finally:
        db.close()
# ----------------------------------------------------------

# ***** CREAR ROL  **********
@app_rout_rol.post("/pi003TO1_rol_add/")
def api30a_alerv_add(rol: PR_Rol_model, db: Session = Depends(get_db_user)):
    try:
        rol_db = PR_Rol_base(**rol.dict())
        db.add(rol_db)
        db.commit()
        db.refresh(rol_db)
        return rol_db

    except Exception as e:
        # En caso de otros errores, levanta una excepción HTTP con código de estado 500 (Internal Server Error)
        error_detail = {"error": "Error al agregar rol", "error_message": str(e)}
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)


@app_rout_rol.post("/pi003TO1_perfil_add/")
def api30a_alerv_add(perfil: PR_Perfil_model, db: Session = Depends(get_db_user)):
    try:
        perfil_db = PR_Perfil_base(**perfil.dict())
        db.add(perfil_db)
        db.commit()
        db.refresh(perfil_db)
        return perfil_db

    except Exception as e:
        # En caso de otros errores, levanta una excepción HTTP con código de estado 500 (Internal Server Error)
        error_detail = {"error": "Error al agregar rol", "error_message": str(e)}
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)


from fastapi import HTTPException


# Obtener perfil por ID
@app_rout_rol.get("/perfiles/{perfil_id}", response_model=PR_Perfil_model)
def get_perfil(perfil_id: int, db: Session = Depends(get_db_user)):
    perfil = db.query(PR_Perfil_base).filter(PR_Perfil_base.PR_Usu_perf_id == perfil_id).first()
    if not perfil:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    return perfil

# Obtener rol por ID
@app_rout_rol.get("/roles/{rol_id}", response_model=PR_Rol_model)
def get_rol(rol_id: int, db: Session = Depends(get_db_user)):
    rol = db.query(PR_Rol_base).filter(PR_Rol_base.PR_Usu_rol_id == rol_id).first()
    if not rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol
              
@app_rout_rol.get("/roles_listget/", response_model=List[PR_Rol_model])
async def list_rol(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_user)):
    try:
        rol = db.query(PR_Rol_base).order_by(PR_Rol_base.PR_Usu_rol_id) \
                                                .offset(skip) \
                                                .limit(limit) \
                                                .all()
        return rol
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        db.close()

@app_rout_rol.get("/perfil_listget/", response_model=List[PR_Perfil_model])
async def list_prefil(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_user)):
    try:
        rol = db.query(PR_Perfil_base).order_by(PR_Perfil_base.PR_Usu_perf_id) \
                                                .offset(skip) \
                                                .limit(limit) \
                                                .all()
        return rol
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        db.close()
        
        
@app_rout_rol.put("/roles_update/{rol_id}", response_model=PR_Rol_model)
def update_rol(rol_id: int, roles: PR_Rol_model, db: Session = Depends(get_db_user)):
    try:
        # Buscar el rol por su ID
        rol_db = db.query(PR_Rol_base).filter(
            PR_Rol_base.PR_Usu_rol_id == rol_id
        ).first()

        if not rol_db:
            raise HTTPException(status_code=404, detail="rol no encontrada")

        # Actualizar los campos proporcionados en la solicitud
        for field, value in roles.dict(exclude_unset=True).items():
            setattr(rol_db, field, value)

        # usuario_db. = datetime.now()
        
        # Guardar los cambios en la base de datos
        db.commit()
        db.refresh(rol_db)

        return rol_db

    except Exception as e:
        # En caso de errores, revertir los cambios y levantar una excepción HTTP
        db.rollback()
        error_detail = {"error": "Error al actualizar Usuario", "error_message": str(e)}
        raise HTTPException(status_code=500, detail=error_detail)

    finally:
        # Cerrar la conexión a la base de datos al finalizar
        db.close()
        
        
@app_rout_rol.put("/perfiles_update/{perfil_id}", response_model=PR_Perfil_model)
def update_perfil(perfil_id: int, perfiles: PR_Perfil_model, db: Session = Depends(get_db_user)):
    try:
        # Buscar el rol por su ID
        perfil_db = db.query(PR_Perfil_base).filter(
            PR_Perfil_base.PR_Usu_perf_id == perfil_id
        ).first()

        if not perfil_db:
            raise HTTPException(status_code=404, detail="rol no encontrada")

        # Actualizar los campos proporcionados en la solicitud
        for field, value in perfiles.dict(exclude_unset=True).items():
            setattr(perfil_db, field, value)

        # usuario_db. = datetime.now()
        
        # Guardar los cambios en la base de datos
        db.commit()
        db.refresh(perfil_db)

        return perfil_db

    except Exception as e:
        # En caso de errores, revertir los cambios y levantar una excepción HTTP
        db.rollback()
        error_detail = {"error": "Error al actualizar Usuario", "error_message": str(e)}
        raise HTTPException(status_code=500, detail=error_detail)

    finally:
        # Cerrar la conexión a la base de datos al finalizar
        db.close()
        
                
############## GRUPOS ###################

@app_rout_grupo.get("/grupos_list_id/{grupos_id}", response_model=PR_grupos_model)
def get_grupo(grupos_id: int, db: Session = Depends(get_db_grup)):
    grupo = db.query(PR_grupos_base).filter(PR_grupos_base.PR_Gru_ch_nomb  == grupos_id).first()
    if not grupo:
        raise HTTPException(status_code=404, detail="grupo no encontrado")
    return grupo

@app_rout_grupo.get("/grupos_listget/", response_model=List[PR_grupos_model])
async def list_grupos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db_grup)):
    try:
        grupos = db.query(PR_grupos_base).order_by(PR_grupos_base.PR_Gru_id).offset(skip).limit(limit).all()
        return grupos
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error en el servidor: {str(e)}")
    finally:
        db.close()

@app_rout_grupo.post("/grupos_add/", response_model=PR_grupos_model)
def api30a_alerv_add(grupo: PR_grupos_model, db: Session = Depends(get_db_grup)):
    try:
        grupo_db = PR_grupos_base(**grupo.dict())
        db.add(grupo_db)
        db.commit()
        db.refresh(grupo_db)
        return grupo_db
    except Exception as e:
        error_detail = {"error": "Error al agregar rol", "error_message": str(e)}
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_detail)

@app_rout_grupo.put("/grupos_update/{grupos_id}", response_model=PR_grupos_model)
def update_grupo(grupos_id: int, grupos: PR_grupos_model, db: Session = Depends(get_db_grup)):
    try:
        grupo_db = db.query(PR_grupos_base).filter(PR_grupos_base.PR_Gru_id == grupos_id).first()
        if not grupo_db:
            raise HTTPException(status_code=404, detail="grupo no encontrada")

        for field, value in grupos.dict(exclude_unset=True).items():
            setattr(grupo_db, field, value)

        db.commit()
        db.refresh(grupo_db)
        return grupo_db
    except Exception as e:
        db.rollback()
        error_detail = {"error": "Error al actualizar Usuario", "error_message": str(e)}
        raise HTTPException(status_code=500, detail=error_detail)
    finally:
        db.close()

@app_rout_grupo.delete("/grupos_delete/{grupos_id}", response_model=dict)
def delete_grupo(grupos_id: int, db: Session = Depends(get_db_grup)):
    try:
        grupo_db = db.query(PR_grupos_base).filter(PR_grupos_base.PR_Gru_id == grupos_id).first()
        if not grupo_db:
            raise HTTPException(status_code=404, detail="Grupo no encontrado")

        grupo_db.estado = False
        grupo_db.date_delete = datetime.now()
        db.commit()
        return {"message": "Grupo eliminado"}
    except Exception as e:
        db.rollback()
        error_detail = {"error": "Error al eliminar Grupo", "error_message": str(e)}
        raise HTTPException(status_code=500, detail=error_detail)
    finally:
        db.close()
    try:
        grupo_db = db.query(PR_grupos_base).filter(
            PR_grupos_base.PR_Gru_id == grupos_id,
            # PR_grupos_base.estado == True
        ).first()

        if not grupo_db:
            raise HTTPException(status_code=404, detail="Grupo no encontrada")

        grupo_db.estado = False
        grupo_db.date_delete = datetime.now()
        db.commit()
        return {"message": "Grupo eliminado"}
    except Exception as e:
        db.rollback()
        error_detail = {"error": "Error al eliminar Grupo", "error_message": str(e)}
        raise HTTPException(status_code=500, detail=error_detail)
    finally:
        db.close()