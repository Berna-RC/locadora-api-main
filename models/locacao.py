import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Date, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Locacao(Base):
    __tablename__ = "locacoes"

    id                      = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id              = Column(String, ForeignKey("usuarios.id"), nullable=False)
    carro_id                = Column(String, ForeignKey("carros.id"), nullable=False)
    data_retirada           = Column(Date, nullable=False)
    data_devolucao_prevista = Column(Date, nullable=False)
    data_devolucao_real     = Column(Date, nullable=True)
    valor_total             = Column(Float, nullable=True)
    status                  = Column(String, default="ativa")
    observacoes             = Column(Text, nullable=True)
    criado_em               = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="locacoes")
    carro   = relationship("Carro",   back_populates="locacoes")
