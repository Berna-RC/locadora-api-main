from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from database import get_db
from dependencies import get_usuario_autenticado
from models.usuario import Usuario
from schemas.locacao import LocacaoCriar, DevolucaoInput, StatusLocacaoEnum
import repositories.carro_repository as carro_repo
import repositories.locacao_repository as locacao_repo

router = APIRouter(prefix="/locacoes", tags=["Locações"])


@router.post("", status_code=201, summary="Criar locação")
def criar_locacao(body: LocacaoCriar, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_autenticado)):
    carro = carro_repo.buscar_por_id(db, body.carro_id)
    if not carro:
        raise HTTPException(404, "Carro não encontrado")
    if not carro.disponivel:
        raise HTTPException(400, "Carro indisponível para locação")

    dias = (body.data_devolucao_prevista - body.data_retirada).days
    valor_total = round(dias * carro.diaria, 2)
    carro.disponivel = False
    db.commit()

    locacao = locacao_repo.criar(db, usuario.id, body.carro_id, body.data_retirada,
                                  body.data_devolucao_prevista, valor_total, body.observacoes)
    return {"mensagem": "Locação criada com sucesso", "id": locacao.id, "valor_total": valor_total, "dias": dias}


@router.get("", summary="Minhas locações (ou todas se Admin)")
def listar_locacoes(
    status_filtro: Optional[StatusLocacaoEnum] = None,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_usuario_autenticado),
):
    usuario_id = None if usuario.role == "admin" else usuario.id
    locacoes = locacao_repo.listar(db, usuario_id, status_filtro.value if status_filtro else None)
    return [
        {"id": l.id, "usuario_id": l.usuario_id, "cliente_nome": l.usuario.nome,
         "carro_id": l.carro_id, "marca": l.carro.marca, "modelo": l.carro.modelo, "placa": l.carro.placa,
         "data_retirada": l.data_retirada, "data_devolucao_prevista": l.data_devolucao_prevista,
         "data_devolucao_real": l.data_devolucao_real, "valor_total": l.valor_total,
         "status": l.status, "observacoes": l.observacoes, "criado_em": l.criado_em}
        for l in locacoes
    ]


@router.get("/{locacao_id}", summary="Detalhes de uma locação")
def buscar_locacao(locacao_id: str, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_autenticado)):
    locacao = locacao_repo.buscar_por_id(db, locacao_id)
    if not locacao:
        raise HTTPException(404, "Locação não encontrada")
    if usuario.role != "admin" and locacao.usuario_id != usuario.id:
        raise HTTPException(403, "Acesso negado")
    return {
        "id": locacao.id, "usuario_id": locacao.usuario_id, "cliente_nome": locacao.usuario.nome,
        "carro_id": locacao.carro_id, "marca": locacao.carro.marca, "modelo": locacao.carro.modelo,
        "placa": locacao.carro.placa, "categoria": locacao.carro.categoria,
        "data_retirada": locacao.data_retirada, "data_devolucao_prevista": locacao.data_devolucao_prevista,
        "data_devolucao_real": locacao.data_devolucao_real, "valor_total": locacao.valor_total,
        "status": locacao.status, "observacoes": locacao.observacoes, "criado_em": locacao.criado_em,
    }


@router.patch("/{locacao_id}/devolver", summary="Registrar devolução")
def devolver_carro(locacao_id: str, body: DevolucaoInput, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_autenticado)):
    locacao = locacao_repo.buscar_por_id(db, locacao_id)
    if not locacao:
        raise HTTPException(404, "Locação não encontrada")
    if usuario.role != "admin" and locacao.usuario_id != usuario.id:
        raise HTTPException(403, "Acesso negado")
    if locacao.status != "ativa":
        raise HTTPException(400, f"Locação já está {locacao.status}")

    hoje = date.today()
    atraso = max(0, (hoje - locacao.data_devolucao_prevista).days)
    multa = round(atraso * locacao.carro.diaria * 0.20, 2)
    valor_final = round(locacao.valor_total + multa, 2)
    obs = (f"{body.observacoes or ''} | Atraso: {atraso} dias | Multa: R$ {multa}".strip(" |")
           if atraso > 0 else body.observacoes)

    locacao_repo.devolver(db, locacao, hoje, valor_final, obs, body.km_final)
    return {"mensagem": "Devolução registrada com sucesso", "data_devolucao": hoje.isoformat(),
            "atraso_dias": atraso, "multa": multa, "valor_final": valor_final}


@router.patch("/{locacao_id}/cancelar", summary="Cancelar locação")
def cancelar_locacao(locacao_id: str, db: Session = Depends(get_db), usuario: Usuario = Depends(get_usuario_autenticado)):
    locacao = locacao_repo.buscar_por_id(db, locacao_id)
    if not locacao:
        raise HTTPException(404, "Locação não encontrada")
    if usuario.role != "admin" and locacao.usuario_id != usuario.id:
        raise HTTPException(403, "Acesso negado")
    if locacao.status != "ativa":
        raise HTTPException(400, f"Locação já está {locacao.status}")
    locacao_repo.cancelar(db, locacao)
    return {"mensagem": "Locação cancelada com sucesso"}
