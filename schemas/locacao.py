from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
from enum import Enum


class StatusLocacaoEnum(str, Enum):
    ativa     = "ativa"
    concluida = "concluida"
    cancelada = "cancelada"


class LocacaoCriar(BaseModel):
    carro_id:                str
    data_retirada:           date
    data_devolucao_prevista: date
    observacoes:             Optional[str] = None

    @field_validator("data_devolucao_prevista")
    @classmethod
    def devolucao_depois_retirada(cls, v, info):
        if "data_retirada" in info.data and v <= info.data["data_retirada"]:
            raise ValueError("data_devolucao_prevista deve ser após data_retirada")
        return v


class DevolucaoInput(BaseModel):
    km_final:    Optional[int] = Field(None, ge=0)
    observacoes: Optional[str] = None