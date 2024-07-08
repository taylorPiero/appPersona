# whatsapp.py
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import urllib.parse
import webbrowser
import time
import pyautogui
import logging

router = APIRouter()

# Modelo Pydantic para la solicitud
class WhatsAppMessage(BaseModel):
    phone_numbers: list[str]
    message: str

# Función para enviar mensajes de WhatsApp
def enviar_mensaje_whatsapp(telefono, texto):
    try:
        mensaje = f"https://wa.me/{telefono}?text={urllib.parse.quote(texto)}"
        webbrowser.open(mensaje)
        time.sleep(10)  # Espera de 10 segundos para asegurar que la página (WhatsApp) se cargue completamente
        pyautogui.press('enter')  # Enviar el mensaje automáticamente dando ENTER
    except Exception as e:
        logging.error(f"Error al enviar mensaje a {telefono}: {e}")

# Endpoint para enviar mensajes de WhatsApp
@router.post("/send_whatsapp_messages")
async def send_whatsapp_messages(whatsapp_message: WhatsAppMessage, background_tasks: BackgroundTasks):
    if not whatsapp_message.phone_numbers:
        raise HTTPException(status_code=400, detail="La lista de números de teléfono no puede estar vacía.")

    for telefono in whatsapp_message.phone_numbers:
        background_tasks.add_task(enviar_mensaje_whatsapp, telefono, whatsapp_message.message)
        time.sleep(15)  # Pausa entre mensajes para evitar bloqueos por actividad sospechosa

    return {"message": "Mensajes enviados en segundo plano"}
