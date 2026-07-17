---
source_roadmap: roadmap_equilibrado.md
phase_index: 4
phase_title: "Integração Frontend-Backend e Testes E2E"
epic_title: "Dashboard de Gestão Imobiliária (Real Estate Control)"
generated_at: "2026-07-16T14:30:00"
---

# Story: Integração Frontend-Backend e Testes E2E

## Context

Conectar frontend ao backend via chamadas HTTP, validar fluxos completos de usuário e implementar testes E2E com Playwright. Esta fase garante que a aplicação funciona de ponta a ponta e atende aos requisitos de performance.

**Objetivo**: Integrar frontend e backend, validar todos os fluxos de usuário end-to-end e garantir qualidade com testes automatizados.

**Limites de entrega**: Aplicação integrada funcionando localmente, testes E2E cobrindo fluxos principais, performance validada.

## Tasks

- [ ] Configurar integração frontend-backend
  - [ ] Configurar variável de ambiente VITE_API_BASE_URL apontando para backend local (http://localhost:8000)
  - [ ] Validar que frontend consome endpoints do backend corretamente
  - [ ] Testar CORS (frontend deve conseguir fazer requests para backend)
- [ ] Validar fluxo de visualização de métricas
  - [ ] Abrir dashboard e verificar que cards de métricas carregam dados do backend
  - [ ] Verificar que skeleton loader aparece durante carregamento
  - [ ] Verificar que estado de erro funciona (simular erro no backend)
- [ ] Validar fluxo de visualização de gráfico de contratos
  - [ ] Verificar que gráfico de barras carrega dados do backend
  - [ ] Verificar que tooltip funciona ao passar o mouse
  - [ ] Verificar que estado de erro funciona (simular erro no backend)
- [ ] Validar fluxo de consulta de tabela de imóveis
  - [ ] Verificar que tabela carrega dados do backend
  - [ ] Verificar que paginação funciona (navegar entre páginas)
  - [ ] Verificar que estado vazio funciona (backend retorna lista vazia)
  - [ ] Verificar que estado de erro funciona (simular erro no backend)
- [ ] Validar fluxo de cadastro de imóvel
  - [ ] Preencher formulário com dados válidos e submeter
  - [ ] Verificar que toast verde "Imóvel cadastrado com sucesso!" aparece
  - [ ] Verificar que formulário é limpo após sucesso
  - [ ] Verificar que tabela de imóveis é atualizada automaticamente
  - [ ] Testar validação de campos obrigatórios (submeter formulário vazio)
  - [ ] Verificar que mensagens de erro aparecem abaixo de cada campo
  - [ ] Testar erro de API (simular erro 500 no backend)
  - [ ] Verificar que toast vermelho "Erro ao cadastrar imóvel." aparece
- [ ] Implementar testes E2E com Playwright
  - [ ] Instalar Playwright (npm install -D @playwright/test)
  - [ ] Configurar playwright.config.ts (baseURL, timeout, browsers)
  - [ ] Criar teste E2E: Visualização de métricas
    - [ ] Abrir dashboard
    - [ ] Verificar que cards de métricas estão visíveis
    - [ ] Verificar que valores são exibidos corretamente
  - [ ] Criar teste E2E: Visualização de gráfico de contratos
    - [ ] Abrir dashboard
    - [ ] Verificar que gráfico de barras está visível
    - [ ] Verificar que tooltip funciona (hover sobre barra)
  - [ ] Criar teste E2E: Consulta de tabela de imóveis
    - [ ] Abrir dashboard
    - [ ] Verificar que tabela está visível
    - [ ] Verificar que paginação funciona (clicar em próxima página)
  - [ ] Criar teste E2E: Cadastro de imóvel (fluxo completo)
    - [ ] Abrir dashboard
    - [ ] Preencher formulário de cadastro
    - [ ] Clicar em "Cadastrar"
    - [ ] Verificar que toast de sucesso aparece
    - [ ] Verificar que novo imóvel aparece na tabela
  - [ ] Criar teste E2E: Validação de formulário
    - [ ] Abrir dashboard
    - [ ] Submeter formulário vazio
    - [ ] Verificar que mensagens de erro aparecem
- [ ] Validar tratamento de erros
  - [ ] Testar timeout de API (simular delay no backend)
  - [ ] Testar erro 4xx (Bad Request, Not Found)
  - [ ] Testar erro 5xx (Internal Server Error)
  - [ ] Verificar que mensagens de erro são amigáveis
- [ ] Validar performance
  - [ ] Medir tempo de carregamento do dashboard (deve ser < 2s)
  - [ ] Medir tempo de cadastro de imóvel (deve ser < 1s)
  - [ ] Usar Chrome DevTools (Network, Performance) para análise
  - [ ] Documentar resultados e otimizar se necessário
- [ ] Executar todos os testes E2E e validar sucesso
  - [ ] npx playwright test
  - [ ] Verificar que todos os testes passam
  - [ ] Gerar relatório de testes (npx playwright show-report)

## Acceptance Criteria

- AC-4.1: Frontend consome endpoints do backend (métricas, gráfico, tabela, cadastro) — todas as chamadas HTTP funcionam, dados são exibidos corretamente
- AC-4.2: Fluxo de visualização de métricas funciona end-to-end — cards de métricas carregam dados do backend, skeleton loader funciona
- AC-4.3: Fluxo de cadastro de imóvel funciona end-to-end (validação + feedback) — formulário valida campos, toast de sucesso/erro aparece, tabela é atualizada
- AC-4.4: Fluxo de consulta de tabela funciona end-to-end (paginação) — tabela carrega dados, paginação funciona
- AC-4.5: Testes E2E implementados com Playwright (cobertura de fluxos principais) — testes E2E criados e passando (visualização de métricas, cadastro de imóvel, consulta de tabela)
- AC-4.6: Tratamento de erros implementado (timeout, erro de API, validação) — mensagens de erro amigáveis, estados de erro funcionam
- AC-4.7: Performance validada (carregamento do dashboard < 2s, cadastro < 1s) — métricas de performance medidas e documentadas, otimizações aplicadas se necessário

## Worktree Config

- **story-slug**: integracao-frontend-backend-testes-e2e
- **branch-name**: story/integracao-frontend-backend-testes-e2e
- **base-branch**: main

## Test Strategy

- **unit-test-runner**: npm test (frontend), pytest -xvs --tb=long (backend)
- **e2e-required**: sim
- **coverage-threshold**: 80
- **test-paths**: tests/e2e/

## PR Config

- **draft**: true
- **base**: main
- **labels**: ["story/integracao-frontend-backend-testes-e2e", "integration", "e2e", "testing"]

## Autonomy Blockers

- **Backend ou frontend incompletos**: Esta fase depende de ambas as fases 2 e 3 estarem completas. Se alguma estiver incompleta, bloquear execução e solicitar conclusão.
- **Problemas de CORS**: Se frontend não conseguir fazer requests para backend, verificar configuração de CORS no backend (middleware FastAPI). Documentar solução se encontrado.
- **Performance abaixo do esperado**: Se carregamento do dashboard > 2s ou cadastro > 1s, investigar causas (network latency, dados mockados grandes, renderização lenta). Documentar otimizações aplicadas.

## Technical Notes

- **Dependências**: Fases 2 e 3 (Backend + Frontend) — ambos devem estar completos e funcionais
- **Pontos de integração**: 
  - Frontend React → Backend FastAPI (HTTP REST)
  - Playwright (testes E2E, browser automation)
  - Chrome DevTools (análise de performance)
- **Riscos**: 
  - CORS pode bloquear requests — configurar middleware no backend
  - Testes E2E podem ser flaky (instáveis) — usar waits adequados (waitForSelector, waitForResponse)
  - Performance pode variar em diferentes ambientes — medir em ambiente local e documentar baseline
- **Referencias**: 
  - PRD: `docs/planning/real-estate-control-prd.md` (seção 3.2 — Fluxos Principais, seção 8.6 — Latência)
  - Playwright Docs: https://playwright.dev/docs/intro
- **Stack**: Playwright (testes E2E), Axios (cliente HTTP), Chrome DevTools (performance)
- **Conflitos potenciais de worktree**: Esta story modifica arquivos de frontend (src/) e backend (app/). Se outras stories estiverem modificando os mesmos arquivos, coordenar para evitar conflitos.
