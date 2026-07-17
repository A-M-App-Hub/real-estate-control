# real estate control

Dashboard de Gestão Imobiliária: painel administrativo para controle de contratos de aluguel, imóveis e proprietários. Inclui cards com métricas (receita, ocupação, inadimplência), gráfico de novos co

## Setup

```bash
uv sync
uv run uvicorn src.main:app --reload
uv run pytest --cov=src
```

## Estrutura

```
src/             # Código da aplicação (FastAPI)
tests/           # Testes (pytest)
docs/            # Documentação e artefatos de planejamento
docs/planning/   # Stories, blueprints, roadmaps, ADR
skills/          # project-pipeline skill (gerada por pipeline-forge)
iac_scripts/     # Scripts de infraestrutura (preenchidos por project-pipeline)
.github/         # CI/CD workflows
```

## Deploy

- Push em `story/**` ou `feat/**` → CI (lint + testes)
- PR para `main` → CI + deploy automático em QA (após project-pipeline ativar CD)
- Release publicada → deploy em prod via `skills/project-pipeline/SKILL.md`
