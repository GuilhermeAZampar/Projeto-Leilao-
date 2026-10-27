from decimal import Decimal
from sqlalchemy import Integer,Numeric,ForeignKey,CheckConstraint
from sqlalchemy.orm import Mapped,mapped_column,relationship


from database import Base




class Carteira(Base):
    __tablename__ = "carteiras"
    __table_args__ = (
        CheckConstraint("saldo >=0", name="ck_saldo_positivo"),
        CheckConstraint("saldo_reservado>=0 AND saldo_reservado <=saldo",name="ck_saldo_negativo"),
    )
    usuario:Mapped["Usuario"]=relationship("Usuario",back_populates="carteira")
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    usuario_id:Mapped[int]=mapped_column(ForeignKey("usuarios.id"),unique=True,nullable=False)
    saldo:Mapped[Decimal]=mapped_column(Numeric(10,2),nullable=False,default=Decimal("0.00"))
    saldo_reservado:Mapped[Decimal]=mapped_column(Numeric(10,2),nullable=False,default=Decimal("0.00"))
