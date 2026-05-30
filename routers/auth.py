from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from schemas.usuario import UsuarioCriar, LoginInput
import repositories.usuario_repository as usuario_repo

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()


@router.post("/registrar", status_code=201, summary="Registrar novo cliente")
def registrar(body: UsuarioCriar, db: Session = Depends(get_db)):
    if usuario_repo.email_ou_cnh_existe(db, body.email, body.cnh):
        raise HTTPException(400, "E-mail ou CNH já cadastrado")
    usuario = usuario_repo.criar_usuario(db, body.nome, body.email, body.senha, body.telefone, body.cnh)
    return {"mensagem": "Usuário criado com sucesso", "id": usuario.id}


@router.post("/login", summary="Login e obtenção de token JWT")
def login(body: LoginInput, db: Session = Depends(get_db)):
    usuario = usuario_repo.autenticar(db, body.email, body.senha)
    if not usuario:
        raise HTTPException(401, "Credenciais inválidas")
    token = usuario_repo.criar_token(usuario.id, usuario.role)
    return {
        "access_token": token,
        "token_type": "bearer",
        "usuario": {"id": usuario.id, "nome": usuario.nome, "email": usuario.email, "role": usuario.role},
    }


@router.post("/logout", summary="Logout (orientação ao cliente)")
def logout():
    # Com JWT o logout é feito no lado do cliente descartando o token
    return {"mensagem": "Logout realizado. Descarte o token no cliente."}
