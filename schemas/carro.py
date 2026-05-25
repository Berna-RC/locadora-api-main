from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class CategoriaEnum(str, Enum):
    hatch     = "hatch"
    sedan     = "sedan"
    suv       = "suv"
    pickup    = "pickup"
    esportivo = "esportivo"
    minivan   = "minivan"


class CarroCriar(BaseModel):
    marca:     str
    modelo:    str
    ano:       int           = Field(..., ge=1990, le=2030)
    placa:     str
    cor:       str
    categoria: CategoriaEnum
    diaria:    float         = Field(..., gt=0)
    km_atual:  int           = Field(0, ge=0)
    descricao: Optional[str] = None


class CarroAtualizar(BaseModel):
    marca:      Optional[str]           = None
    modelo:     Optional[str]           = None
    ano:        Optional[int]           = Field(None, ge=1990, le=2030)
    cor:        Optional[str]           = None
    categoria:  Optional[CategoriaEnum] = None
    diaria:     Optional[float]         = Field(None, gt=0)
    km_atual:   Optional[int]           = Field(None, ge=0)
    descricao:  Optional[str]           = None
    disponivel: Optional[bool]          = None