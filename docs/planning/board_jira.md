# Board Jira — Dashboard de Gestão Imobiliária (Real Estate Control)

## Informações do Board

**Tipo de Board**: Scrum  
**Épico**: Dashboard de Gestão Imobiliária (Real Estate Control)  
**Project Key**: A definir (ex: REC)  
**Roadmap Fonte**: roadmap_equilibrado.md

---

## Status Disponíveis (Scrum Board)

| Status | Descrição |
|--------|-----------|
| **Backlog** | Fases planejadas, aguardando início |
| **To Do** | Fases prontas para execução |
| **In Progress** | Fases em desenvolvimento |
| **Done** | Fases concluídas |
| **Cancelado** | Fases canceladas ou removidas do escopo |

---

## Fases do Épico

| # | Título da Fase | Descrição | Critérios de Aceite | Data Início | Data Fim | Release Alvo | Dependências | Status |
|---|---------------|-----------|---------------------|-------------|----------|--------------|--------------|--------|
| 1 | Provisionamento de Infraestrutura e Setup Inicial | Provisionar infraestrutura GCP via Terraform (arquétipo AS1I), configurar hub A-M-App-Hub, validar autenticação CAS e preparar ambiente de desenvolvimento local. | AC-1.1: Infraestrutura GCP provisionada via Terraform (ambiente dev)<br>AC-1.2: Hub A-M-App-Hub configurado com acesso CAS<br>AC-1.3: Spike de autenticação CAS concluído com sucesso (validação de login)<br>AC-1.4: Repositório GitHub configurado com CI/CD básico (GitHub Actions)<br>AC-1.5: Estrutura de pastas do projeto criada (backend, frontend, docs) | | | MVP v1.0 | Nenhuma | Backlog |
| 2 | Desenvolvimento do Backend Core com APIs Mockadas | Implementar backend FastAPI com endpoints REST para métricas, gráfico de contratos, listagem de imóveis e cadastro de imóvel. Dados mockados em memória (sem persistência real). | AC-2.1: Endpoint GET /api/metricas retorna receita, taxa de ocupação e inadimplência (dados mockados)<br>AC-2.2: Endpoint GET /api/contratos/novos-por-mes retorna dados para gráfico de barras (últimos 12 meses)<br>AC-2.3: Endpoint GET /api/imoveis retorna lista de imóveis com paginação (query params page e limit)<br>AC-2.4: Endpoint POST /api/imoveis cadastra novo imóvel (validação de campos obrigatórios)<br>AC-2.5: Endpoint GET /health retorna status do backend<br>AC-2.6: Documentação OpenAPI gerada automaticamente (FastAPI Swagger UI)<br>AC-2.7: Testes unitários para endpoints críticos (cobertura mínima: 80%) | | | MVP v1.0 | Fase 1 | Backlog |
| 3 | Implementação do Frontend (Dashboard UI) | Desenvolver interface do dashboard com React + TypeScript + Vite. Implementar cards de métricas, gráfico de contratos (Recharts), tabela de imóveis e formulário de cadastro. Interface responsiva (desktop priority, funcional em tablets). | AC-3.1: Cards de métricas exibem receita, taxa de ocupação e inadimplência (mockados localmente ou via API)<br>AC-3.2: Gráfico de barras exibe novos contratos por mês (Recharts, interativo com tooltip)<br>AC-3.3: Tabela de imóveis exibe colunas (Endereço, Tipo, Status, Valor Aluguel) com paginação<br>AC-3.4: Formulário de cadastro valida campos obrigatórios e exibe feedback visual (toast)<br>AC-3.5: Header/Topbar exibe logo A&M, título do dashboard e informações do usuário<br>AC-3.6: Interface é responsiva (desktop priority, funcional em tablets)<br>AC-3.7: Estados vazios e de erro implementados (skeleton loaders, mensagens de erro) | | | MVP v1.0 | Fase 1 | Backlog |
| 4 | Integração Frontend-Backend e Testes E2E | Conectar frontend ao backend via chamadas HTTP, validar fluxos completos de usuário e implementar testes E2E com Playwright. | AC-4.1: Frontend consome endpoints do backend (métricas, gráfico, tabela, cadastro)<br>AC-4.2: Fluxo de visualização de métricas funciona end-to-end<br>AC-4.3: Fluxo de cadastro de imóvel funciona end-to-end (validação + feedback)<br>AC-4.4: Fluxo de consulta de tabela funciona end-to-end (paginação)<br>AC-4.5: Testes E2E implementados com Playwright (cobertura de fluxos principais)<br>AC-4.6: Tratamento de erros implementado (timeout, erro de API, validação)<br>AC-4.7: Performance validada (carregamento do dashboard < 2s, cadastro < 1s) | | | MVP v1.0 | Fases 2 e 3 | Backlog |
| 5 | Observabilidade, Documentação e Deploy para QA | Configurar logs estruturados, health checks, documentação de APIs (OpenAPI) e preparar aplicação para deploy em QA e produção. | AC-5.1: Logs estruturados implementados no backend (formato JSON, níveis INFO/ERROR)<br>AC-5.2: Health checks implementados (/health endpoint com status de dependências)<br>AC-5.3: Documentação OpenAPI completa e acessível via Swagger UI<br>AC-5.4: README atualizado com instruções de setup e execução local<br>AC-5.5: Deploy para ambiente QA concluído com sucesso<br>AC-5.6: Validação de usuários (consultores A&M) realizada em QA<br>AC-5.7: Bugs críticos (P0) corrigidos antes de deploy para produção | | | MVP v1.0 | Fase 4 | Backlog |

---

## Observações

- **Datas**: Acordadas entre PO e desenvolvedor no início do projeto (não calculadas automaticamente)
- **Hierarquia**: Épico → Fase (sem subtasks ou stories no Jira)
- **Paralelização**: Fases 2 e 3 podem ser executadas em paralelo após contratos de API definidos
- **Caminho Crítico**: Fase 1 → Fase 2 → Fase 4 → Fase 5

---

**Gerado por**: roadmap-engineer (DeepAgent)  
**Data**: 2026-07-16  
**Variante**: Equilibrado
