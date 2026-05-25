from sqlalchemy.orm import Session
from models.carro import Carro
from models.locacao import Locacao
from typing import Optional


def listar(db: Session, disponivel: Optional[bool], categoria: Optional[str],
           diaria_max: Optional[float], marca: Optional[str]) -> list[Carro]:
    query = db.query(Carro)
    if disponivel is not None:
        query = query.filter(Carro.disponivel == disponivel)
    if categoria:
        query = query.filter(Carro.categoria == categoria)
    if diaria_max:
        query = query.filter(Carro.diaria <= diaria_max)
    if marca:
        query = query.filter(Carro.marca.ilike(f"%{marca}%"))
    return query.all()


def buscar_por_id(db: Session, carro_id: str) -> Carro | None:
    return db.query(Carro).filter_by(id=carro_id).first()


def buscar_por_placa(db: Session, placa: str) -> Carro | None:
    return db.query(Carro).filter_by(placa=placa).first()


def criar(db: Session, dados: dict) -> Carro:
    carro = Carro(**dados)
    db.add(carro)
    db.commit()
    return carro


def atualizar(db: Session, carro: Carro, campos: dict) -> Carro:
    for campo, valor in campos.items():
        setattr(carro, campo, valor)
    db.commit()
    return carro


def remover(db: Session, carro: Carro) -> None:
    db.delete(carro)
    db.commit()


def tem_locacao_ativa(db: Session, carro_id: str) -> bool:
    return db.query(Locacao).filter_by(carro_id=carro_id, status="ativa").first() is not None
