from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from database import get_db
from dependencies import requer_admin
import repositories.locacao_repository as locacao_repo

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("", summary="Resumo geral [Admin]")
def dashboard(db: Session = Depends(get_db), _=Depends(requer_admin)):
    return locacao_repo.resumo_dashboard(db, date.today())
