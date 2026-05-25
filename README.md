# 🚗 Locadora de Carros — API

API RESTful completa para gerenciamento de locadora de carros, desenvolvida com **Python + FastAPI + SQLite**.

---

## ✅ Funcionalidades

- Autenticação com token Bearer (login/logout/registro)
- CRUD completo de carros (com filtros por categoria, disponibilidade, diária, marca)
- Gestão de locações (criar, devolver, cancelar)
- Cálculo automático de valor total e multa por atraso
- Perfis: **cliente** e **admin**
- Dashboard com resumo financeiro e frota
- Banco SQLite (sem configuração externa necessária)

---

## 🚀 Como rodar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Iniciar servidor
python main.py
# ou
uvicorn main:app --reload
```

Acesse a documentação interativa em:
- Swagger UI: http://localhost:8000/docs
- ReDoc:       http://localhost:8000/redoc

---

## 🔑 Credenciais padrão (Admin)

| Campo | Valor |
|-------|-------|
| Email | admin@locadora.com |
| Senha | admin123 |

---

## 📋 Endpoints

### Auth
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | /auth/registrar | Registrar novo cliente |
| POST | /auth/login | Login (retorna token) |
| POST | /auth/logout | Invalidar token |

### Usuários
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /usuarios/me | Meu perfil |
| GET | /usuarios | Listar todos [Admin] |
| GET | /usuarios/{id} | Buscar por ID [Admin] |

### Carros
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /carros | Listar com filtros |
| GET | /carros/{id} | Detalhes do carro |
| POST | /carros | Cadastrar [Admin] |
| PATCH | /carros/{id} | Atualizar [Admin] |
| DELETE | /carros/{id} | Remover [Admin] |

### Locações
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | /locacoes | Criar locação |
| GET | /locacoes | Listar locações |
| GET | /locacoes/{id} | Detalhes |
| PATCH | /locacoes/{id}/devolver | Registrar devolução |
| PATCH | /locacoes/{id}/cancelar | Cancelar |

### Dashboard
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /dashboard | Resumo geral [Admin] |

---

## 📦 Categorias de carros
`hatch` | `sedan` | `suv` | `pickup` | `esportivo` | `minivan`

## 📄 Regras de negócio
- Carro indisponível não pode ser locado
- Carro com locação ativa não pode ser removido
- Multa de atraso: **20% da diária por dia de atraso**
- Token expira em **8 horas**
- Cliente só vê/gerencia suas próprias locações

---

## 🗂 Estrutura
```
locadora_api/
├── main.py           # Toda a aplicação
├── requirements.txt  # Dependências
├── README.md         # Esta documentação
└── locadora.db       # Banco de dados (gerado automaticamente)
```
