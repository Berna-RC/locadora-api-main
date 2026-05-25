from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from dependencies import get_usuario_autenticado, requer_admin
from schemas.carro import CarroCriar, CarroAtualizar, CategoriaEnum
import repositories.carro_repository as carro_repo

router = APIRouter(prefix="/carros", tags=["Carros"])


@router.get("", summary="Listar carros (com filtros)")
def listar_carros(
    disponivel: Optional[bool]          = None,
    categoria:  Optional[CategoriaEnum] = None,
    diaria_max: Optional[float]         = None,
    marca:      Optional[str]           = None,
    db: Session = Depends(get_db),
    _=Depends(get_usuario_autenticado),
):
    carros = carro_repo.listar(db, disponivel, categoria.value if categoria else None, diaria_max, marca)
    return [
        {"id": c.id, "marca": c.marca, "modelo": c.modelo, "ano": c.ano,
         "placa": c.placa, "cor": c.cor, "categoria": c.categoria,
         "diaria": c.diaria, "disponivel": c.disponivel,
         "km_atual": c.km_atual, "descricao": c.descricao, "criado_em": c.criado_em}
        for c in carros
    ]


@router.get("/{carro_id}", summary="Detalhes de um carro")
def buscar_carro(carro_id: str, db: Session = Depends(get_db), _=Depends(get_usuario_autenticado)):
    carro = carro_repo.buscar_por_id(db, carro_id)
    if not carro:
        raise HTTPException(404, "Carro não encontrado")
    return {
        "id": carro.id, "marca": carro.marca, "modelo": carro.modelo, "ano": carro.ano,
        "placa": carro.placa, "cor": carro.cor, "categoria": carro.categoria,
        "diaria": carro.diaria, "disponivel": carro.disponivel,
        "km_atual": carro.km_atual, "descricao": carro.descricao, "criado_em": carro.criado_em,
    }


@router.post("", status_code=201, summary="Cadastrar novo carro [Admin]")
def cadastrar_carro(body: CarroCriar, db: Session = Depends(get_db), _=Depends(requer_admin)):
    if carro_repo.buscar_por_placa(db, body.placa):
        raise HTTPException(400, "Placa já cadastrada")
    carro = carro_repo.criar(db, {
        "marca": body.marca, "modelo": body.modelo, "ano": body.ano,
        "placa": body.placa, "cor": body.cor, "categoria": body.categoria.value,
        "diaria": body.diaria, "km_atual": body.km_atual, "descricao": body.descricao,
    })
    return {"mensagem": "Carro cadastrado com sucesso", "id": carro.id}


@router.patch("/{carro_id}", summary="Atualizar carro [Admin]")
def atualizar_carro(carro_id: str, body: CarroAtualizar, db: Session = Depends(get_db), _=Depends(requer_admin)):
    carro = carro_repo.buscar_por_id(db, carro_id)
    if not carro:
        raise HTTPException(404, "Carro não encontrado")
    campos = {k: (v.value if k == "categoria" and hasattr(v, "value") else v)
              for k, v in body.model_dump().items() if v is not None}
    if not campos:
        raise HTTPException(400, "Nenhum campo para atualizar")
    carro_repo.atualizar(db, carro, campos)
    return {"mensagem": "Carro atualizado com sucesso"}


@router.delete("/{carro_id}", summary="Remover carro [Admin]")
def remover_carro(carro_id: str, db: Session = Depends(get_db), _=Depends(requer_admin)):
    carro = carro_repo.buscar_por_id(db, carro_id)
    if not carro:
        raise HTTPException(404, "Carro não encontrado")
    if carro_repo.tem_locacao_ativa(db, carro_id):
        raise HTTPException(400, "Não é possível remover um carro com locação ativa")
    carro_repo.remover(db, carro)
    return {"mensagem": "Carro removido com sucesso"}
