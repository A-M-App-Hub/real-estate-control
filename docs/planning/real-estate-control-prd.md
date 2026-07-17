# PRD — Dashboard de Gestão Imobiliária (Real Estate Control)

---

## Metadados do Projeto

| Campo | Valor |
|-------|-------|
| **Projeto / Feature** | Dashboard de Gestão Imobiliária (Real Estate Control) |
| **Data** | 2026-07-16 |
| **Status** | Draft |
| **Responsável pelo preenchimento** | Equipe de Desenvolvimento A&M |
| **Stakeholders envolvidos** | Consultores A&M (usuários finais) |
| **Prazo esperado (MVP)** | 4 semanas <!-- PREMISSA: prazo padrão POC AS1I --> |
| **Link do protótipo (Figma, Lovable, URL)** | A definir |
| **Link do Discovery / documento de referência** | `/workspace/real-estate-control/docs/planning/solution-brief.yaml` |
| **PO / responsável por validar regras de negócio** | A definir <!-- PREMISSA: POC interna --> |

---

## PARTE A — PRODUTO

---

## 1. Visão Geral do Produto

### 1.1 Resumo Executivo

O **Dashboard de Gestão Imobiliária** é um painel administrativo interno para consultores A&M controlarem contratos de aluguel, imóveis e proprietários de forma centralizada. O sistema oferece visibilidade em tempo real de métricas-chave (receita, ocupação, inadimplência), histórico de contratos e cadastro simplificado de imóveis, permitindo decisões data-driven e reduzindo o esforço manual de consolidação de informações.

### 1.2 Problema

- **Controle descentralizado:** Informações de imóveis, contratos e pagamentos espalhadas em planilhas, e-mails e sistemas desconectados
- **Falta de visibilidade:** Dificuldade em obter visão consolidada de métricas críticas (receita, ocupação, inadimplência) em tempo real
- **Esforço manual elevado:** Tempo gasto em consolidação manual de dados para tomada de decisão e geração de relatórios
- **Risco de inconsistências:** Dados duplicados ou desatualizados devido à falta de fonte única de verdade

### 1.3 Proposta de Valor

| Dimensão | Impacto esperado |
|----------|-----------------|
| **Eficiência operacional** | Redução de 60% no tempo de consolidação de informações de portfólio imobiliário |
| **Visibilidade de negócio** | Acesso em tempo real a métricas críticas (receita, ocupação, inadimplência) em um único painel |
| **Qualidade de decisão** | Decisões baseadas em dados consolidados e atualizados, reduzindo risco de erro |
| **Centralização** | Fonte única de verdade para gestão de imóveis, contratos e pagamentos |

### 1.4 Usuários-Alvo

| Perfil | Descrição | Necessidade principal |
|--------|-----------|----------------------|
| **Primário** | Consultores A&M (internos) | Visualizar métricas de portfólio, cadastrar novos imóveis, consultar histórico de contratos e identificar inadimplências |
| **Secundário** | Gestores/Líderes de Projetos | Acompanhar performance do portfólio e tomar decisões estratégicas baseadas em KPIs consolidados |

---

## 2. Escopo e Features

### 2.1 Lista de Features

| # | Feature | MVP? | Prioridade (P0-P3) | Complexidade (S/M/L/XL) | Descrição |
|---|---------|------|--------------------|--------------------------|-----------|
| 1 | Cards de Métricas | Sim | P0 | S | Exibir 3 cards no topo da página: Receita de Aluguéis (R$), Taxa de Ocupação (%), Inadimplência (%) |
| 2 | Gráfico de Novos Contratos | Sim | P0 | M | Gráfico de barras mostrando quantidade de novos contratos assinados por mês (últimos 12 meses) |
| 3 | Tabela de Imóveis | Sim | P0 | M | Listar imóveis cadastrados (ordenados por data de cadastro, mais recentes primeiro) com colunas: Endereço/Código, Tipo, Status, Valor Aluguel/Condomínio. Incluir paginação. |
| 4 | Formulário de Cadastro de Imóvel | Sim | P0 | M | Formulário para cadastrar novo imóvel com campos: Proprietário, Endereço, Tipo, Status Inicial, Valor Sugerido de Aluguel. Validação de campos obrigatórios e feedback visual. |

### 2.2 Escopo do MVP

**Incluso no MVP:**
- Dashboard principal com cards de métricas (receita, ocupação, inadimplência)
- Gráfico de barras de novos contratos (últimos 12 meses)
- Tabela de imóveis cadastrados com ordenação e paginação
- Formulário de cadastro de novo imóvel com validação
- Autenticação via CAS (hub AS1I)
- Interface responsiva (desktop priority, funcional em tablets)
- Dados mockados (persistência em memória no backend FastAPI)

**Fora do escopo MVP (futuro):**
- Persistência real em banco de dados (Firestore/Cloud SQL)
- Gestão completa de contratos (CRUD, renovações, rescisões)
- Gestão de pagamentos e fluxo de cobrança
- Exportação de relatórios (Excel, PDF)
- Notificações automáticas (e-mail, in-app)
- Integração com sistemas contábeis/ERP
- Dashboards analíticos avançados (BI)

**Features explicitamente fora do escopo:**
- Gestão de manutenção de imóveis
- Portal do inquilino (self-service)
- Integração com plataformas de anúncio (Airbnb, OLX, etc.)
- Assinatura digital de contratos

---

## 3. Jornadas do Usuário

### 3.1 Personas

| Persona | Descrição | Ações principais |
|---------|-----------|-----------------|
| **Consultor A&M** | Profissional interno responsável por gerenciar portfólio de imóveis de clientes | Visualizar métricas, cadastrar imóveis, consultar histórico, identificar inadimplências |
| **Gestor/Líder** | Líder de projeto ou área que acompanha performance do portfólio | Visualizar KPIs consolidados, tomar decisões estratégicas |

### 3.2 Fluxos Principais

#### Fluxo 1: Visualizar Métricas do Portfólio

**Persona:** Consultor A&M  
**Objetivo:** Obter visão consolidada da performance do portfólio imobiliário  
**Passos:**
1. Usuário acessa o dashboard (autenticação via CAS)
2. Sistema exibe cards de métricas no topo: Receita de Aluguéis, Taxa de Ocupação, Inadimplência
3. Sistema exibe gráfico de novos contratos (últimos 12 meses)
4. Usuário visualiza e interpreta as informações

**Pontos de decisão:**
- Identificar tendências de crescimento/queda de contratos
- Detectar inadimplência acima do esperado e acionar ações corretivas

**Cenários de erro:**
- Erro ao carregar métricas: exibir mensagem "Erro ao carregar dados. Tente novamente." com botão de retry
- Timeout na API: exibir skeleton loader e mensagem de carregamento

#### Fluxo 2: Cadastrar Novo Imóvel

**Persona:** Consultor A&M  
**Objetivo:** Adicionar novo imóvel ao portfólio  
**Passos:**
1. Usuário acessa o formulário de cadastro na página principal
2. Usuário preenche campos obrigatórios: Proprietário, Endereço, Tipo, Status Inicial, Valor Sugerido de Aluguel
3. Usuário clica em "Cadastrar"
4. Sistema valida campos obrigatórios
5. Sistema salva o imóvel (em memória no MVP)
6. Sistema exibe feedback de sucesso (toast/snackbar verde) e limpa o formulário
7. Tabela de imóveis é atualizada automaticamente com o novo registro

**Pontos de decisão:**
- Escolha do tipo de imóvel (Residencial, Comercial, Terreno)
- Definição do status inicial (Disponível, Em Manutenção)

**Cenários de erro:**
- Campos obrigatórios vazios: exibir mensagens de validação abaixo de cada campo
- Erro ao salvar: exibir toast vermelho "Erro ao cadastrar imóvel. Tente novamente."
- Valor de aluguel inválido (não numérico): exibir mensagem "Valor deve ser um número válido"

#### Fluxo 3: Consultar Imóveis Cadastrados

**Persona:** Consultor A&M  
**Objetivo:** Visualizar lista de imóveis do portfólio  
**Passos:**
1. Usuário acessa a tabela de imóveis na página principal
2. Sistema exibe imóveis ordenados por data de cadastro (mais recentes primeiro)
3. Usuário visualiza colunas: Endereço/Código, Tipo, Status, Valor Aluguel/Condomínio
4. Usuário navega entre páginas (paginação)

**Pontos de decisão:**
- Identificar imóveis disponíveis para locação
- Verificar valores de aluguel praticados

**Cenários de erro:**
- Nenhum imóvel cadastrado: exibir estado vazio "Nenhum imóvel cadastrado. Cadastre o primeiro imóvel usando o formulário acima."
- Erro ao carregar tabela: exibir mensagem de erro com botão de retry

### 3.3 Regras de Negócio Críticas

| Regra | Descrição | Impacto no fluxo |
|-------|-----------|-----------------|
| **RN01 - Cálculo de Receita** | Receita de Aluguéis = soma do valor mensal de todos os contratos com status "Ativo" no mês corrente | Afeta card de métrica "Receita de Aluguéis" |
| **RN02 - Cálculo de Taxa de Ocupação** | Taxa de Ocupação (%) = (Imóveis com status "Alugado" / Total de Imóveis) * 100 | Afeta card de métrica "Taxa de Ocupação" |
| **RN03 - Cálculo de Inadimplência** | Inadimplência (%) = (Contratos com pagamentos em atraso no mês / Total de Contratos Ativos) * 100 | Afeta card de métrica "Inadimplência" |
| **RN04 - Validação de Cadastro** | Campos obrigatórios: Proprietário, Endereço, Tipo, Status Inicial, Valor Sugerido de Aluguel | Bloqueia cadastro se campos vazios |
| **RN05 - Ordenação de Imóveis** | Tabela de imóveis sempre ordenada por data de cadastro (mais recentes primeiro) | Define ordem de exibição na tabela |

---

## 4. Métricas de Sucesso (KPIs)

### 4.1 KPIs de Negócio

| Métrica | Baseline | Target |
|---------|---------|--------|
| Receita de Aluguéis (R$) | A definir <!-- PREMISSA: depende de dados históricos --> | A definir |
| Taxa de Ocupação (%) | A definir | A definir |
| Inadimplência (%) | A definir | A definir |

### 4.2 KPIs de Produto / Operacionais

| Métrica | Baseline | Target |
|---------|---------|--------|
| Tempo de carregamento do dashboard | N/A | < 2s |
| Taxa de adoção (usuários ativos / total de consultores) | 0% | > 80% em 4 semanas |
| Número de imóveis cadastrados | 0 | > 50 em 4 semanas (MVP) |
| Tempo médio de cadastro de imóvel | N/A | < 1 minuto |

---

## 5. Backlog Futuro

<!-- PREMISSA: features típicas pós-MVP para dashboard de gestão imobiliária -->

| Feature | Categoria | Justificativa do diferimento |
|---------|-----------|------------------------------|
| Persistência real (Firestore/Cloud SQL) | Infraestrutura | MVP usa dados mockados; persistência real exige arquétipo AS3I e planejamento de schema |
| Exportação de relatórios (Excel, PDF) | Funcionalidade | Não crítico para validação inicial; pode ser adicionado após feedback de usuários |
| Gestão completa de contratos (CRUD) | Funcionalidade | MVP foca em visualização; CRUD completo exige modelagem de workflow e validações complexas |
| Notificações automáticas (inadimplência, vencimentos) | Funcionalidade | Requer integração com serviço de e-mail/push; não crítico para POC |
| Integração com sistemas contábeis/ERP | Integração | Depende de definição de sistemas-alvo e APIs disponíveis |
| Dashboards analíticos avançados (BI) | Funcionalidade | Requer volume de dados históricos e definição de análises específicas |
| Gestão de manutenção de imóveis | Funcionalidade | Escopo adicional; pode ser feature futura conforme demanda |

---

## PARTE B — TÉCNICO ESSENCIAL

---

## 6. Plataforma e Infraestrutura

### 6.1 Stack Tecnológica

<!-- INFERIDO: arquétipo AS1I + requisitos do usuário -->

| Camada | Tecnologia | Justificativa |
|--------|-----------|---------------|
| **Backend** | FastAPI (Python 3.13+) | Padrão esteira AS1I, performance, tipagem forte, OpenAPI nativo |
| **Frontend** | React + TypeScript + Vite | Padrão esteira AS1I, ecossistema maduro, componentes reutilizáveis |
| **Banco de Dados** | Nenhum (dados mockados em memória) | MVP AS1I com `persistence: none` — dados em memória no backend FastAPI |
| **Mobile / Responsividade** | Responsivo web (desktop priority, funcional em tablets) | Usuários internos A&M usam primariamente desktop; responsividade garante acesso em tablets |
| **Gráficos** | Recharts ou Chart.js | Bibliotecas React para gráficos interativos |

### 6.2 Infraestrutura

**Hub App Space (AS1I — padrão esteira-condutora):**

| Campo | Valor |
|-------|-------|
| Topologia | FastAPI_Mixed (backend + SPA servido pelo FastAPI) + INTERNAL_CAS |
| Deploy | app-space-infra (hub) + Bootstrap Hub + Deploy Solution |
| Auth | CAS (auth-proxy hub) — autenticação SSO interna A&M |
| OpenAPI | `openapi/hub-fragment.yaml` + register-hub |
| Persistência | `none` (dados mockados em memória no backend) |
| Ambientes | 3 ambientes padrão: dev (d), qa (q), prod (p) |
| CI/CD | GitHub Actions via forge hub |

### 6.3 FinOps

<!-- PREMISSA: AS1I hub-hosted, sem custos significativos de infra própria -->

| Campo | Valor |
|-------|-------|
| Orçamento estimado (MVP) | Baixo (< $50/mês) — hub-hosted, sem banco de dados, tráfego interno |
| Volume esperado de usuários (inicial) | 10-20 consultores A&M (internos) |
| Responsável por acompanhar custos | A definir |

---

## 7. Acessos e segurança (alto nível)

<!-- INFERIDO: arquétipo AS1I hub -->

| Pergunta | Resposta |
|----------|----------|
| Onde / como fica a autenticação? | CAS (auth-proxy do hub A-M-App-Hub) — autenticação SSO interna A&M |
| Exposição da aplicação / APIs | Restrito (rede interna A&M) — acesso via hub, sem exposição pública |
| Método de autenticação do usuário | SSO via CAS (Central Authentication Service) — credenciais corporativas A&M |

### Perfis (enxuto)

<!-- PREMISSA: MVP com perfil único; RBAC futuro se necessário -->

| Perfil | Descrição (o que pode fazer) |
|--------|------------------------------|
| **Consultor A&M** | Acesso completo: visualizar métricas, cadastrar imóveis, consultar tabela de imóveis |

### Compliance / dados sensíveis (resumo)

| LGPD, PII, retenção ou restrições relevantes (1–2 frases) |
|-----------------------------------------------------------|
| Dados de proprietários e inquilinos podem conter PII (nomes, endereços). MVP usa dados mockados; implementação futura com persistência real deve seguir políticas de retenção e anonimização conforme LGPD. |

---

## 8. Requisitos Funcionais

### 8.1 Fontes de Dados (Input)

| Fonte | Tipo (manual/API/upload/ETL) | Formato | Detalhes |
|-------|------------------------------|---------|----------|
| Formulário de cadastro de imóvel | Manual (UI) | JSON (POST API) | Usuário preenche formulário; frontend envia POST para `/api/imoveis` |
| Dados mockados (MVP) | Hardcoded no backend | Python dict/list | Backend FastAPI retorna dados mockados para métricas, gráfico e tabela |

### 8.2 Telas e Visualizações Principais

| Tela/Página | Descrição | Dados exibidos | Ações disponíveis |
|-------------|-----------|----------------|------------------|
| **Dashboard Principal** | Página única com todas as funcionalidades | Cards de métricas (receita, ocupação, inadimplência), gráfico de novos contratos, tabela de imóveis, formulário de cadastro | Visualizar métricas, cadastrar imóvel, navegar na tabela (paginação) |

**Detalhamento da tela Dashboard Principal:**

1. **Header/Topbar:**
   - Logo A&M
   - Título: "Dashboard de Gestão Imobiliária"
   - Informações do usuário logado (nome, avatar)
   - Botão de logout

2. **Cards de Métricas (topo):**
   - **Card 1:** Receita de Aluguéis (R$)
     - Valor principal: R$ XXX.XXX,XX
     - Ícone: cifrão ou dinheiro
     - Cor: verde (positivo)
   - **Card 2:** Taxa de Ocupação (%)
     - Valor principal: XX%
     - Ícone: casa ou chave
     - Cor: azul (neutro)
   - **Card 3:** Inadimplência (%)
     - Valor principal: XX%
     - Ícone: alerta ou exclamação
     - Cor: vermelho (atenção)

3. **Gráfico de Novos Contratos:**
   - Título: "Novos Contratos por Mês"
   - Tipo: Gráfico de barras verticais
   - Eixo X: Meses (últimos 12 meses, ex: Jan/26, Fev/26, ...)
   - Eixo Y: Quantidade de contratos
   - Interatividade: Tooltip ao passar o mouse (mês + quantidade)

4. **Tabela de Imóveis:**
   - Título: "Imóveis Cadastrados"
   - Colunas:
     - Endereço/Código (texto)
     - Tipo (badge: Residencial/Comercial/Terreno)
     - Status (badge colorido: Alugado [verde], Disponível [azul], Em Manutenção [amarelo])
     - Valor Aluguel/Condomínio (R$)
   - Ordenação: Data de cadastro (mais recentes primeiro)
   - Paginação: 10 itens por página
   - Estado vazio: "Nenhum imóvel cadastrado. Cadastre o primeiro imóvel usando o formulário abaixo."

5. **Formulário de Cadastro de Imóvel:**
   - Título: "Cadastrar Novo Imóvel"
   - Campos:
     - **Proprietário** (text input, obrigatório)
     - **Endereço** (text input, obrigatório)
     - **Tipo** (dropdown: Residencial, Comercial, Terreno, obrigatório)
     - **Status Inicial** (dropdown: Disponível, Em Manutenção, obrigatório)
     - **Valor Sugerido de Aluguel** (number input, R$, obrigatório)
   - Botão: "Cadastrar" (primary button)
   - Validação: Exibir mensagens de erro abaixo de cada campo se obrigatório vazio
   - Feedback: Toast verde "Imóvel cadastrado com sucesso!" ou toast vermelho "Erro ao cadastrar imóvel."

### 8.3 APIs de Saída (alto nível)

<!-- Endpoints REST do backend FastAPI -->

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/api/metricas` | GET | Retorna cards de métricas: receita de aluguéis (R$), taxa de ocupação (%), inadimplência (%) |
| `/api/contratos/novos-por-mes` | GET | Retorna dados para gráfico de barras: quantidade de novos contratos por mês (últimos 12 meses) |
| `/api/imoveis` | GET | Retorna lista de imóveis cadastrados (paginação via query params `page` e `limit`) |
| `/api/imoveis` | POST | Cadastra novo imóvel (body JSON: proprietario, endereco, tipo, status, valor_aluguel) |
| `/health` | GET | Health check do backend |

**Exemplo de resposta `/api/metricas`:**
```json
{
  "receita_alugueis": 125000.00,
  "taxa_ocupacao": 85.5,
  "inadimplencia": 3.2
}
```

**Exemplo de resposta `/api/contratos/novos-por-mes`:**
```json
{
  "meses": ["Jan/26", "Fev/26", "Mar/26", ...],
  "quantidades": [5, 8, 12, ...]
}
```

**Exemplo de resposta `/api/imoveis` (GET):**
```json
{
  "total": 50,
  "page": 1,
  "limit": 10,
  "imoveis": [
    {
      "id": "uuid-1",
      "proprietario": "João Silva",
      "endereco": "Rua A, 123 - São Paulo/SP",
      "tipo": "Residencial",
      "status": "Alugado",
      "valor_aluguel": 2500.00,
      "data_cadastro": "2026-07-10T10:30:00Z"
    },
    ...
  ]
}
```

**Exemplo de body `/api/imoveis` (POST):**
```json
{
  "proprietario": "Maria Oliveira",
  "endereco": "Av. B, 456 - Rio de Janeiro/RJ",
  "tipo": "Comercial",
  "status": "Disponível",
  "valor_aluguel": 5000.00
}
```

### 8.4 Exportações e Relatórios

<!-- Fora do escopo MVP -->

| Tipo | Formato (PDF/Excel/CSV/tela) | Periodicidade | Destinatário |
|------|------------------------------|---------------|-------------|
| Relatório de imóveis | Excel/CSV | Sob demanda (futuro) | Consultor A&M |
| Relatório de inadimplência | PDF | Mensal (futuro) | Gestor/Líder |

### 8.5 Notificações

<!-- Fora do escopo MVP -->

| Evento | Canal (email/push/in-app) | Destinatário | Frequência |
|--------|--------------------------|-------------|-----------|
| Inadimplência detectada | E-mail (futuro) | Consultor responsável | Imediata |
| Vencimento de contrato | E-mail (futuro) | Consultor responsável | 30 dias antes |

### 8.6 Latência

| Operação crítica | Tipo (síncrono/assíncrono) | Meta de tempo | Prioridade |
|-----------------|--------------------------|--------------|-----------|
| Carregamento do dashboard (métricas + gráfico + tabela) | Síncrono | < 2s | P0 |
| Cadastro de imóvel (POST) | Síncrono | < 1s | P0 |

---

## 9. Design System e UI/UX

### 9.1 Conformidade com Design System

| Campo | Valor |
|-------|-------|
| **Conformidade com Design System** | **OBRIGATÓRIO** — seguir `boas_praticas_e_conhecimentos/biblioteca_de_agent_skills/esteira_de_desenvolvimento/references/design-system.md` |
| Desvios justificados | Nenhum desvio planejado |
| Protótipo visual (link) | A definir |
| Status do protótipo | A definir (Wireframe/Completo) |

### 9.2 Componentes Necessários

<!-- INFERIDO: componentes típicos de dashboard -->

- [x] Botões (Primary, Secondary, Ghost, Danger)
- [x] Inputs e Campos de Formulário
- [x] Cards (Padrão, Métrica/KPI)
- [x] Tabelas (com filtros/busca/ordenação)
- [ ] Menu Lateral (Sidebar) e Header (Topbar) — Header/Topbar apenas
- [ ] Modais e Dialogs
- [x] Notificações (Toast/Snackbar)
- [x] Badges e Tags
- [x] Skeleton Loaders e estados vazios/erro
- [x] Formulários (single-column, two-column, multi-step) — single-column
- [x] Paginação
- [x] Outros: Gráficos (Recharts ou Chart.js)

### 9.3 Responsividade

| Requisito | Valor |
|-----------|-------|
| Suporte mobile | Não (MVP) |
| Suporte tablet | Sim (funcional) |
| Suporte desktop | Sim (prioridade) |
| Prioridade de otimização | Desktop-first |

---

## 10. Riscos e Dependências

### 10.1 Riscos Principais

<!-- PREMISSA: riscos típicos AS1I mock -->

| Risco | Impacto (Alto/Médio/Baixo) | Probabilidade | Mitigação | Responsável |
|-------|---------------------------|---------------|-----------|-------------|
| **Qualidade dos dados mockados** | Médio | Alta | Validar regras de negócio com PO; usar dados realistas no mock | Equipe Dev |
| **Migração futura para persistência real** | Alto | Média | Documentar modelo de dados; planejar migração para AS3I com Firestore/Cloud SQL | Tech Lead |
| **Definição de regras de negócio incompleta** | Alto | Média | Validar RNs críticas (cálculo de métricas) com PO antes do desenvolvimento | PO + Dev |
| **Adoção baixa por usuários** | Médio | Baixa | Envolver consultores A&M no feedback do MVP; comunicar valor e facilitar onboarding | Product Owner |
| **Performance com volume de dados crescente** | Baixo | Baixa | MVP usa mock com volume controlado; monitorar latência e planejar otimizações futuras | Tech Lead |

### 10.2 Dependências

| Dependência | Tipo (interna/externa) | Prazo esperado | Impacto no cronograma |
|-------------|------------------------|----------------|----------------------|
| Acesso ao hub A-M-App-Hub (CAS) | Interna | Imediato | Crítico — bloqueia autenticação |
| Definição de PO para validação de regras de negócio | Interna | Semana 1 | Alto — impacta validação de RNs |
| Feedback de consultores A&M (usuários-alvo) | Interna | Semana 2-3 | Médio — impacta ajustes de UX |

---

## 11. Aprovação

| Área | Responsável | Status | Data |
|------|------------|--------|------|
| Produto/PO | A definir | ( ) Aprovado ( ) Pendente | |
| UX/UI | A definir | ( ) Aprovado ( ) Pendente | |
| Tech Lead | A definir | ( ) Aprovado ( ) Pendente | |
| Negócio/Stakeholder | A definir | ( ) Aprovado ( ) Pendente | |

**Resultado final:** ( ) Aprovado para desenvolvimento ( ) Aprovado com ressalvas ( ) Reprovado

**Condições para seguir (se houver):**

**Data da decisão:**
