from datetime import datetime
from pydantic import BaseModel,Field
from models.leilao import StatusLeilao
from decimal import Decimal

class LeilaoCriacao(BaseModel):
    titulo:str=Field(...,min_length=3,max_length=200)
    descricao:str=Field(...)
    imagem_url:str | None=None
    item_externo_id:str=Field(...)
    valor_inicial:Decimal=Field(gt=0,max_digits=10,decimal_places=2)
    incremento_minimo:Decimal=Field(gt=0,max_digits=10,decimal_places=2)
    inicio_em:datetime
    fim_em:datetime


class LeilaoResposta(BaseModel):
    id:int
    leiloeiro_id:int
    titulo:str
    descricao:str
    imagem_url:str | None
    item_externo_id:str
    valor_inicial:Decimal
    incremento_minimo:Decimal
    inicio_em:datetime
    fim_em:datetime
    status:StatusLeilao
    model_config = {"from_attributes":True}