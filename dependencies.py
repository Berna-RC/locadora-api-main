import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from models.usuario import Usuario
import repositories.usuario_repository as usuario_repo

security = HTTPBearer()


def get_usuario_autenticado(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> Usuario:
    token_str = credentials.credentials
    try:
        # Decodifica o JWT — já valida a assinatura e a expiração automaticamente
        payload = usuario_repo.decodificar_token(token_str)
        usuario_id = payload.get("sub")
        if not usuario_id:
            raise HTTPException(status_code=401, detail="Token inválido")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

    usuario = usuario_repo.buscar_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return usuario


def requer_admin(usuario: Usuario = Depends(get_usuario_autenticado)) -> Usuario:
    if usuario.role != "admin":
        raise HTTPException(status_code=403, detail="Acesso restrito a administradores")
    return usuario
