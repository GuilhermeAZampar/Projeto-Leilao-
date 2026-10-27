from decimal import Decimal

from sqlalchemy import select

from database import SessionLocal
from models.lance import Lance
from services.auditoria import verificar_auditoria


with SessionLocal() as db:
    try:
        lance = db.scalar(
            select(Lance).where(Lance.leilao_id == 9).limit(1)
        )

        if lance is None:
            print("Nenhum lance encontrado no leilão 9.")
        else:
            print("Antes da alteração:", verificar_auditoria(db, 9))

            lance.valor += Decimal("1.00")
            db.flush()

            print("Depois da alteração:", verificar_auditoria(db, 9))
    finally:
        db.rollback()
        print("Teste finalizado; alteração desfeita.")