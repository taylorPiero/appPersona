# from tkinter import CHAR, NUMERIC
# from unicodedata import numeric
# from click import FLOAT
# from sqlalchemy.exc import SQLAlchemyError
# from fastapi import FastAPI, HTTPException,APIRouter,Depends,status, Form, BackgroundTasks, Request
# from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData,ForeignKey, Float,Numeric,func, Date
# from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship
# from datetime import datetime, timedelta
# from typing import List,Dict,Optional
# from dotenv import load_dotenv
# from pydantic import BaseModel
# from appPersonas.config.db import sessions
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import JSONResponse
# from pydantic import ConfigDict
# from sqlalchemy.exc import IntegrityError
# from appPersonas.database.database_models import p_per_pers_base, p_rol_pers_base, p_usuarios_pers_base
# from appPersonas.database.models import p_per_pers_model, p_rol_pers_model, p_usuarios_pers_model, TelegramUpdateModel
# import telegram
# import os
# from jose import JWTError, jwt
# from pydantic import BaseModel, EmailStr, Field
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# import sqlite3
# from sqlalchemy.ext.declarative import declarative_base

# from telegram import Bot
# import requests


# from twilio.twiml.messaging_response import MessagingResponse
# from twilio.request_validator import RequestValidator


# from telegram.constants import ParseMode
# from telegram.ext import Updater,ApplicationBuilder

# from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

# from google.oauth2 import service_account
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build
# from twilio.rest import Client
# from twilio.base.exceptions import TwilioRestException
# from fastapi.templating import Jinja2Templates
# import pywhatkit as kit



# engine_personas = create_engine(DB_SQLALCHEMY_URL_PRA_PERS_20)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_personas)
 
# appTO1_rout_personas = APIRouter()
# app_rout_usuarios = APIRouter()
# app_rout_rol = APIRouter()
# appgestion = APIRouter()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()  



# # # }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
# # # whatsapp


# # # load_dotenv()  # Cargar variables de entorno desde .env


# # # Credenciales de Twilio (deben estar en tu archivo .env)
# # TWILIO_ACCOUNT_SID = 'ACca03a3c9d31e0a6d05b196d75a97d3fb'
# # TWILIO_AUTH_TOKEN = 'b139d0a41bd657ba19429b8acd7a0e32'
# # TWILIO_PHONE_NUMBER = 'whatsapp:+14155238886'  # Reemplaza con tu número de WhatsApp de Twilio
                                
# # # Validador de solicitudes de Twilio (opcional, pero recomendado)
# # request_validator = RequestValidator(TWILIO_AUTH_TOKEN)

# # # Modelo Pydantic para la solicitud de envío de mensajes
# # class WhatsAppMessage(BaseModel):
# #     phone_numbers: list[str] = Field(..., description="Lista de números de teléfono (con código de país)")
# #     message: str = Field(..., description="Mensaje a enviar")

# # # ... (otras importaciones)

# # @appgestion.post("/send_whatsapp_message")
# # async def send_whatsapp_message(message_data: WhatsAppMessage):
# #     client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# #     for phone_number in message_data.phone_numbers:
# #         try:
# #             message = client.messages.create(
# #                 from_=TWILIO_PHONE_NUMBER,  # Asegúrate de que el formato sea correcto
# #                 body=message_data.message,
# #                 to=f"whatsapp:{phone_number}"
# #             )
# #         except Exception as e:
# #             raise HTTPException(status_code=500, detail=f"Error al enviar mensaje a {phone_number}: {e}")

# #     return {"message": f"Mensajes enviados exitosamente a {len(message_data.phone_numbers)} números"}



# # @appgestion.post("/incoming-messages")
# # async def incoming_messages(request: Request) -> str:  # Cambio: str como tipo de retorno
# #     # Validar la solicitud de Twilio (opcional)
# #     if not request_validator.validate(
# #         str(request.url), request.form, request.headers.get("X-Twilio-Signature")
# #     ):
# #         raise HTTPException(status_code=400, detail="Invalid request")

# #     # Obtener datos del mensaje entrante
# #     from_number = request.form["From"]
# #     message_body = request.form["Body"]

# #     # Procesar el mensaje (aquí va tu lógica de chatbot)
# #     response_message = "Gracias por tu mensaje. ¡Pronto te responderemos!"

# #     # Crear una respuesta TwiML
# #     twiml = MessagingResponse()
# #     twiml.message(response_message)

# #     # Devolver la respuesta TwiML como cadena de texto
# #     return str(twiml) 

# # # }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
# # # whatsapp





# # }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
# # sms


# # Credenciales de Twilio (reemplaza con tus datos)
# account_sid = "AC5e3c38947ce0875326f782aa231d9428"
# auth_token = "b86a78c0ff515e173c951d985bd829b3"
# twilio_phone_number = "+15673473872"

# # Cliente de Twilio
# client = Client(account_sid, auth_token)

# # Modelo para los datos del SMS
# class SMSData(BaseModel):
#     recipients: List[str]
#     message: str


# # Ruta para enviar el SMS

# @appgestion.post("/send_sms ..../")
# async def send_sms(sms_data: SMSData, db: Session = Depends(get_db)):
#     # Verificar si hay destinatarios
#     if not p_usuarios_pers_base.usu_ch_telf_pers:
#         raise HTTPException(status_code=400, detail="No recipients provided.")

#     # Obtener números de teléfono de los usuarios seleccionados (o todos)
#     if p_usuarios_pers_base.usu_ch_telf_pers == ["all"]:
#         # Consulta a tu base de datos para obtener todos los números de teléfono
#         phone_numbers = db.query(p_usuarios_pers_base).filter(p_usuarios_pers_base.active == True).all() 
#     else:
#         # Filtrar números de teléfono específicos en la base de datos
#         phone_numbers = db.query(p_usuarios_pers_base).filter(p_usuarios_pers_base.usu_ch_telf_pers.in_(sms_data.recipients)).all()
    
#     if not phone_numbers:
#         raise HTTPException(status_code=400, detail="Invalid phone number.")
    
#     # Enviar SMS a cada destinatario
#     for user in phone_numbers:
#         try:
#             message = client.messages.create(
#                 body=sms_data.message,
#                 from_=twilio_phone_number,
#                 to=user.usu_ch_telf_pers  # Usar el número del usuario
#             )
#             print(f"SMS sent to {user.usu_ch_telf_pers}: {message.sid}")
#         except TwilioRestException as e:
#             print(f"Error sending to {user.usu_ch_telf_pers}: {e}")
    
#     return {"message": "SMS messages sent successfully"}

# # @appgestion.post("/send_sms/")
# # async def send_sms(sms_data: SMSData):
# #     try:
# #         message = client.messages.create(
# #             body=sms_data.message,
# #             from_=twilio_phone_number,
# #             to=sms_data.to
# #         )
# #         return {"message_sid": message.sid}
# #     except TwilioRestException as e:
# #         raise HTTPException(status_code=400, detail=f"Twilio Error: {e}")


# # }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}





# # }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}
# # email


# # Configuración de la conexión SMTP
# conf = ConnectionConfig(
#     MAIL_USERNAME="luisneyra143@gmail.com",  # Reemplaza con tu correo
#     MAIL_PASSWORD="gegoiixulecoqdmu",       # Reemplaza con tu contraseña
#     MAIL_FROM="luisneyra143@gmail.com",
#     MAIL_PORT=587,  # o 465 si usas SSL/TLS
#     MAIL_SERVER="smtp.gmail.com",
#     MAIL_STARTTLS=True,  # Si usas STARTTLS (normalmente con puerto 587)
#     MAIL_SSL_TLS=False,  # Si usas SSL/TLS (normalmente con puerto 465)
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True
# )

# # Modelo para los datos del correo
# class EmailSchema(BaseModel):
#     user_ids: list[int] | None = None  # Lista de IDs de usuario o None para todos
#     subject: str
#     body: str

# # Ruta para enviar el correo
# @appgestion.post("/email")
# async def send_email(
#     email: EmailSchema,
#     background_tasks: BackgroundTasks,
#     db: Session = Depends(get_db),
# ):
#     if email.user_ids is None:
#         # Enviar a todos los usuarios
#         recipients = db.query(p_usuarios_pers_base.usu_ch_mail_pers).all()
#     else:
#         # Enviar solo a los seleccionados
#         recipients = (
#             db.query(p_usuarios_pers_base.usu_ch_mail_pers)
#             .filter(p_usuarios_pers_base.usu_in_idpk_pers.in_(email.user_ids))
#             .all()
#         )

#     # Extraer los correos electrónicos de los resultados de la consulta
#     recipients = [email[0] for email in recipients]

#     message = MessageSchema(
#         recipients=recipients,
#         subject=email.subject,
#         body=email.body,
#         subtype="plain",
#     )

#     fm = FastMail(conf)  # Configurar FastMail con la opción elegida (contraseña o OAuth2)
#     background_tasks.add_task(fm.send_message, message)

#     return {"message": f"Email sent to {len(recipients)} recipients in background"}
# # fin email
# # }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}



# # Reemplaza con tus credenciales de Telegram
# TELEGRAM_API_TOKEN = '7104813241:AAHhCfbDYwiGpelUc7fWNziLf7aTLNunoyA'
# TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage'
# bot = Bot(token="7104813241:AAHhCfbDYwiGpelUc7fWNziLf7aTLNunoyA")

# @appgestion.post("/send_message/")
# async def send_message(user_id: int, message: str):
#     # Envía el mensaje al usuario especificado
#     await bot.send_message(chat_id=user_id, text=message)
#     return {"status": "message sent"}
# # }}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}


