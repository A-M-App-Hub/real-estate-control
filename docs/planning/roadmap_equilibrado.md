# Solution Roadmap — Dashboard de Gestão Imobiliária (Real Estate Control)

## 1. Context

### 1.1 Document objective

Este roadmap descreve a sequência completa de desenvolvimento da solução **Dashboard de Gestão Imobiliária**, incluindo:

* Sequenciamento de desenvolvimento por fases
* Estrutura de backlog hierárquico (Épico → Fase)
* Dependências entre fases
* Critérios de prontidão e aceite por fase
* Governança de execução

### 1.2 References

* **Blueprint**: `docs/planning/blueprints/blueprint-AS1I-rendered.md`
* **PRD**: `docs/planning/real-estate-control-prd.md`
* **Solution Brief**: `docs/planning/solution-brief.yaml`
* **Arquétipo**: AS1I (Front interno CAS, sem persistência)
* **Topologia**: FastAPI_Mixed + INTERNAL_CAS
* **Stack**: React + TypeScript + Vite (frontend) | FastAPI (backend)

### 1.3 Roadmap scope

* **Horizonte de planejamento**: MVP completo (4 semanas)
* **Releases incluídas**: MVP v1.0 (ambiente dev → qa → prod)
* **Ambientes**: dev (d), qa (q), prod (p)
* **Restrições e premissas**:
  - Dados mockados em memória (sem persistência real)
  - Autenticação via CAS (hub A-M-App-Hub)
  - Usuários internos A&M (10-20 consultores)
  - Desktop-first, funcional em tablets

---

## 2. Roadmap strategy

### 2.1 Planning approach

* **Entrega incremental**: Fases de desenvolvimento que entregam valor progressivo
* **Sequenciamento orientado a valor**: Infraestrutura base → Backend → Frontend → Integração
* **Planejamento consciente de dependências**: Fases bloqueadoras executadas primeiro
* **Execução consciente de risco**: Validações técnicas antecipadas (spike de autenticação CAS)

### 2.2 Sequencing principles

* **Fundação primeiro**: Infraestrutura e configuração de ambiente antes de features
* **Desbloquear caminho crítico cedo**: Backend mockado antes de frontend para permitir desenvolvimento paralelo
* **Habilitar validação antecipada**: Spike de autenticação CAS na Fase 1 para validar integração
* **Maximizar paralelização quando viável**: Frontend e backend podem ser desenvolvidos em paralelo após Fase 2

### 2.3 Planning assumptions

* **Capacidade do time**: 1 desenvolvedor full-stack (desenvolvimento impulsionado por IA)
* **Modelo de alocação**: Dedicação integral ao projeto
* **Senioridade**: Desenvolvedor sênior com suporte de agentes de IA
* **Disponibilidade de ambiente**: Hub A-M-App-Hub disponível desde o início
* **Prontidão de dependências externas**: Acesso ao CAS disponível via hub

---

## 3. Roadmap structure

### 3.1 Delivery phases

| Fase | Nome | Objetivo | Valor entregue |
|------|------|----------|----------------|
| 1 | Provisionamento de Infraestrutura e Setup Inicial | Criar ambiente de desenvolvimento e validar autenticação CAS | Infraestrutura base + validação de acesso |
| 2 | Desenvolvimento do Backend Core com APIs Mockadas | Implementar endpoints REST com dados mockados | Backend funcional com APIs testáveis |
| 3 | Implementação do Frontend (Dashboard UI) | Desenvolver interface do dashboard com componentes React | UI completa e responsiva |
| 4 | Integração Frontend-Backend e Testes E2E | Conectar frontend ao backend e validar fluxos completos | Aplicação integrada e funcional |
| 5 | Observabilidade, Documentação e Deploy para QA | Configurar logs, health checks e preparar para produção | Aplicação pronta para validação de usuários |

### 3.2 Delivery scope per phase

**Fase 1** habilita o ambiente de desenvolvimento e valida a integração com CAS, desbloqueando o trabalho de backend e frontend.

**Fase 2** entrega o backend funcional com APIs mockadas, permitindo que o frontend seja desenvolvido em paralelo usando contratos de API definidos.

**Fase 3** implementa a interface do usuário completa, incluindo cards de métricas, gráfico de contratos, tabela de imóveis e formulário de cadastro.

**Fase 4** integra frontend e backend, validando todos os fluxos de usuário end-to-end e garantindo a qualidade da solução.

**Fase 5** adiciona observabilidade, documentação e prepara a aplicação para deploy em QA e produção.

---

## 4. Detailed roadmap

### 4.1 Consolidated timeline

| Fase | Dependências | Duração estimada | Observações |
|------|--------------|------------------|-------------|
| 1. Provisionamento de Infraestrutura e Setup Inicial | Nenhuma | Acordada com PO | Bloqueia todas as outras fases |
| 2. Desenvolvimento do Backend Core com APIs Mockadas | Fase 1 | Acordada com PO | Desbloqueia Fase 3 e 4 |
| 3. Implementação do Frontend (Dashboard UI) | Fase 1 | Acordada com PO | Pode ser paralela à Fase 2 após contratos de API definidos |
| 4. Integração Frontend-Backend e Testes E2E | Fases 2 e 3 | Acordada com PO | Requer backend e frontend completos |
| 5. Observabilidade, Documentação e Deploy para QA | Fase 4 | Acordada com PO | Última fase antes de produção |

**Nota**: Datas são acordadas entre PO e desenvolvedor no início do projeto. Não há cálculo automático de datas.

### 4.2 Delivery sequencing

| Ordem | Entregável | Fase | Dependências |
|-------|-----------|------|--------------|
| 1 | Infraestrutura GCP provisionada (hub) | 1 | Nenhuma |
| 2 | Autenticação CAS validada (spike) | 1 | Infraestrutura |
| 3 | Estrutura de projeto backend (FastAPI) | 2 | Fase 1 |
| 4 | Endpoints REST com dados mockados | 2 | Estrutura backend |
| 5 | Estrutura de projeto frontend (React + Vite) | 3 | Fase 1 |
| 6 | Componentes UI (cards, gráfico, tabela, formulário) | 3 | Estrutura frontend |
| 7 | Integração frontend-backend | 4 | Fases 2 e 3 |
| 8 | Testes E2E (Playwright) | 4 | Integração completa |
| 9 | Logs estruturados e health checks | 5 | Fase 4 |
| 10 | Documentação de APIs (OpenAPI) | 5 | Fase 4 |
| 11 | Deploy para QA | 5 | Todas as fases anteriores |

### 4.3 Parallel workstreams

Após a conclusão da **Fase 1**, as seguintes fases podem ser desenvolvidas em paralelo:

* **Fase 2 (Backend)** e **Fase 3 (Frontend)** podem ser executadas simultaneamente, desde que os contratos de API (endpoints, payloads) estejam definidos e documentados.

Esta paralelização reduz o tempo total de desenvolvimento e maximiza a eficiência do time.

---

## 5. Development estimation

### 5.1 Estimation methodology

* **Dimensionamento relativo**: Complexidade avaliada por fase (S/M/L/XL)
* **Dimensão de complexidade**: Técnica, integração, UI/UX
* **Dimensão de incerteza**: Baixa (stack conhecida), Média (integrações), Alta (novos padrões)
* **Estratégia de buffer**: Spike de autenticação CAS na Fase 1 reduz incerteza

### 5.2 Estimation by phase

| Fase | Complexidade | Incerteza | Observações |
|------|-------------|-----------|-------------|
| 1. Provisionamento de Infraestrutura e Setup Inicial | M | Baixa | Stack AS1I conhecida, processo padronizado |
| 2. Desenvolvimento do Backend Core com APIs Mockadas | M | Baixa | FastAPI + dados mockados, sem persistência |
| 3. Implementação do Frontend (Dashboard UI) | L | Média | Múltiplos componentes, gráficos, responsividade |
| 4. Integração Frontend-Backend e Testes E2E | M | Média | Integração + testes automatizados |
| 5. Observabilidade, Documentação e Deploy para QA | S | Baixa | Configurações padrão, documentação OpenAPI |

### 5.3 Estimation by component

| Componente | Complexidade | Incerteza | Observações |
|-----------|-------------|-----------|-------------|
| Infraestrutura GCP (hub) | S | Baixa | Terraform padrão AS1I |
| Autenticação CAS | M | Média | Spike necessário para validação |
| Backend FastAPI | M | Baixa | Endpoints REST simples, dados mockados |
| Frontend React | L | Média | Dashboard com múltiplos componentes |
| Gráficos (Recharts) | M | Baixa | Biblioteca madura, bem documentada |
| Testes E2E (Playwright) | M | Média | Cobertura de fluxos principais |
| Observabilidade | S | Baixa | Logs estruturados + health checks |

### 5.4 Estimation risks

* **Spike candidates**:
  - Autenticação CAS: validar integração com hub A-M-App-Hub (incluído na Fase 1)
* **Dependências externas**:
  - Acesso ao hub A-M-App-Hub (CAS): crítico, deve estar disponível desde o início
* **Novas tecnologias**:
  - Nenhuma (stack conhecida: React, FastAPI, Vite, Recharts)
* **Incerteza de integração**:
  - Integração CAS: mitigada por spike na Fase 1

---

## 6. Release calendar

### 6.1 Release strategy

* **Cadência**: Release única do MVP (v1.0)
* **Ambientes**: dev → qa → prod
* **Critérios de promoção**:
  - Dev → QA: Testes E2E passando, integração completa
  - QA → Prod: Validação de usuários (consultores A&M), sem bugs críticos
* **Janela de estabilização**: 1 semana em QA antes de produção

### 6.2 Planned releases

| Release | Escopo | Público | Observações |
|---------|--------|---------|-------------|
| MVP v1.0 (dev) | Todas as fases (1-5) | Equipe de desenvolvimento | Ambiente de desenvolvimento |
| MVP v1.0 (qa) | Todas as fases (1-5) | Consultores A&M (validação) | Validação de usuários |
| MVP v1.0 (prod) | Todas as fases (1-5) | Consultores A&M (produção) | Release oficial |

**Nota**: Datas-alvo são acordadas entre PO e desenvolvedor no início do projeto.

### 6.3 Release readiness criteria

* **Quality gates**:
  - Todos os testes E2E passando (cobertura mínima: fluxos principais)
  - Sem bugs críticos (P0) ou bloqueadores
  - Validação de regras de negócio (RN01-RN05) com PO
* **Cobertura de testes**:
  - Backend: Testes unitários para endpoints críticos
  - Frontend: Testes de componentes principais
  - E2E: Fluxos de visualização de métricas, cadastro de imóvel, consulta de tabela
* **Thresholds de performance**:
  - Carregamento do dashboard < 2s
  - Cadastro de imóvel < 1s
* **Validação de segurança**:
  - Autenticação CAS funcionando
  - Acesso restrito a usuários autenticados

---

## 7. Dependencies

### 7.1 Internal dependencies

| Item | Depende de |
|------|-----------|
| Fase 2 (Backend) | Fase 1 (Infraestrutura) |
| Fase 3 (Frontend) | Fase 1 (Infraestrutura) |
| Fase 4 (Integração) | Fases 2 e 3 (Backend + Frontend) |
| Fase 5 (Observabilidade) | Fase 4 (Integração completa) |

### 7.2 External dependencies

| Item | Owner | Impacto |
|------|-------|---------|
| Acesso ao hub A-M-App-Hub (CAS) | Equipe de Infraestrutura A&M | Crítico — bloqueia autenticação (Fase 1) |
| Validação de regras de negócio (RN01-RN05) | Product Owner | Alto — impacta lógica de cálculo de métricas (Fase 2) |
| Feedback de consultores A&M | Usuários-alvo | Médio — impacta ajustes de UX (Fase 5, QA) |

### 7.3 Critical path

O **caminho crítico** do projeto é:

1. **Fase 1 (Infraestrutura)** → Desbloqueia todo o desenvolvimento
2. **Fase 2 (Backend)** → Desbloqueia integração
3. **Fase 4 (Integração)** → Desbloqueia validação E2E
4. **Fase 5 (Observabilidade)** → Desbloqueia deploy para QA/Prod

A **Fase 3 (Frontend)** pode ser paralelizada com a Fase 2, mas a integração (Fase 4) depende de ambas estarem completas.

---

## 8. Structured backlog (hierarchical)

### 8.1 Epic

**Épico Único**: Dashboard de Gestão Imobiliária (Real Estate Control)

**Valor de negócio**:
- Redução de 60% no tempo de consolidação de informações de portfólio imobiliário
- Acesso em tempo real a métricas críticas (receita, ocupação, inadimplência)
- Fonte única de verdade para gestão de imóveis e contratos

**Métricas de sucesso**:
- Taxa de adoção > 80% (consultores A&M) em 4 semanas
- Tempo de carregamento do dashboard < 2s
- Número de imóveis cadastrados > 50 em 4 semanas (MVP)
- Tempo médio de cadastro de imóvel < 1 minuto

**Critérios de aceite do Épico**:
- AC-E.1: Dashboard exibe cards de métricas (receita, ocupação, inadimplência) com dados mockados
- AC-E.2: Gráfico de novos contratos exibe dados dos últimos 12 meses
- AC-E.3: Tabela de imóveis lista registros ordenados por data de cadastro (mais recentes primeiro) com paginação
- AC-E.4: Formulário de cadastro valida campos obrigatórios e salva imóvel em memória
- AC-E.5: Autenticação via CAS funciona corretamente (acesso restrito a usuários autenticados)
- AC-E.6: Aplicação é responsiva (desktop priority, funcional em tablets)
- AC-E.7: Testes E2E cobrem fluxos principais (visualização de métricas, cadastro de imóvel, consulta de tabela)

### 8.2 Fases (agregadores)

As fases representam blocos substanciais de desenvolvimento. Cada fase é uma unidade de trabalho que pode ser completada em um prompt bem estruturado de workflow agnóstico.

**Total de fases**: 5

---

## 9. Executable backlog (hierarchical list)

### Épico: Dashboard de Gestão Imobiliária (Real Estate Control)

---

#### Fase 1: Provisionamento de Infraestrutura e Setup Inicial

**Descrição**:
Provisionar infraestrutura GCP via Terraform (arquétipo AS1I), configurar hub A-M-App-Hub, validar autenticação CAS e preparar ambiente de desenvolvimento local.

**Critérios de aceite**:
- AC-1.1: Infraestrutura GCP provisionada via Terraform (ambiente dev)
- AC-1.2: Hub A-M-App-Hub configurado com acesso CAS
- AC-1.3: Spike de autenticação CAS concluído com sucesso (validação de login)
- AC-1.4: Repositório GitHub configurado com CI/CD básico (GitHub Actions)
- AC-1.5: Estrutura de pastas do projeto criada (backend, frontend, docs)

**Dependências**: Nenhuma (fase inicial)

**Critérios de prontidão**:
- Acesso ao hub A-M-App-Hub disponível
- Credenciais GCP configuradas
- Repositório GitHub criado (A-M-App-Hub/real-estate-control)

**Datas**: Acordadas com PO

---

#### Fase 2: Desenvolvimento do Backend Core com APIs Mockadas

**Descrição**:
Implementar backend FastAPI com endpoints REST para métricas, gráfico de contratos, listagem de imóveis e cadastro de imóvel. Dados mockados em memória (sem persistência real).

**Critérios de aceite**:
- AC-2.1: Endpoint `GET /api/metricas` retorna receita, taxa de ocupação e inadimplência (dados mockados)
- AC-2.2: Endpoint `GET /api/contratos/novos-por-mes` retorna dados para gráfico de barras (últimos 12 meses)
- AC-2.3: Endpoint `GET /api/imoveis` retorna lista de imóveis com paginação (query params `page` e `limit`)
- AC-2.4: Endpoint `POST /api/imoveis` cadastra novo imóvel (validação de campos obrigatórios)
- AC-2.5: Endpoint `GET /health` retorna status do backend
- AC-2.6: Documentação OpenAPI gerada automaticamente (FastAPI Swagger UI)
- AC-2.7: Testes unitários para endpoints críticos (cobertura mínima: 80%)

**Dependências**: Fase 1 (Infraestrutura)

**Critérios de prontidão**:
- Infraestrutura GCP disponível (Fase 1 completa)
- Estrutura de projeto backend criada

**Datas**: Acordadas com PO

---

#### Fase 3: Implementação do Frontend (Dashboard UI)

**Descrição**:
Desenvolver interface do dashboard com React + TypeScript + Vite. Implementar cards de métricas, gráfico de contratos (Recharts), tabela de imóveis e formulário de cadastro. Interface responsiva (desktop priority, funcional em tablets).

**Critérios de aceite**:
- AC-3.1: Cards de métricas exibem receita, taxa de ocupação e inadimplência (mockados localmente ou via API)
- AC-3.2: Gráfico de barras exibe novos contratos por mês (Recharts, interativo com tooltip)
- AC-3.3: Tabela de imóveis exibe colunas (Endereço, Tipo, Status, Valor Aluguel) com paginação
- AC-3.4: Formulário de cadastro valida campos obrigatórios e exibe feedback visual (toast)
- AC-3.5: Header/Topbar exibe logo A&M, título do dashboard e informações do usuário
- AC-3.6: Interface é responsiva (desktop priority, funcional em tablets)
- AC-3.7: Estados vazios e de erro implementados (skeleton loaders, mensagens de erro)

**Dependências**: Fase 1 (Infraestrutura)

**Critérios de prontidão**:
- Contratos de API definidos (endpoints, payloads) — pode ser paralelo à Fase 2
- Estrutura de projeto frontend criada

**Datas**: Acordadas com PO

---

#### Fase 4: Integração Frontend-Backend e Testes E2E

**Descrição**:
Conectar frontend ao backend via chamadas HTTP, validar fluxos completos de usuário e implementar testes E2E com Playwright.

**Critérios de aceite**:
- AC-4.1: Frontend consome endpoints do backend (métricas, gráfico, tabela, cadastro)
- AC-4.2: Fluxo de visualização de métricas funciona end-to-end
- AC-4.3: Fluxo de cadastro de imóvel funciona end-to-end (validação + feedback)
- AC-4.4: Fluxo de consulta de tabela funciona end-to-end (paginação)
- AC-4.5: Testes E2E implementados com Playwright (cobertura de fluxos principais)
- AC-4.6: Tratamento de erros implementado (timeout, erro de API, validação)
- AC-4.7: Performance validada (carregamento do dashboard < 2s, cadastro < 1s)

**Dependências**: Fases 2 e 3 (Backend + Frontend)

**Critérios de prontidão**:
- Backend completo com APIs funcionais (Fase 2 completa)
- Frontend completo com componentes implementados (Fase 3 completa)

**Datas**: Acordadas com PO

---

#### Fase 5: Observabilidade, Documentação e Deploy para QA

**Descrição**:
Configurar logs estruturados, health checks, documentação de APIs (OpenAPI) e preparar aplicação para deploy em QA e produção.

**Critérios de aceite**:
- AC-5.1: Logs estruturados implementados no backend (formato JSON, níveis INFO/ERROR)
- AC-5.2: Health checks implementados (`/health` endpoint com status de dependências)
- AC-5.3: Documentação OpenAPI completa e acessível via Swagger UI
- AC-5.4: README atualizado com instruções de setup e execução local
- AC-5.5: Deploy para ambiente QA concluído com sucesso
- AC-5.6: Validação de usuários (consultores A&M) realizada em QA
- AC-5.7: Bugs críticos (P0) corrigidos antes de deploy para produção

**Dependências**: Fase 4 (Integração completa)

**Critérios de prontidão**:
- Integração frontend-backend completa e validada (Fase 4 completa)
- Testes E2E passando

**Datas**: Acordadas com PO

---

## 10. Execution governance

### 10.1 Ceremonies

* **Backlog refinement**: Semanal (30 min) — revisar fases, ajustar prioridades
* **Sprint planning**: Início de cada fase — definir escopo e critérios de aceite
* **Sync meetings**: Diário (15 min) — status, blockers, próximos passos
* **Review**: Final de cada fase — demo de funcionalidades, validação com PO
* **Retrospective**: Final do MVP — lições aprendidas, melhorias para próximas iterações

### 10.2 Quality gates

* **Fase 1**: Autenticação CAS validada (spike concluído)
* **Fase 2**: Testes unitários passando (cobertura mínima 80%)
* **Fase 3**: Interface responsiva validada (desktop + tablet)
* **Fase 4**: Testes E2E passando (cobertura de fluxos principais)
* **Fase 5**: Deploy para QA concluído, validação de usuários

### 10.3 Risk management

* **Risco**: Integração CAS falha
  - **Mitigação**: Spike na Fase 1 para validação antecipada
* **Risco**: Performance abaixo do esperado
  - **Mitigação**: Validação de performance na Fase 4 (< 2s carregamento)
* **Risco**: Adoção baixa por usuários
  - **Mitigação**: Envolver consultores A&M no feedback do MVP (Fase 5, QA)

### 10.4 Communication plan

* **Stakeholders**: Product Owner, Consultores A&M (usuários-alvo), Equipe de Infraestrutura A&M
* **Canais**: Slack (#real-estate-control), e-mail, reuniões de review
* **Frequência**: Semanal (status report), final de cada fase (demo)

---

## 11. Next steps

Após a aprovação deste roadmap:

1. **Definir datas de início e fim por fase** (acordo PO-desenvolvedor)
2. **Gerar story files** para cada fase (handoff para Dev Agent)
3. **Sincronizar com Jira** (opcional, via MCP)
4. **Executar Fase 1** (Provisionamento de Infraestrutura e Setup Inicial)

---

**Roadmap gerado por**: roadmap-engineer (DeepAgent)  
**Data**: 2026-07-16  
**Variante**: Equilibrado (selecionado automaticamente — padrão esteira-condutora)
