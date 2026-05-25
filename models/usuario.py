import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nome       = Column(String, nullable=False)
    email      = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    telefone   = Column(String, nullable=True)
    cnh        = Column(String, unique=True, nullable=False)
    role       = Column(String, default="cliente")
    criado_em  = Column(DateTime, default=datetime.utcnow)

    tokens   = relationship("Token",   back_populates="usuario", cascade="all, delete-orphan")
    locacoes = relationship("Locacao", back_populates="usuario")
