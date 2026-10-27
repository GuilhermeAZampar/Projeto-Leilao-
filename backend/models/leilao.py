from datetime import datetime
from sqlalchemy import String,Integer,ForeignKey,Enum as SQLEnum,Numeric,Text,DateTime,CheckConstraint
from sqlalchemy.orm import Mapped,mapped_column,relationship
from database import Base
from decimal import Decimal
from enum import Enum

class StatusLeilao(str,Enum):
    AGENDADO="agendado"
    ATIVO="ativo"
    ENCERRADO="encerrado"
    CANCELADO="cancelado"



class Leilao(Base):
    __tablename__="leilao"
    __table_args__ = (
        CheckConstraint("valor_inicial > 0",name="ck_valor_inicial_positivo"),
        CheckConstraint("incremento_minimo > 0",name="ck_incremento_minimo_positivo"),
        CheckConstraint("fim_em > inicio_em",name="ck_periodo_positivo"),
    )
    leiloeiro:Mapped["Usuario"]=relationship("Usuario",back_populates="leiloes")
    lances:Mapped[list["Lance"]]=relationship("Lance",back_populates="leilao")
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    leiloeiro_id:Mapped[int]=mapped_column(Integer,ForeignKey("usuarios.id"),nullable=False)
    titulo:Mapped[str]=mapped_column(String(200),nullable=False)
    descricao:Mapped[str]=mapped_column(Text,nullable=False)
    imagem_url:Mapped[str | None]=mapped_column(Text,nullable=True)
    item_externo_id:Mapped[str]=mapped_column(String(100),nullable=False)
    valor_inicial:Mapped[Decimal]=mapped_column(Numeric(10,2),nullable=False )
    incremento_minimo:Mapped[Decimal]=mapped_column(Numeric(10,2),nullable=False)
    inicio_em:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False)
    fim_em:Mapped[datetime]=mapped_column(DateTime(timezone=True),nullable=False)
    status:Mapped[StatusLeilao]=mapped_column(SQLEnum(StatusLeilao,name='status_leilao',values_callable=lambda enum:[item.value for item in enum] ),default=StatusLeilao.AGENDADO,nullable=False)

