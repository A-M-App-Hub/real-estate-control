# ADR — real-estate-control

**Data de criação:** 2026-07-16  
**Skill orquestradora:** esteira-condutora

---

## Estado Atual

**Lifecycle:** construcao
**Arquétipo:** AS1I
**Playbook:** AS1I-construcao.yaml
**Step atual:** dev
**Fase:** 4
**Modo:** AUTOMATION  
**GitHub actor:** am-esteira-helpe[bot]  
**Org:** A-M-App-Hub  
**Repositório:** A-M-App-Hub/real-estate-control  
**Status solução:** ACTIVE  
**Próxima ação:** Executar Fase 1 (Provisionamento de Infraestrutura) ou sincronizar com Jira  
**Última atualização:** 2026-07-17 00:06 UTC

---

## Premissas e Mapeamento Inicial

- **Repositório**: `A-M-App-Hub/real-estate-control`
- **Topologia alvo**: Minimal (FastAPI_Mixed) + INTERNAL_CAS
- **SSO**: CAS
- **Persistência**: none (dados mockados em memória)
- **Stack frontend**: React + TypeScript + Vite
- **Stack backend**: FastAPI (Python 3.13+)
- **FinOps**: Desativado (v1)
- **PostHog**: Desativado (v1)

---

## Artefatos de Referência

| Artefato | Path | Preenchido por | Data |
|----------|------|----------------|------|
| Solution Brief | `docs/planning/solution-brief.yaml` | render-brief.sh | 2026-07-16 |
| PRD | `docs/planning/real-estate-control-prd.md` | doc-workshop | 2026-07-16 |
| Blueprint | `docs/planning/blueprints/blueprint-AS1I-rendered.md` | render-blueprint.sh | 2026-07-16 |
| Roadmap | `docs/planning/roadmap_equilibrado.md` | roadmap-engineer | 2026-07-16 |
| Board Jira | `docs/planning/board_jira.md` | roadmap-engineer | 2026-07-16 |
| Cards CSV | `docs/planning/cards_epico.csv` | roadmap-engineer | 2026-07-16 |
| Stories | `docs/planning/stories/*.md` | roadmap-engineer | 2026-07-16 |
| User Status | `docs/planning/user-status.md` | esteira-condutora | 2026-07-16 |

---

## Histórico de Fases

| Data | Hora | Transição | Observações |
|------|------|-----------|-------------|
| 2026-07-16 | 14:30 | Fase 3 iniciada | Roadmap Engineer invocado para gerar roadmap e stories |
| 2026-07-16 | 14:45 | Fase 3 completa | Roadmap equilibrado gerado, 5 story files criados, board Jira e CSV exportados |

---

## Notas para o Agente

- Recovery: ler **Estado Atual** + invocar `detect-entry.sh`
- Atualizar ADR após cada step via `adr.sh update`
