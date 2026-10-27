from datetime import datetime
from sqlalchemy import String,DateTime,Integer,func,Enum as SQLEnum
from sqlalchemy.orm import Mapped , mapped_column,relationship
from enum import Enum

from database import Base


class PapelUsuario(str,Enum):
    LEILOEIRO="leiloeiro"
    LICITANTE="licitante"


class Usuario(Base):
    __tablename__="usuarios"
    carteira:Mapped["Carteira | None"]=relationship("Carteira",back_populates="usuario",uselist=False)
    leiloes:Mapped[list["Leilao"]]=relationship("Leilao",back_populates="leiloeiro")
    lances:Mapped[list["Lance"]]=relationship("Lance",back_populates="usuario_licitante")
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    nome:Mapped[str]=mapped_column(String(100),nullable=False)
    email:Mapped[str]=mapped_column(String(250),unique=True,nullable=False)
    senha_hash:Mapped[str]=mapped_column(String(255),nullable=False)
    papel:Mapped[PapelUsuario]=mapped_column(SQLEnum(PapelUsuario,name='papel_usuario_enum',values_callable=lambda enum:[item.value for item in enum]),nullable=False)
    criado_em:Mapped[datetime]=mapped_column(DateTime(timezone=True),server_default=func.now(),nullable=False)