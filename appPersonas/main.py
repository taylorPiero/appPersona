from fastapi import FastAPI,APIRouter
from fastapi.middleware import Middleware

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine,Float
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from .routers.appT01Persona import appTO1_rout_personas as apiT01_personas, app_rout_usuarios, app_rout_rol, appgestion
from .routers.login import logins
from .routers.email import app_email
from spyne import Application, rpc, ServiceBase, Unicode, AnyDict, Fault
import pytz
load_dotenv()

app = FastAPI()
# Set the default response class
# Configuración regional y zona horaria para Perú

# Configuración regional y zona horaria por defecto
DEFAULT_REGION = "es_PE"
DEFAULT_TIMEZONE = "America/Lima"
# Dependencia para obtener la zona horaria
def get_default_timezone():
    return pytz.timezone(DEFAULT_TIMEZONE)


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://localhost:5005",
    "http://190.117.85.58:5005",
    "http://192.168.1.45:5005",

]
# Create a Spyne application
# Allow these methods to be used
methods = ["GET", "POST", "PUT", "DELETE"]

# Only these headers are allowed
headers = ["Content-Type", "Authorization"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
    
)

app.include_router(logins, prefix="/auth")
app.include_router(app_email)
app.include_router(appgestion)
app.include_router(apiT01_personas)
app.include_router(app_rout_usuarios)
app.include_router(app_rout_rol)