---
source_roadmap: roadmap_equilibrado.md
phase_index: 3
phase_title: "Implementação do Frontend (Dashboard UI)"
epic_title: "Dashboard de Gestão Imobiliária (Real Estate Control)"
generated_at: "2026-07-16T14:30:00"
---

# Story: Implementação do Frontend (Dashboard UI)

## Context

Desenvolver interface do dashboard com React + TypeScript + Vite. Implementar cards de métricas, gráfico de contratos (Recharts), tabela de imóveis e formulário de cadastro. Interface responsiva (desktop priority, funcional em tablets).

**Objetivo**: Criar UI completa e responsiva do dashboard com todos os componentes visuais e interativos.

**Limites de entrega**: Frontend React funcional com cards de métricas, gráfico de barras, tabela paginada, formulário de cadastro e estados de erro/vazio.

## Tasks

- [ ] Criar estrutura do projeto frontend React + TypeScript + Vite
  - [ ] Executar `npm create vite@latest` com template react-ts
  - [ ] Configurar tsconfig.json e vite.config.ts
  - [ ] Instalar dependências (React, TypeScript, Recharts, Axios, React Router)
- [ ] Implementar Header/Topbar
  - [ ] Logo A&M (placeholder ou imagem real)
  - [ ] Título "Dashboard de Gestão Imobiliária"
  - [ ] Informações do usuário logado (nome, avatar)
  - [ ] Botão de logout (placeholder)
- [ ] Implementar Cards de Métricas
  - [ ] Card 1: Receita de Aluguéis (R$) — ícone cifrão, cor verde
  - [ ] Card 2: Taxa de Ocupação (%) — ícone casa, cor azul
  - [ ] Card 3: Inadimplência (%) — ícone alerta, cor vermelho
  - [ ] Consumir dados de /api/metricas (mockados localmente se backend não disponível)
  - [ ] Implementar skeleton loader durante carregamento
  - [ ] Implementar estado de erro com botão de retry
- [ ] Implementar Gráfico de Novos Contratos
  - [ ] Usar Recharts (BarChart) para gráfico de barras verticais
  - [ ] Eixo X: Meses (últimos 12 meses, ex: Jan/26, Fev/26)
  - [ ] Eixo Y: Quantidade de contratos
  - [ ] Tooltip interativo ao passar o mouse (mês + quantidade)
  - [ ] Consumir dados de /api/contratos/novos-por-mes
  - [ ] Implementar skeleton loader durante carregamento
  - [ ] Implementar estado de erro com mensagem
- [ ] Implementar Tabela de Imóveis
  - [ ] Colunas: Endereço/Código, Tipo (badge), Status (badge colorido), Valor Aluguel/Condomínio (R$)
  - [ ] Ordenação por data de cadastro (mais recentes primeiro)
  - [ ] Paginação (10 itens por página, controles de navegação)
  - [ ] Consumir dados de /api/imoveis (query params page e limit)
  - [ ] Implementar skeleton loader durante carregamento
  - [ ] Implementar estado vazio ("Nenhum imóvel cadastrado. Cadastre o primeiro imóvel usando o formulário abaixo.")
  - [ ] Implementar estado de erro com botão de retry
- [ ] Implementar Formulário de Cadastro de Imóvel
  - [ ] Campos: Proprietário (text), Endereço (text), Tipo (dropdown), Status Inicial (dropdown), Valor Sugerido de Aluguel (number)
  - [ ] Validação de campos obrigatórios (exibir mensagens de erro abaixo de cada campo)
  - [ ] Botão "Cadastrar" (primary button)
  - [ ] Enviar POST para /api/imoveis ao submeter
  - [ ] Exibir toast verde "Imóvel cadastrado com sucesso!" em caso de sucesso
  - [ ] Exibir toast vermelho "Erro ao cadastrar imóvel." em caso de erro
  - [ ] Limpar formulário após sucesso
  - [ ] Atualizar tabela de imóveis automaticamente após cadastro
- [ ] Implementar responsividade
  - [ ] Layout desktop (> 1024px): cards em linha, gráfico e tabela lado a lado
  - [ ] Layout tablet (768px - 1024px): cards em linha, gráfico e tabela empilhados
  - [ ] Validar em diferentes resoluções
- [ ] Implementar estados de erro e vazio
  - [ ] Skeleton loaders para carregamento
  - [ ] Mensagens de erro com botão de retry
  - [ ] Estado vazio para tabela sem dados
- [ ] Configurar comunicação com backend
  - [ ] Criar serviço Axios com baseURL configurável (variável de ambiente)
  - [ ] Implementar interceptors para tratamento de erros (timeout, 4xx, 5xx)

## Acceptance Criteria

- AC-3.1: Cards de métricas exibem receita, taxa de ocupação e inadimplência (mockados localmente ou via API) — valores exibidos corretamente, skeleton loader funciona
- AC-3.2: Gráfico de barras exibe novos contratos por mês (Recharts, interativo com tooltip) — gráfico renderiza, tooltip funciona ao passar o mouse
- AC-3.3: Tabela de imóveis exibe colunas (Endereço, Tipo, Status, Valor Aluguel) com paginação — tabela renderiza, paginação funciona (10 itens por página)
- AC-3.4: Formulário de cadastro valida campos obrigatórios e exibe feedback visual (toast) — validação funciona, toast verde/vermelho exibido corretamente
- AC-3.5: Header/Topbar exibe logo A&M, título do dashboard e informações do usuário — header renderiza corretamente
- AC-3.6: Interface é responsiva (desktop priority, funcional em tablets) — layout ajusta corretamente em desktop (> 1024px) e tablet (768px - 1024px)
- AC-3.7: Estados vazios e de erro implementados (skeleton loaders, mensagens de erro) — skeleton loaders funcionam, mensagens de erro exibidas corretamente

## Worktree Config

- **story-slug**: implementacao-frontend-dashboard-ui
- **branch-name**: story/implementacao-frontend-dashboard-ui
- **base-branch**: main

## Test Strategy

- **unit-test-runner**: npm test
- **e2e-required**: sim
- **coverage-threshold**: 80
- **test-paths**: src/__tests__/

## PR Config

- **draft**: true
- **base**: main
- **labels**: ["story/implementacao-frontend-dashboard-ui", "frontend", "ui"]

## Autonomy Blockers

- **Contratos de API não definidos**: Se o backend ainda não estiver pronto, usar dados mockados localmente e validar contratos de API (endpoints, payloads) antes de integrar. Documentar premissas sobre estrutura de dados.
- **Design System não disponível**: PRD menciona conformidade obrigatória com Design System (`boas_praticas_e_conhecimentos/biblioteca_de_agent_skills/esteira_de_desenvolvimento/references/design-system.md`). Se o arquivo não existir, usar componentes básicos do React e documentar desvios. Validar com PO se há biblioteca de componentes disponível (ex: Material-UI, Ant Design, Chakra UI).
- **Logo A&M não disponível**: Usar placeholder ou texto "A&M" até que logo oficial seja fornecido.

## Technical Notes

- **Dependências**: Fase 1 (Infraestrutura) — repositório e estrutura de projeto devem estar prontos
- **Pontos de integração**: 
  - Backend FastAPI (consumidor das APIs REST)
  - Recharts (biblioteca de gráficos)
  - Axios (cliente HTTP)
- **Riscos**: 
  - Design System pode não estar disponível — usar componentes básicos e documentar desvios
  - Integração com backend pode revelar incompatibilidades de contrato — validar payloads antecipadamente
  - Responsividade pode ter edge cases em resoluções intermediárias — testar em múltiplas resoluções
- **Referencias**: 
  - PRD: `docs/planning/real-estate-control-prd.md` (seção 8.2 — Telas e Visualizações Principais, seção 9 — Design System e UI/UX)
  - Blueprint: `docs/planning/blueprints/blueprint-AS1I-rendered.md` (stack React + Vite)
  - Design System: `boas_praticas_e_conhecimentos/biblioteca_de_agent_skills/esteira_de_desenvolvimento/references/design-system.md` (se disponível)
- **Stack**: React 18+, TypeScript, Vite, Recharts, Axios, CSS Modules ou Styled Components
- **Regra Lovable**: Priorizar experiência do usuário — feedback visual imediato, estados de carregamento claros, mensagens de erro amigáveis
