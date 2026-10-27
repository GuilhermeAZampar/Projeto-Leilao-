from fastapi import Depends,HTTPException,APIRouter,status
from sqlalchemy.exc import DataError,IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy import select
from database import get_db
from dependencies import get_usuario
from models.usuario import Usuario,PapelUsuario
from models.carteira import Carteira
from schemas.carteira import CarteiraResposta,DepositoEntrada
from schemas.usuarios import UsuarioCadastro
from decimal import Decimal

router = APIRouter(prefix="/carteira",tags=["Carteira"])


@router.get("/",response_model=CarteiraResposta)
def consulta_carteira(usuario_atual:Usuario = Depends(get_usuario),db:Session = Depends(get_db)):

    carteira=db.scalar(select(Carteira).where(Carteira.usuario_id == usuario_atual.id))

    if carteira is None:
        raise HTTPException(status_code=404,detail="Carteira não encontrada")

    return CarteiraResposta(
        saldo=carteira.saldo,
        saldo_reservado=carteira.saldo_reservado,
        saldo_disponivel=carteira.saldo - carteira.saldo_reservado
    )

@router.post("/depositar",response_model=CarteiraResposta)
def depositar(dados:DepositoEntrada,usuario_atual:Usuario=Depends(get_usuario),db:Session = Depends(get_db)):
    if usuario_atual.papel != PapelUsuario.LICITANTE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Erro o usaurio precisa ser licitante")

    try:
        carteira=db.scalar(select(Carteira).where(Carteira.usuario_id == usuario_atual.id).with_for_update())
        if carteira is None:
            raise HTTPException(status_code=404,detail="Carteira não encontrada")

        novo_saldo=carteira.saldo + dados.valor
        if novo_saldo > Decimal("99999999.99"):
            raise HTTPException(status_code=400,detail="Erro o valor passa do limite permitido na carteira")

        carteira.saldo = novo_saldo
        db.commit()
        db.refresh(carteira)
    except(IntegrityError,DataError):
        db.rollback()
        raise HTTPException(status_code=400,detail="Não foi possivel realizr o deposito  ")
    except Exception:
        db.rollback()
        raise

    return CarteiraResposta(
        saldo=carteira.saldo,
        saldo_reservado=carteira.saldo_reservado,
        saldo_disponivel=carteira.saldo - carteira.saldo_reservado
    )
