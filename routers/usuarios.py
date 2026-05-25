from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_usuario_autenticado, requer_admin
from models.usuario import Usuario
import repositories.usuario_repository as usuario_repo

router = APIRouter(prefix="/usuarios", tags=["Usuários"])


@router.get("/me", summary="Meu perfil")
def meu_perfil(usuario: Usuario = Depends(get_usuario_autenticado)):
    return {
        "id": usuario.id, "nome": usuario.nome, "email": usuario.email,
        "telefone": usuario.telefone, "cnh": usuario.cnh,
        "role": usuario.role, "criado_em": usuario.criado_em,
    }


@router.get("", summary="Listar todos os usuários [Admin]")
def listar_usuarios(db: Session = Depends(get_db), _=Depends(requer_admin)):
    return [
        {"id": u.id, "nome": u.nome, "email": u.email, "telefone": u.telefone,
         "cnh": u.cnh, "role": u.role, "criado_em": u.criado_em}
        for u in usuario_repo.listar_todos(db)
    ]


@router.get("/{usuario_id}", summary="Buscar usuário por ID [Admin]")
def buscar_usuario(usuario_id: str, db: Session = Depends(get_db), _=Depends(requer_admin)):
    usuario = usuario_repo.buscar_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(404, "Usuário não encontrado")
    return {
        "id": usuario.id, "nome": usuario.nome, "email": usuario.email,
        "telefone": usuario.telefone, "cnh": usuario.cnh,
        "role": usuario.role, "criado_em": usuario.criado_em,
    }
