import hashlib
import json

from sqlalchemy import select
from sqlalchemy.orm import Session
from models.auditoria import Auditoria
from models.leilao import Leilao
from models.lance import Lance
from decimal import Decimal

HASH_INICIAL="0"*64

def calcular_hash(leilao_id:int,sequencia:int,hash_anterior:str,tipo_evento:str,dados_evento:str)->str:
    conteudo={
        "leilao_id": leilao_id,
        "sequencia": sequencia,
        "hash_anterior": hash_anterior,
        "tipo_evento": tipo_evento,
        "dados_evento": dados_evento

    }

    mensagens=json.dumps(conteudo,sort_keys=True,separators=(',',':'),ensure_ascii=False)
    return hashlib.sha256(mensagens.encode("UTF-8")).hexdigest()

def registrar_evento(db:Session,leilao_id:int,tipo_evento:str,dados:dict)->Auditoria:
    leilao=db.scalar((select(Leilao).where(Leilao.id == leilao_id).with_for_update()))
    if leilao is None:
        raise ValueError("Erro o leilao nao existe")

    ultimo_evento=db.scalar(select(Auditoria).where(Auditoria.leilao_id == leilao_id).order_by(Auditoria.sequencia.desc()).limit(1))
    if ultimo_evento is not None:
        sequencia=ultimo_evento.sequencia + 1
    else:
        sequencia=1

    if ultimo_evento is not None:
        hash_anterior=ultimo_evento.hash_atual
    else:
        hash_anterior=HASH_INICIAL

    dados_evento=json.dumps(dados,sort_keys=True,separators=(',',':'),ensure_ascii=False)
    hash_atual=calcular_hash(leilao_id,sequencia,hash_anterior,tipo_evento, dados_evento)
    evento=Auditoria(
        leilao_id=leilao_id,
        sequencia=sequencia,
        hash_anterior=hash_anterior,
        tipo_evento=tipo_evento,
        dados_evento=dados_evento,
        hash_atual=hash_atual
    )
    db.add(evento)
    db.flush()
    return evento


def verificar_auditoria(db:Session,leilao_id:int)->dict:
    eventos=db.scalars(select(Auditoria).where(Auditoria.leilao_id==leilao_id).order_by(Auditoria.sequencia.asc())).all()
    hash_anterior=HASH_INICIAL
    for numero,e in enumerate(eventos,start=1):
        if e.sequencia != numero:
            return{"valido":False,"erro":f"Sequncia invalida no {e.id}"}

        if e.hash_anterior != hash_anterior:
            return {"valido":False,"erro":f"Erro o hash esta errado {e.id}"}

        hash_esperado=calcular_hash(
            e.leilao_id,
            e.sequencia,
            e.hash_anterior,
            e.tipo_evento,
            e.dados_evento

        )
        if hash_esperado != e.hash_atual:
            return{"valido":False,"erro":f"Erro o hash esta errado {e.id}"}

        hash_anterior=e.hash_atual
    lances = db.scalars(select(Lance).where(Lance.leilao_id == leilao_id)).all()
    eventos_lance=[json.loads(evento.dados_evento)for evento in eventos if evento.tipo_evento =="LANCE_REGISTRADO"]
    eventos_por_id = {
        evento["lance_id"]: evento
        for evento in eventos_lance
    }

    if len(eventos_lance) != len(lances) or len(eventos_por_id) != len(eventos_lance):
        return {"valido": False, "erro": "Quantidade de lances e eventos não corresponde"}

    for lance in lances:
        evento = eventos_por_id.get(lance.id)

        if evento is None:
            return {"valido": False, "erro": f"Lance {lance.id} sem evento de auditoria"}

        if (evento["licitante_id"] != lance.licitante_id or Decimal(evento["valor"]) != lance.valor ):
            return {"valido": False, "erro": f"Dados do lance {lance.id} foram alterados"}
    return {"valido":True,"total_eventos":len(eventos),"hash_final":hash_anterior}


