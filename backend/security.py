import os
import jwt
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv

load_dotenv()
from pwdlib import PasswordHash
from jwt.exceptions import InvalidTokenError

ALGORITHIM=os.getenv('ALGORITHIM','HS256')
SECRET_KEY=os.getenv('SECRET_KEY')
ACESS_TOKEN_EXPIRE_MINUTES=int(os.getenv('ACESS_TOKEN_EXPIRE_MINUTES',60))

passwordhash=PasswordHash.recommended()

if not SECRET_KEY:
    raise RuntimeError('SECRET_KEY nao achada no .env')


def criar_token_acesso(usuario_id:int)->str:
    expiracao=datetime.now(timezone.utc)+timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)

    dados={
        "sub":str(usuario_id),
        "exp":expiracao
    }


    token=jwt.encode(dados,SECRET_KEY,algorithm=ALGORITHIM)

    return token


def validar_token(token:str)->int | None:
    try:
        dados=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=['HS256']
        )

        usuario_id=dados.get("sub")
        if usuario_id is None:
            return None

        return int(usuario_id)
    except(InvalidTokenError,ValueError,TypeError):
        return None


def gerar_hash(senha:str)->str:
    return passwordhash.hash(senha)


def verificar_senha(senha:str,senha_hash:str)->bool:
   return passwordhash.verify(senha,senha_hash)
