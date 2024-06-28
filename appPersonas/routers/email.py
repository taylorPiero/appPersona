from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from fastapi import FastAPI, HTTPException,APIRouter,Depends,status, Form, BackgroundTasks, Request

from appPersonas.database.database_models import PR_Persona_base, PR_Detalle_Persona_base, PR_Parametro_Persona_base, PR_Rol_base, PR_Perfil_base, PR_Usuario_base, PR_grupos_base, PR_segmentos_base, PR_TMensaje_base, PR_DetalleMensaje_base, Pr_Archivos_base
from appPersonas.database.models import PR_Persona_model
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from appPersonas.config.db import engines

from pydantic import BaseModel

SessionLocal_pers = sessionmaker(autocommit=False, autoflush=False, bind=engines['persona'])

def get_db_pers():
    db = SessionLocal_pers()
    try:
        yield db
    finally:
        db.close()

app_email=APIRouter()

# Configuración de la conexión SMTP
conf = ConnectionConfig(
    MAIL_USERNAME="luisneyra143@gmail.com",  # Reemplaza con tu correo
    MAIL_PASSWORD="gegoiixulecoqdmu",       # Reemplaza con tu contraseña
    MAIL_FROM="luisneyra143@gmail.com",
    MAIL_PORT=587,  # o 465 si usas SSL/TLS
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,  # Si usas STARTTLS (normalmente con puerto 587)
    MAIL_SSL_TLS=False,  # Si usas SSL/TLS (normalmente con puerto 465)
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

# Modelo para los datos del correo
class EmailSchema(BaseModel):
    user_ids: list[int] | None = None  # Lista de IDs de usuario o None para todos
    subject: str
    body: str

# Ruta para enviar el correo
@app_email.post("/email")
async def send_email(
    email: EmailSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db_pers),
):
    if email.user_ids is None:
        # Enviar a todos los usuarios
        recipients = db.query(PR_Detalle_Persona_base.PR_DetP_ch_email).all()
    else:
        # Enviar solo a los seleccionados
        recipients = (
            db.query(PR_Detalle_Persona_base.PR_DetP_ch_email)
            .filter(PR_Detalle_Persona_base.PR_DetP_id.in_(email.user_ids))
            .all()
        )

    # Extraer los correos electrónicos de los resultados de la consulta
    recipients = [email[0] for email in recipients]

    message = MessageSchema(
        recipients=recipients,
        subject=email.subject,
        body=email.body,
        subtype="plain",
    )

    fm = FastMail(conf)  # Configurar FastMail con la opción elegida (contraseña o OAuth2)
    background_tasks.add_task(fm.send_message, message)

    return {"message": f"Email sent to {len(recipients)} recipients in background"}