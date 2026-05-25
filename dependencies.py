from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.usuario import Usuario
import repositories.usuario_repository as usuario_repo

security = HTTPBearer()


def get_usuario_autenticado(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Usuario:
    token_str = credentials.credentials
    token = usuario_repo.buscar_token(db, token_str)
    if not token:
        raise HTTPException(status_code=401, detail="Token inválido")
    if token.expira_em < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expirado")
    usuario = usuario_repo.buscar_por_id(db, token.usuario_id)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return usuario


def requer_admin(usuario: Usuario = Depends(get_usuario_autenticado)) -> Usuario:
    if usuario.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return usuario
