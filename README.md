# Dashboard de Gestão Imobiliária (Real Estate Control)

Painel administrativo interno para consultores A&M controlarem contratos de aluguel, imóveis e proprietários de forma centralizada.

## Visão Geral

O Dashboard de Gestão Imobiliária oferece:
- **Cards de Métricas**: Receita de aluguéis, taxa de ocupação e inadimplência em tempo real
- **Gráfico de Contratos**: Visualização de novos contratos assinados por mês (últimos 12 meses)
- **Tabela de Imóveis**: Listagem paginada de imóveis cadastrados
- **Cadastro de Imóveis**: Formulário com validação para adicionar novos imóveis ao portfólio

**Arquétipo**: AS1I (Frontend interno CAS - FastAPI + React)  
**Stack**: FastAPI (Python 3.13+), React 19 + TypeScript, Vite, Recharts  
**Persistência**: MVP com dados mockados em memória (sem banco de dados)

## Pré-requisitos

- **Python**: 3.13 ou superior
- **Node.js**: 18 ou superior
- **Bun**: Gerenciador de pacotes JavaScript (recomendado)
- **uv**: Gerenciador de pacotes Python

## Setup Local

### Backend (FastAPI)

```bash
# Criar ambiente virtual e instalar dependências
uv venv
source .venv/bin/activate  # Linux/macOS

uv pip install -e ".[dev]"

# Executar servidor de desenvolvimento
uvicorn src.main:app --reload --port 8000
```

Backend estará disponível em: `http://localhost:8000`  
Documentação Swagger UI: `http://localhost:8000/docs`

### Frontend (React + Vite)

```bash
cd frontend
bun install
bun run dev
```

Frontend estará disponível em: `http://localhost:5173`

## Executar Testes

```bash
source .venv/bin/activate
pytest tests/unit/ --cov=src --cov-report=term-missing --cov-fail-under=80
```

**Cobertura atual**: 93%

## APIs

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/health` | Health check |
| GET | `/api/v1/metrics` | Métricas (receita, ocupação, inadimplência) |
| GET | `/api/v1/contracts/monthly-stats` | Contratos por mês |
| GET | `/api/v1/properties` | Lista imóveis (paginado) |
| POST | `/api/v1/properties` | Cadastra imóvel |

**Documentação completa**: `/docs` (Swagger UI)
