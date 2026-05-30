import hashlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, SessionLocal
from models import Usuario, Carro  # garante que os models são registrados no Base
from routers import auth, usuarios, carros, locacoes, dashboard


# =============================================================================
#  SEED — dados iniciais
# =============================================================================

def seed_dados():
    db = SessionLocal()
    try:
        if not db.query(Usuario).filter_by(email="admin@locadora.com").first():
            admin = Usuario(
                id="admin-0000-0000-0000-000000000000",
                nome="Administrador",
                email="admin@locadora.com",
                senha_hash=hashlib.sha256("admin123".encode()).hexdigest(),
                cnh="ADMIN-0000",
                role="admin",
            )
            db.add(admin)

        if db.query(Carro).count() == 0:
            db.add_all([
                Carro(marca="Toyota",     modelo="Corolla", ano=2023, placa="ABC-1234", cor="Branco", categoria="sedan",  diaria=180.0),
                Carro(marca="Volkswagen", modelo="Gol",     ano=2022, placa="DEF-5678", cor="Prata",  categoria="hatch",  diaria=110.0),
                Carro(marca="Chevrolet",  modelo="S10",     ano=2023, placa="GHI-9012", cor="Preto",  categoria="pickup", diaria=250.0),
                Carro(marca="Jeep",       modelo="Compass", ano=2024, placa="JKL-3456", cor="Cinza",  categoria="suv",    diaria=300.0),
                Carro(marca="Honda",      modelo="Civic",   ano=2023, placa="MNO-7890", cor="Azul",   categoria="sedan",  diaria=200.0),
            ])
        db.commit()
    finally:
        db.close()


# =============================================================================
#  CRIAÇÃO DO APP
# =============================================================================

Base.metadata.create_all(bind=engine)
seed_dados()

app = FastAPI(
    title="🚗 Locadora de Carros",
    description="API completa para gerenciamento de locadora de carros",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
#  REGISTRO DAS ROTAS
# =============================================================================

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(carros.router)
app.include_router(locacoes.router)
app.include_router(dashboard.router)


# =============================================================================
#  ENTRYPOINT
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
