import hashlib
import jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.usuario import Usuario

# Chave secreta para assinar o JWT — em produção usaria uma variável de ambiente
SECRET_KEY = "locadora-secret-key-2026"
ALGORITHM = "HS256"
EXPIRACAO_HORAS = 8


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


def criar_token(usuario_id: str, role: str) -> str:
    """Gera um JWT com o id e role do usuário, expira em 8 horas."""
    payload = {
        "sub": usuario_id,        # subject — id do usuário
        "role": role,             # perfil do usuário
        "exp": datetime.utcnow() + timedelta(hours=EXPIRACAO_HORAS),  # expiração
        "iat": datetime.utcnow(), # issued at — quando foi gerado
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decodificar_token(token_str: str) -> dict:
    """Decodifica e valida o JWT. Lança exceção se inválido ou expirado."""
    return jwt.decode(token_str, SECRET_KEY, algorithms=[ALGORITHM])
