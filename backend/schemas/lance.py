from pydantic import BaseModel,Field
from datetime import datetime
from decimal import Decimal


class LanceCriacao(BaseModel):
    valor:Decimal=Field(gt=0,max_digits=10,decimal_places=2)



class LanceResposta(BaseModel):
    id:int
    leilao_id:int
    licitante_id:int
    licitante_nome:str | None=None
    valor:Decimal
    criado_em:datetime
    model_config={"from_attributes":True}
