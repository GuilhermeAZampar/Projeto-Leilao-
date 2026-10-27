from decimal import Decimal

from fastapi import APIRouter,HTTPException,Depends,status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from database import get_db
from models import usuario, carteira
from models.usuario import Usuario,PapelUsuario
from models.carteira import Carteira
from schemas.usuarios import UsuarioCadastro,UsuarioResposta,UsuarioLogin,TokenResposta
from security import criar_token_acesso, gerar_hash, verificar_senha
from dependencies import get_usuario

router=APIRouter(prefix="/auth",tags=["Autenticação"])

@router.post("/cadastro",response_model=UsuarioResposta,status_code=status.HTTP_201_CREATED)
def cadastro_usuario(dados:UsuarioCadastro,db:Session=Depends(get_db)):
    usuario_existe=db.scalar(select(Usuario).where(Usuario.email==str(dados.email)))
    if usuario_existe:
        raise HTTPException(status_code=409,detail="Erro usuario ja cadastrado")

    novo_usuario=Usuario(
        nome=dados.nome,
        email=str(dados.email),
        senha_hash=gerar_hash(dados.senha),
        papel=dados.papel
    )

    try:
        db.add(novo_usuario)
        db.flush()
        carteira=Carteira(
            usuario_id=novo_usuario.id,
            saldo=Decimal("0.00"),
            saldo_reservado=Decimal("0.00")
        )



        db.add(carteira)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409,detail="Email Ja cadastrado")


    db.refresh(novo_usuario)
    return novo_usuario


@router.post("/login",response_model=TokenResposta,status_code=status.HTTP_200_OK)
def login_usuario(dados:UsuarioLogin,db:Session=Depends(get_db)):
    usuario=db.scalar(select(Usuario).where(Usuario.email==str(dados.email)))
    if not usuario or not verificar_senha(dados.senha,usuario.senha_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Email ou senha incorreto",headers={"WWW-Authenticate":"Bearer"})

    token=criar_token_acesso(usuario.id)
    return {"access_token":token,"token_type":"bearer"}


@router.post("/me",response_model=UsuarioResposta,status_code=status.HTTP_200_OK)
def meu_perfil(usuario_atual:Usuario=Depends(get_usuario)):
    return usuario_atual

