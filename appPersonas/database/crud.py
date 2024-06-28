from sqlalchemy.orm import Session
from . import models, database_models as dm # Importa tus modelos y esquemas

# Funciones CRUD para usuarios
def get_usuario_by_email(db: Session, email: str):
    
    return db.query(models.PR_Usuario).filter(models.PR_Usuario.PR_Usu_ch_email == email).first()