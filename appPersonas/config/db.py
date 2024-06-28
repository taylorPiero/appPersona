
# import pydoc
# from sqlalchemy import create_engine


# direccion_servidor_local = 'LAPTOP-HBEP190U\SQLEXPRESS2017'
# nombre_base_de_datos_local = 'dbpersonas'  # Nombre de tu base de datos local
# nombre_usuario_local = 'nluis'  # Tu usuario local
# password_local = '123456'  # Tu contraseña local



# # Configurar URL de conexión
# DB_SQLALCHEMY_URL_PERSONAS_ASIS = f"mssql+pyodbc://{nombre_usuario_local}:{password_local}@{direccion_servidor_local}/{nombre_base_de_datos_local}?driver=ODBC+Driver+17+for+SQL+Server"
# engine_SQLS_alertaV_local = create_engine(DB_SQLALCHEMY_URL_PERSONAS_ASIS, echo=True)

# config/db.py
# import pyodbc
# from sqlalchemy import create_engine

# from env.libfun.funciones_conexion import conexion_obtener_ip_activa

# direcciones_ip = ["192.168.196.28"]
# ip_activa = conexion_obtener_ip_activa(direcciones_ip)

# direccion_servidor = '192.168.88.250'
# direccion_servidor2 = ip_activa
# CDB_TO1_PLACAS_ASIS = 'PRA_PERS_20'
# nombre_usuario = 'uspracticantes'
# password = 'practica.2024.I'


# # Configurar URL de conexión a la base de datos de AlertaV
# DB_SQLALCHEMY_URL_PRA_PERS_20 = f"mssql+pyodbc://{nombre_usuario}:{password}@{direccion_servidor2}/{CDB_TO1_PLACAS_ASIS}?driver=ODBC+Driver+17+for+SQL+Server"
# engine_SQLS_alertaV = create_engine(DB_SQLALCHEMY_URL_PRA_PERS_20, echo=True)

from sqlalchemy import create_engine
import pyodbc
# Función para obtener la IP activa (asegúrate de definirla correctamente)
from env.libfun.funciones_conexion import conexion_obtener_ip_activa

# Direcciones IP y credenciales (reemplaza con tus valores reales)
direcciones_ip = ["192.168.196.28"]
ip_activa = conexion_obtener_ip_activa(direcciones_ip)
direccion_servidor = ip_activa
nombre_usuario = 'uspracticantes'
password = 'practica.2024.I'

# Nombres de las bases de datos
CDB_PRACTICAS_GRUPOS = 'DB_PRACTICAS_GRUPOS'
CDB_PRACTICAS_MENSAJE = 'DB_PRACTICAS_MENSAJE'
CDB_PRACTICAS_PERSONA = 'DB_PRACTICAS_PERSONA'
CDB_PRACTICAS_USUARIO = 'DB_PRACTICAS_USUARIO'

# Configurar URLs de conexión para cada base de datos
DB_URLS = {
    "grupos": f"mssql+pyodbc://{nombre_usuario}:{password}@{direccion_servidor}/{CDB_PRACTICAS_GRUPOS}?driver=ODBC+Driver+17+for+SQL+Server",
    "mensaje": f"mssql+pyodbc://{nombre_usuario}:{password}@{direccion_servidor}/{CDB_PRACTICAS_MENSAJE}?driver=ODBC+Driver+17+for+SQL+Server",
    "persona": f"mssql+pyodbc://{nombre_usuario}:{password}@{direccion_servidor}/{CDB_PRACTICAS_PERSONA}?driver=ODBC+Driver+17+for+SQL+Server",
    "usuario": f"mssql+pyodbc://{nombre_usuario}:{password}@{direccion_servidor}/{CDB_PRACTICAS_USUARIO}?driver=ODBC+Driver+17+for+SQL+Server",
}

# Crear motores de SQLAlchemy para cada conexión
engines = {key: create_engine(url, echo=True) for key, url in DB_URLS.items()}

# Ahora puedes usar `engines['grupos']`, `engines['mensaje']`, etc. para interactuar con cada base de datos
