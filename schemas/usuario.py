from pydantic import BaseModel, Field
from typing import Optional


class UsuarioCriar(BaseModel):
    nome:     str           = Field(..., min_length=3)
    email:    str
    senha:    str           = Field(..., min_length=6)
    telefone: Optional[str] = None
    cnh:      str


class LoginInput(BaseModel):
    email: str
    senha: str
