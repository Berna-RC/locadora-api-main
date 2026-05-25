from sqlalchemy.orm import Session
from sqlalchemy import func
from models.locacao import Locacao
from models.carro import Carro
from models.usuario import Usuario
from datetime import date
from typing import Optional


def criar(db: Session, usuario_id: str, carro_id: str, data_retirada: date,
          data_devolucao_prevista: date, valor_total: float, observacoes: Optional[str]) -> Locacao:
    locacao = Locacao(
        usuario_id=usuario_id,
        carro_id=carro_id,
        data_retirada=data_retirada,
        data_devolucao_prevista=data_devolucao_prevista,
        valor_total=valor_total,
        observacoes=observacoes,
    )
    db.add(locacao)
    db.commit()
    return locacao


def buscar_por_id(db: Session, locacao_id: str) -> Locacao | None:
    return db.query(Locacao).filter_by(id=locacao_id).first()


def listar(db: Session, usuario_id: Optional[str], status: Optional[str]) -> list[Locacao]:
    query = db.query(Locacao)
    if usuario_id:
        query = query.filter(Locacao.usuario_id == usuario_id)
    if status:
        query = query.filter(Locacao.status == status)
    return query.all()


def devolver(db: Session, locacao: Locacao, data_real: date, valor_final: float,
             observacoes: Optional[str], km_final: Optional[int]) -> Locacao:
    locacao.status = "concluida"
    locacao.data_devolucao_real = data_real
    locacao.valor_total = valor_final
    locacao.observacoes = observacoes
    locacao.carro.disponivel = True
    if km_final:
        locacao.carro.km_atual = km_final
    db.commit()
    return locacao


def cancelar(db: Session, locacao: Locacao) -> Locacao:
    locacao.status = "cancelada"
    locacao.carro.disponivel = True
    db.commit()
    return locacao


def resumo_dashboard(db: Session, hoje: date) -> dict:
    total_carros    = db.query(func.count(Carro.id)).scalar()
    disponiveis     = db.query(func.count(Carro.id)).filter(Carro.disponivel == True).scalar()
    locados         = db.query(func.count(Carro.id)).filter(Carro.disponivel == False).scalar()
    total_clientes  = db.query(func.count(Usuario.id)).filter(Usuario.role == "cliente").scalar()
    locacoes_ativas = db.query(func.count(Locacao.id)).filter(Locacao.status == "ativa").scalar()

    receita_mes = db.query(func.coalesce(func.sum(Locacao.valor_total), 0)).filter(
        Locacao.status == "concluida",
        func.strftime("%Y-%m", Locacao.data_devolucao_real) == hoje.strftime("%Y-%m"),
    ).scalar()

    receita_total = db.query(func.coalesce(func.sum(Locacao.valor_total), 0)).filter(
        Locacao.status == "concluida"
    ).scalar()

    return {
        "carros": {"total": total_carros, "disponiveis": disponiveis, "locados": locados},
        "clientes": total_clientes,
        "locacoes_ativas": locacoes_ativas,
        "financeiro": {
            "receita_mes_atual": round(receita_mes, 2),
            "receita_total": round(receita_total, 2),
        },
    }
