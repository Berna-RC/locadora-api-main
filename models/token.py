from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Token(Base):
    __tablename__ = "tokens"

    token      = Column(String, primary_key=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"), nullable=False)
    expira_em  = Column(DateTime, nullable=False)

    usuario = relationship("Usuario", back_populates="tokens")
