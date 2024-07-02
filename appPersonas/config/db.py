
from sqlalchemy import create_engine
import pyodbc
# Función para obtener la IP activa (asegúrate de definirla correctamente)
from env.libfun.funciones_conexion import conexion_obtener_ip_activa

# Direcciones IP y credenciales (reemplaza con tus valores reales)
direcciones_ip = ["DESKTOP-U2339IU"]
ip_activa = conexion_obtener_ip_activa(direcciones_ip)
direccion_servidor = ip_activa
nombre_usuario = ''
password = ''

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
