---
source_roadmap: roadmap_equilibrado.md
phase_index: 1
phase_title: "Provisionamento de Infraestrutura e Setup Inicial"
epic_title: "Dashboard de Gestão Imobiliária (Real Estate Control)"
generated_at: "2026-07-16T14:30:00"
---

# Story: Provisionamento de Infraestrutura e Setup Inicial

## Context

Provisionar infraestrutura GCP via Terraform (arquétipo AS1I), configurar hub A-M-App-Hub, validar autenticação CAS e preparar ambiente de desenvolvimento local. Esta fase é crítica pois desbloqueia todo o desenvolvimento subsequente (backend e frontend).

**Objetivo**: Criar a fundação técnica do projeto, incluindo infraestrutura cloud, autenticação SSO e estrutura de repositório.

**Limites de entrega**: Infraestrutura provisionada e validada, repositório configurado, spike de autenticação CAS concluído.

## Tasks

- [ ] Provisionar infraestrutura GCP via Terraform (arquétipo AS1I)
  - [ ] Executar terraform apply para ambiente dev
  - [ ] Validar recursos criados (Cloud Run, IAM, networking)
- [ ] Configurar hub A-M-App-Hub com acesso CAS
  - [ ] Registrar aplicação no hub
  - [ ] Configurar auth-proxy para CAS
  - [ ] Obter credenciais de acesso
- [ ] Executar spike de autenticação CAS
  - [ ] Implementar fluxo de login básico
  - [ ] Validar redirecionamento e callback
  - [ ] Testar obtenção de informações do usuário
- [ ] Configurar repositório GitHub com CI/CD básico
  - [ ] Criar workflows GitHub Actions (build, test, deploy)
  - [ ] Configurar secrets (GCP credentials, tokens)
  - [ ] Validar pipeline em ambiente dev
- [ ] Criar estrutura de pastas do projeto
  - [ ] Criar diretórios: backend/, frontend/, docs/, tests/
  - [ ] Adicionar README.md com instruções de setup
  - [ ] Configurar .gitignore e arquivos de configuração base

## Acceptance Criteria

- AC-1.1: Infraestrutura GCP provisionada via Terraform (ambiente dev) — recursos Cloud Run, IAM e networking criados e validados
- AC-1.2: Hub A-M-App-Hub configurado com acesso CAS — aplicação registrada, auth-proxy configurado
- AC-1.3: Spike de autenticação CAS concluído com sucesso (validação de login) — fluxo de login funciona, informações do usuário são obtidas
- AC-1.4: Repositório GitHub configurado com CI/CD básico (GitHub Actions) — workflows de build e deploy funcionando
- AC-1.5: Estrutura de pastas do projeto criada (backend, frontend, docs) — diretórios criados, README atualizado

## Worktree Config

- **story-slug**: provisionamento-infraestrutura-setup-inicial
- **branch-name**: story/provisionamento-infraestrutura-setup-inicial
- **base-branch**: main

## Test Strategy

- **unit-test-runner**: pytest -xvs --tb=long
- **e2e-required**: nao
- **coverage-threshold**: 80
- **test-paths**: tests/

## PR Config

- **draft**: true
- **base**: main
- **labels**: ["story/provisionamento-infraestrutura-setup-inicial", "infra", "setup"]

## Autonomy Blockers

- **Acesso ao hub A-M-App-Hub**: Verificar se credenciais GCP e acesso ao hub estão disponíveis antes de executar. Se não estiver disponível, solicitar acesso à equipe de infraestrutura A&M.
- **Validação de autenticação CAS**: Spike pode revelar problemas de configuração que exigem suporte da equipe de infraestrutura. Documentar quaisquer blockers encontrados.

## Technical Notes

- **Dependências**: Nenhuma (fase inicial)
- **Pontos de integração**: 
  - GCP (Cloud Run, IAM, networking)
  - Hub A-M-App-Hub (CAS auth-proxy)
  - GitHub Actions (CI/CD)
- **Riscos**: 
  - Integração CAS pode falhar — mitigado por spike antecipado
  - Credenciais GCP podem estar indisponíveis — validar acesso antes de começar
- **Referencias**: 
  - Blueprint: `docs/planning/blueprints/blueprint-AS1I-rendered.md`
  - PRD: `docs/planning/real-estate-control-prd.md`
  - Arquétipo AS1I: Topologia Minimal (FastAPI_Mixed) + INTERNAL_CAS
