import hashlib
import secrets
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.usuario import Usuario
from models.token import Token


def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


def buscar_por_email(db: Session, email: str) -> Usuario | None:
    return db.query(Usuario).filter_by(email=email).first()


def buscar_por_id(db: Session, usuario_id: str) -> Usuario | None:
    return db.query(Usuario).filter_by(id=usuario_id).first()


def email_ou_cnh_existe(db: Session, email: str, cnh: str) -> bool:
    return db.query(Usuario).filter(
        (Usuario.email == email) | (Usuario.cnh == cnh)
    ).first() is not None


def criar_usuario(db: Session, nome: str, email: str, senha: str, telefone: str | None, cnh: str) -> Usuario:
    usuario = Usuario(
        nome=nome,
        email=email,
        senha_hash=hash_senha(senha),
        telefone=telefone,
        cnh=cnh,
    )
    db.add(usuario)
    db.commit()
    return usuario


def autenticar(db: Session, email: str, senha: str) -> Usuario | None:
    return db.query(Usuario).filter_by(
        email=email,
        senha_hash=hash_senha(senha)
    ).first()


def listar_todos(db: Session) -> list[Usuario]:
    return db.query(Usuario).all()


def criar_token(db: Session, usuario_id: str) -> str:
    token = Token(
        token=secrets.token_hex(32),
        usuario_id=usuario_id,
        expira_em=datetime.utcnow() + timedelta(hours=8),
    )
    db.add(token)
    db.commit()
    return token.token


def buscar_token(db: Session, token_str: str) -> Token | None:
    return db.query(Token).filter_by(token=token_str).first()


def deletar_token(db: Session, token_str: str) -> None:
    token = db.query(Token).filter_by(token=token_str).first()
    if token:
        db.delete(token)
        db.commit()
