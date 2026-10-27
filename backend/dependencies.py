from fastapi import Depends,HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials,HTTPBearer
from sqlalchemy.orm import Session
from models.usuario import Usuario
from security import validar_token
from database import get_db


bearer_scheme=HTTPBearer()

def get_usuario(credentials:HTTPAuthorizationCredentials = Depends(bearer_scheme),db:Session=Depends(get_db))->Usuario:
    usuario_id=validar_token(credentials.credentials)
    if usuario_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Token invalido",headers={"WWW-Authenticate":"Bearer"})


    usuario=db.get(Usuario,usuario_id)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Usuario nao encontrado",headers={"WWW-Authenticate":"Bearer"})

    return usuario

