# real estate control — Convenções para Claude Code

## Paths de Artefatos

| Tipo | Path |
|------|------|
| Blueprints | `docs/planning/blueprints/` |
| Análises | `docs/planning/analysis/` |
| Ecosystem review | `docs/planning/ecosystem/` |
| Roadmaps | `docs/planning/roadmaps/` |
| Stories | `docs/planning/stories/` |
| Implementation context | `docs/planning/implementation-context.md` |
| ADR | `docs/planning/ADR.md` |
| Deploy fingerprints | `docs/planning/REFERENCE_DEPLOYS.md` |
| Debug log (append-only) | `docs/planning/DEBUG_LOG.md` |
| Drift report (último) | `docs/planning/DRIFT_REPORT.md` |
| Probe dumps | `docs/planning/PROBES/` |
| Smoke exports | `docs/planning/SMOKE_REPORTS/` |
| Project pipeline skill | `skills/project-pipeline/SKILL.md` |

## FinOps — Charge Code Policy

Se o blueprint tem seção 13 (FinOps):
- **Charge code é um dado de negócio cujo ÚNICA fonte de verdade é o usuário humano.**
- Nunca inventar, inferir, copiar ou adaptar charge codes
- Se não passar na regex `^P\d{6}[A-Z]{2}\d{2}\.\d+\.\d+$`: **STOP**, perguntar ao usuário
- Referência: `boas_praticas_e_conhecimentos/.../referencias/charge-code-policy.md`

## IaC / Deploy — leitura obrigatória antes de editar Terraform

1. `assets-library/docs/prohibited-actions.md` (via cópia da esteira ou path pinned no ADR) — nota: a seção "Segurança / OpenAPI" aplica-se apenas quando `SSO_PROVIDER == CAS`
2. `assets-library/docs/debug-loop-protocol.md` quando investigar falhas de deploy
3. Invocar `skills/project-pipeline/SKILL.md` — **Fase 0** antes de apply

## Stack

- Python 3.13+, FastAPI, uv
- Testes: pytest + pytest-cov (threshold: 80%)
- Linter: ruff
- Topologia: FastAPI_Mixed + INTERNAL_CAS

## Branches

- Feature/story branches: `story/{slug}` ou `feat/{slug}`
- PRs sempre para `main`
- Deploy: invocar `skills/project-pipeline/SKILL.md` após Vera liberar bootstrap
