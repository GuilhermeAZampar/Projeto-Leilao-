from datetime import datetime
from sqlalchemy import String,Integer,Numeric,Enum as SQLEnum,DateTime,Text,Numeric,ForeignKey,CheckConstraint,func
from sqlalchemy.orm import Mapped,mapped_column,relationship
from database import Base
from decimal import Decimal

class Lance(Base):
    __tablename__ = 'lance'
    __table_args__ = (
        CheckConstraint("valor>0",name="ck_valor_positivo"),
    )
    leilao:Mapped["Leilao"]=relationship("Leilao",back_populates="lances")
    usuario_licitante:Mapped["Usuario"]=relationship("Usuario",back_populates="lances")
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    leilao_id:Mapped[int]=mapped_column(Integer,ForeignKey('leilao.id'),nullable=False)
    licitante_id:Mapped[int]=mapped_column(Integer,ForeignKey('usuarios.id'),nullable=False)
    valor:Mapped[Decimal]=mapped_column(Numeric(10,2),nullable=False)
    criado_em:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)
