from datetime import datetime, timezone
from sqlalchemy import select,desc
from sqlalchemy.orm import Session

from models.leilao import Leilao,StatusLeilao
from models.lance import Lance
from models.carteira import Carteira
from services.auditoria import registrar_evento

def liquidar_leilao(leilao_id: int,db:Session) :
    leilao=db.scalar(select(Leilao).where(Leilao.id == leilao_id).with_for_update())
    if leilao is None:
        return False

    if leilao.status in (StatusLeilao.ENCERRADO,StatusLeilao.CANCELADO) :
        return False

    agora=datetime.now(timezone.utc)
    if agora <leilao.fim_em:
        return False

    maior_lance=db.scalar(select(Lance).where(Lance.leilao_id == leilao.id).order_by(desc(Lance.valor),desc(Lance.id)).limit(1))

    if maior_lance is None:
        leilao.status = StatusLeilao.ENCERRADO
        dados_evento = {"leilao_id": leilao_id, "status": "encerrado"}
        registrar_evento(db,leilao_id,"LEILAO_ENCERRADO_SEM_LANCES",dados_evento)
        return True

    ids_usuarios=[
        maior_lance.licitante_id,
        leilao.leiloeiro_id
    ]

    carteiras=db.scalars(select(Carteira).where(Carteira.usuario_id.in_(ids_usuarios)).order_by(Carteira.usuario_id).with_for_update()).all()
    carteiras_por_usuario={
        carteira.usuario_id:carteira for carteira in carteiras
    }

    carteira_vencedor=carteiras_por_usuario.get(maior_lance.licitante_id)
    carteira_leiloeiro = carteiras_por_usuario.get(leilao.leiloeiro_id)

    if carteira_vencedor is None or carteira_leiloeiro is None:
        raise ValueError("Erro ao encontrar carteiras")

    if carteira_vencedor.saldo_reservado < maior_lance.valor:
        raise ValueError("Erro o saldo reservado é menor que o lance")

    if carteira_vencedor.saldo < maior_lance.valor:
        raise ValueError("Erro saldo é menor que o lance")

    if maior_lance.licitante_id ==leilao.leiloeiro_id:
        raise ValueError("O Leiloeiro nao pode ser o vencedor")

    carteira_vencedor.saldo -=maior_lance.valor
    carteira_vencedor.saldo_reservado -=maior_lance.valor
    carteira_leiloeiro.saldo += maior_lance.valor


    leilao.status = StatusLeilao.ENCERRADO
    dados_liquidacao={"leilao_id":leilao_id,"vencedor_id":maior_lance.licitante_id,"leiloeiro_id":leilao.leiloeiro_id,"valor":str(maior_lance.valor)}
    registrar_evento(db,leilao_id,"LEILAO_LIQUIDADO",dados_liquidacao)
    return True

def buscar_leiloes_vencido(db:Session):
    agora=datetime.now(timezone.utc)
    leilao=db.scalars(select(Leilao.id).where(Leilao.fim_em <= agora).where(Leilao.status.not_in([StatusLeilao.ENCERRADO,StatusLeilao.CANCELADO])).order_by(Leilao.id)).all()

    return leilao

def processar_leiloes_vencidos(db:Session):
    leiloes=buscar_leiloes_vencido(db)
    db.rollback()
    for leilao_id in leiloes:
        try:
            liquidar_leilao(leilao_id, db)
            db.commit()
        except Exception as erro:
            db.rollback()
            print(f"Erro ao processar leilao {leilao_id} erro: {erro}")


