import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from database import Base


class Carro(Base):
    __tablename__ = "carros"

    id         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    marca      = Column(String, nullable=False)
    modelo     = Column(String, nullable=False)
    ano        = Column(Integer, nullable=False)
    placa      = Column(String, unique=True, nullable=False)
    cor        = Column(String, nullable=False)
    categoria  = Column(String, nullable=False)
    diaria     = Column(Float, nullable=False)
    disponivel = Column(Boolean, default=True)
    km_atual   = Column(Integer, default=0)
    descricao  = Column(Text, nullable=True)
    criado_em  = Column(DateTime, default=datetime.utcnow)

    locacoes = relationship("Locacao", back_populates="carro")
