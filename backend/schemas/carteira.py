from decimal import Decimal
from pydantic import BaseModel,Field

class DepositoEntrada(BaseModel):
    valor:Decimal=Field(gt=0,max_digits=10,decimal_places=2)


class CarteiraResposta(BaseModel):
    saldo:Decimal
    saldo_disponivel:Decimal
    saldo_reservado:Decimal