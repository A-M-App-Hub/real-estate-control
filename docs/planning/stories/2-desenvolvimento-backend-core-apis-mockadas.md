---
source_roadmap: roadmap_equilibrado.md
phase_index: 2
phase_title: "Desenvolvimento do Backend Core com APIs Mockadas"
epic_title: "Dashboard de Gestão Imobiliária (Real Estate Control)"
generated_at: "2026-07-16T14:30:00"
---

# Story: Desenvolvimento do Backend Core com APIs Mockadas

## Context

Implementar backend FastAPI com endpoints REST para métricas, gráfico de contratos, listagem de imóveis e cadastro de imóvel. Dados mockados em memória (sem persistência real). Esta fase entrega o backend funcional que permite o desenvolvimento paralelo do frontend.

**Objetivo**: Criar APIs REST completas com dados mockados, documentação OpenAPI e testes unitários.

**Limites de entrega**: Backend FastAPI funcional com 5 endpoints principais, dados mockados em memória, documentação Swagger UI e testes unitários.

## Tasks

- [ ] Criar estrutura do projeto backend FastAPI
  - [ ] Configurar pyproject.toml com dependências (FastAPI, Uvicorn, Pydantic)
  - [ ] Criar estrutura de pastas (app/, tests/, schemas/, services/)
  - [ ] Configurar ambiente virtual e instalar dependências
- [ ] Implementar endpoint GET /api/metricas
  - [ ] Criar schema Pydantic para resposta (receita, taxa_ocupacao, inadimplencia)
  - [ ] Implementar lógica de mock com dados realistas
  - [ ] Adicionar testes unitários
- [ ] Implementar endpoint GET /api/contratos/novos-por-mes
  - [ ] Criar schema Pydantic para resposta (meses, quantidades)
  - [ ] Implementar lógica de mock com dados dos últimos 12 meses
  - [ ] Adicionar testes unitários
- [ ] Implementar endpoint GET /api/imoveis
  - [ ] Criar schema Pydantic para Imovel (id, proprietario, endereco, tipo, status, valor_aluguel, data_cadastro)
  - [ ] Implementar paginação (query params page e limit)
  - [ ] Implementar ordenação por data de cadastro (mais recentes primeiro)
  - [ ] Adicionar testes unitários
- [ ] Implementar endpoint POST /api/imoveis
  - [ ] Criar schema Pydantic para request body (proprietario, endereco, tipo, status, valor_aluguel)
  - [ ] Implementar validação de campos obrigatórios
  - [ ] Implementar lógica de salvamento em memória (lista Python)
  - [ ] Adicionar testes unitários (sucesso e validação)
- [ ] Implementar endpoint GET /health
  - [ ] Retornar status do backend (status: "ok", timestamp)
  - [ ] Adicionar testes unitários
- [ ] Configurar documentação OpenAPI (Swagger UI)
  - [ ] Validar que Swagger UI está acessível em /docs
  - [ ] Adicionar descrições e exemplos nos endpoints
- [ ] Configurar CORS para permitir acesso do frontend
  - [ ] Adicionar middleware CORS com origens permitidas
- [ ] Executar testes unitários e validar cobertura mínima (80%)

## Acceptance Criteria

- AC-2.1: Endpoint GET /api/metricas retorna receita, taxa de ocupação e inadimplência (dados mockados) — resposta JSON válida com valores realistas
- AC-2.2: Endpoint GET /api/contratos/novos-por-mes retorna dados para gráfico de barras (últimos 12 meses) — resposta JSON com arrays de meses e quantidades
- AC-2.3: Endpoint GET /api/imoveis retorna lista de imóveis com paginação (query params page e limit) — resposta JSON com total, page, limit e array de imóveis
- AC-2.4: Endpoint POST /api/imoveis cadastra novo imóvel (validação de campos obrigatórios) — retorna 201 Created com imóvel criado, valida campos obrigatórios (400 Bad Request se inválido)
- AC-2.5: Endpoint GET /health retorna status do backend — resposta JSON com status "ok" e timestamp
- AC-2.6: Documentação OpenAPI gerada automaticamente (FastAPI Swagger UI) — Swagger UI acessível em /docs com todos os endpoints documentados
- AC-2.7: Testes unitários para endpoints críticos (cobertura mínima: 80%) — pytest executado com sucesso, cobertura >= 80%

## Worktree Config

- **story-slug**: desenvolvimento-backend-core-apis-mockadas
- **branch-name**: story/desenvolvimento-backend-core-apis-mockadas
- **base-branch**: main

## Test Strategy

- **unit-test-runner**: pytest -xvs --tb=long --cov=app --cov-report=term-missing
- **e2e-required**: nao
- **coverage-threshold**: 80
- **test-paths**: tests/

## PR Config

- **draft**: true
- **base**: main
- **labels**: ["story/desenvolvimento-backend-core-apis-mockadas", "backend", "api"]

## Autonomy Blockers

- **Validação de regras de negócio (RN01-RN05)**: Confirmar com PO as fórmulas de cálculo de métricas (receita, taxa de ocupação, inadimplência) antes de implementar os mocks. Se regras não estiverem claras, usar valores realistas e documentar premissas.
- **Definição de contratos de API**: Se o frontend já estiver em desenvolvimento paralelo, validar contratos de API (payloads, status codes) com o desenvolvedor frontend para evitar retrabalho.

## Technical Notes

- **Dependências**: Fase 1 (Infraestrutura) — infraestrutura GCP e repositório devem estar prontos
- **Pontos de integração**: 
  - Frontend React (consumidor das APIs)
  - Swagger UI (documentação interativa)
- **Riscos**: 
  - Dados mockados podem não refletir regras de negócio reais — mitigado por validação com PO
  - Paginação pode ter edge cases (página vazia, limite inválido) — cobrir com testes unitários
- **Referencias**: 
  - PRD: `docs/planning/real-estate-control-prd.md` (seção 8.3 — APIs de Saída)
  - Blueprint: `docs/planning/blueprints/blueprint-AS1I-rendered.md` (stack FastAPI)
  - Regras de negócio: RN01 (Cálculo de Receita), RN02 (Taxa de Ocupação), RN03 (Inadimplência)
- **Stack**: FastAPI (Python 3.13+), Pydantic (validação), Uvicorn (servidor ASGI)
