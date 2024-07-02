from jose import JWTError, jwt
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session, sessionmaker
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional, List

from appPersonas.database.database_models import PR_Usuario_base
from appPersonas.config.db import engines

logins = APIRouter()

# Configuración de la base de datos
SessionLocal_user = sessionmaker(autocommit=False, autoflush=False, bind=engines['usuario'])

def get_db_user():
    db = SessionLocal_user()
    try:
        yield db
    finally:
        db.close()

# Configuración JWT
SECRET_KEY = "123456"  # ¡Cambia esto por una clave secreta fuerte!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Modelos Pydantic
class Token(BaseModel):
    access_token: str
    token_type: str
    mensaje: str

class TokenData(BaseModel):
    username: str
    roles: List[str] = []

class User(BaseModel):
    username: str
    roles: List[str] = []

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# Funciones de utilidad
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(request: Request, db: Session = Depends(get_db_user)) -> User:
    token = request.cookies.get("session_token")
    if not token:
        raise credentials_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        roles: List[str] = payload.get("roles", [])
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, roles=roles)
    except JWTError:
        raise credentials_exception

    user = db.query(PR_Usuario_base).filter(PR_Usuario_base.PR_Usu_ch_nomb == token_data.username).first()
    if user is None:
        raise credentials_exception

    return User(username=user.PR_Usu_ch_nomb, roles=roles)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

# Rutas de login y autorización
@logins.post("/login", response_model=Token)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_user)):
    user = db.query(PR_Usuario_base).filter(PR_Usuario_base.PR_Usu_ch_nomb == form_data.username).first()
    if not user or not verify_password(form_data.password, user.PR_Usu_ch_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    roles = ["user"]  # Aquí puedes obtener roles del usuario desde la base de datos
    access_token = create_access_token(
        data={"sub": user.PR_Usu_ch_nomb, "roles": roles}
    )

    response.set_cookie(
        key="session_token",
        value=access_token,
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="lax",
    )

    return Token(access_token=access_token, token_type="bearer", mensaje="Login exitoso")

@logins.get("/protected-route", dependencies=[Depends(get_current_user)])
async def protected_route():
    return {"message": "You have access to this route"}

@logins.post("/logout")
def logout(response: Response):
    response.delete_cookie("session_token")
    return {"mensaje": "Logout exitoso"}