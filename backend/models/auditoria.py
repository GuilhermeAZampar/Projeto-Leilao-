from sqlalchemy import Integer,Text,DateTime,String,ForeignKey,func,Constraint,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column
from datetime import datetime

from database import Base


class Auditoria(Base):
    __tablename__ = 'auditoria'
    __table_args__ = (
        UniqueConstraint('leilao_id', 'sequencia',name='uq_auditoria_leilao_sequencia'),
    )
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    leilao_id:Mapped[int]=mapped_column(Integer,ForeignKey('leilao.id'),index=True)
    sequencia:Mapped[int]=mapped_column(Integer,nullable=False)
    tipo_evento:Mapped[str]=mapped_column(String(50),nullable=False)
    dados_evento:Mapped[str]=mapped_column(Text,nullable=False)
    hash_anterior:Mapped[str]=mapped_column(String(64),nullable=False)
    hash_atual:Mapped[str]=mapped_column(String(64),nullable=False)
    criado_em:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)

