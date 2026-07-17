---
name: bootstrap-deploy
description: "Skill descartável: primeiro ciclo bootstrap IaC + primeiro deploy dev, documentação mínima pós-sucesso (ARCHITECTURE.md), depois remove skills/bootstrap-deploy/SKILL.md em commit próprio."
license: Proprietary
metadata:
  persona: Forge
  repo_name: "real-estate-control"
  service_name: "realestatecontrol"
  topology: "FastAPI_Mixed + INTERNAL_CAS"
  project_display_name: "real estate control"
  topology_pattern: "FastAPI_Mixed"
  access_topology: "INTERNAL_CAS"
  sso_provider: "CAS"
  assets_library_pinned_sha: "local-dab472b513e1"
---

# Bootstrap Deploy — `real estate control`

Skill **descartável** gerada pela esteira (`pipeline-forge`). Cobre **somente**:

- Documentação pré-flight (Reading Gate)
- Bootstrap IaC (Fase 1)
- Primeiro deploy **dev** (Fase 2)
- Debug loop durante este primeiro ciclo (Fase 2.5)

Após deploy dev bem-sucedido: gera `docs/planning/ARCHITECTURE.md`, atualiza ADR/`REFERENCE_DEPLOYS`, e **remove este arquivo** com commit próprio (`rm skills/bootstrap-deploy/SKILL.md`). Operações seguintes → `skills/debug-deploy/SKILL.md`.

**Fontes permitidas:**
- `assets-library/` da esteira (pinned SHA: `local-dab472b513e1`) — **lições obrigatórias antes de agir**
- `base_tf_generator` HTTP API (`/api/regions`, `/api/validate`, `/api/generate`)
- Repositório espelho apenas se o **usuário** informar `A-M-App-Hub/real-estate-control` (read-only via `gh api`), registrado no ADR

---

## Recovery após compactação de contexto

1. Ler `docs/planning/ADR.md` → **Estado Atual**
2. Ler `docs/planning/DEBUG_LOG.md` → últimas entradas
3. Re-ler este arquivo
4. **Antes de agir:** Fase 0 Reading Gate abaixo
5. Prosseguir pela **Próxima ação** no ADR

---

## Protocolo BEFORE ACTING (todas as fases)

**SEMPRE nesta ordem:**

1. **`assets-library/docs/prohibited-actions.md`**
2. **`assets-library/docs/lessons-learned/INDEX.md`**
3. `gh auth status` e, se necessário, seguir `references/gh-cli-prerequisite.md`
4. **`base_tf_generator` API** se bootstrap ou validação forem necessários
5. Pergunta ao usuário: *Deploy bem-sucedido similar? `A-M-App-Hub/real-estate-control` ou `skip`.*
   - Se repo: ler read-only via `gh api` apenas `iac_scripts/` + `.github/config/`; anotar no ADR só `<org>/<repo>` (**nunca** persistir nome de repo espelho em asset versionado pela skill)

---

## Protocolo Copy + Substitute

```bash
cp <assets-library>/<categoria>/<arquivo> <destino>
sed -i "s|<placeholder>|<valor>|g" <destino>
grep -n '<[A-Z_]\+>' <destino> && echo "FAIL: placeholder remanescente" && exit 1
```

---

## Fase 0 — Documentation-First Reading Gate

**Quando:** Antes da **Fase 1** (bootstrap) OU antes da **Fase 2** (primeiro deploy) OU quando o usuário reportar falha.

**Gate IN (para Fase 2):** `iac_scripts/<env>.tfvars` existe e sem placeholders críticos (`project_id`, `region`, `api_domain`) conforme combinado na Fase 1.

### Determinar docs (via `metadata`)

```
topology_pattern = FastAPI_Mixed
access_topology = INTERNAL_CAS
sso_provider = CAS

Docs SEMPRE:
  prohibited-actions.md, symptom-fix-catalog.md, lessons-learned/INDEX.md

Por padrão (arquivos em assets-library/docs/lessons-learned/):
  Pattern_A → 01, 02, 03, 05, 06, 07, 08, 09, 11
  Pattern_B → 01, 02, 03, 05, 06, 07, 08, 09, 10, 11
  Minimal → 01, 02, 03, 05, 08, 09, 11
  CAS → aprofundar 04-auth-proxy-and-cas.md
```

Registrar no ADR (**Estado Atual**) checklist de docs lidas e **Próxima ação** (Bootstrap / Primeiro Deploy).

**Gate OUT:** ADR atualizado.

---
## Gate 0A — Pre-commit Hook (Pré-Bootstrap)

**Antes do primeiro deploy**, verificar que pre-commit hooks estão instalados no repo (Gate A local):

```bash
# Verificar se .pre-commit-config.yaml existe
if [ ! -f ".pre-commit-config.yaml" ]; then
  echo "AVISO: .pre-commit-config.yaml ausente — Gate A (secrets) não protegido localmente"
  echo "Ação: copiar scaffold e instalar"
fi

# Instalar hooks se não instalados
uv tool install pre-commit 2>/dev/null || pip install pre-commit
pre-commit install
echo "pre-commit hook com gitleaks instalado — secrets bloqueados localmente antes do commit"
```

> Gate A (secrets) é **local por repo** — não há workflow de PR para isso. O dev-agent Passo 2.3 é a rede de segurança adicional. Ver `references/security-gate-contract.md`.

---
## Gate 0B — APIs GCP Mínimas (Pré-Bootstrap)

**Antes do primeiro `tofu apply`**, verificar que as APIs críticas estão habilitadas:

```bash
PROJECT_ID="<PROJECT_ID_DEV>"  # substituir pelo project_id do ambiente dev

REQUIRED_APIS=(
  "cloudresourcemanager.googleapis.com"
  "iam.googleapis.com"
  "iamcredentials.googleapis.com"
  "run.googleapis.com"
  "artifactregistry.googleapis.com"
  "secretmanager.googleapis.com"
)

MISSING=()
for api in "${REQUIRED_APIS[@]}"; do
  STATE=$(gcloud services list --enabled --project="$PROJECT_ID" \
    --filter="name:$api" --format="value(state)" 2>/dev/null)
  if [ "$STATE" != "ENABLED" ]; then
    MISSING+=("$api")
  fi
done

if [ ${#MISSING[@]} -gt 0 ]; then
  echo "BLOQUEADO: APIs ausentes em $PROJECT_ID:"
  for api in "${MISSING[@]}"; do echo "  - $api"; done
  echo ""
  echo "  Habilitar:"
  echo "  gcloud services enable ${MISSING[*]} --project=$PROJECT_ID"
  echo ""
  echo "  Referência: references/gcp-api-prerequisites.md"
  exit 1
fi

echo "Gate 0B: APIs mínimas habilitadas em $PROJECT_ID"
```

> Ver lista completa com justificativas em `references/gcp-api-prerequisites.md`.
> O `base_tf_generator` inclui `google_project_service` para essas APIs, mas elas devem existir antes do primeiro plan/apply.

---
## Gate 1 — Security Report Obrigatório (Pré-Deploy)

Antes de `POST /api/generate`:

```bash
# 1. Ler SECURITY_REPORT.md (gerado por skills/security-pipeline/SKILL.md Fase 3)
SECURITY_REPORT_PATH="docs/planning/SECURITY_REPORT.md"

if [ ! -f "$SECURITY_REPORT_PATH" ]; then
  echo "BLOQUEADO: SECURITY_REPORT.md não encontrado"
  echo "  Ação: invocar skills/security-pipeline/SKILL.md Fase 3 para gerar o relatório"
  exit 1
fi

SECVAL_ID=$(grep "Security Validation ID" "$SECURITY_REPORT_PATH" | grep -o 'SECVAL-[^`]*' | head -1)
REPORT_SHA=$(grep "Commit SHA" "$SECURITY_REPORT_PATH" | grep -o '\`[^`]*\`' | head -1 | tr -d '`' | cut -c1-7)
HEAD_SHA=$(git rev-parse HEAD | cut -c1-7)
GATE_PROD=$(grep "Gate prod" "$SECURITY_REPORT_PATH" | grep -v "^#" | head -1 | grep -o 'LIBERADO\|BLOQUEADO' | head -1)

# 2. Validar presença do SECVAL
if [ -z "$SECVAL_ID" ]; then
  echo "BLOQUEADO: SECVAL ID não encontrado em SECURITY_REPORT.md"
  echo "  Ação: invocar skills/security-pipeline/SKILL.md Fase 3"
  exit 1
fi

# 3. Validar SHA match
if [ "$REPORT_SHA" != "$HEAD_SHA" ]; then
  echo "BLOQUEADO: SECURITY_REPORT.md é de commit diferente (stale)"
  echo "  Report SHA: $REPORT_SHA"
  echo "  HEAD SHA:   $HEAD_SHA"
  echo "  Ação: re-executar skills/security-pipeline/SKILL.md Fase 3"
  exit 1
fi

# 4. Verificar gate prod
if [ "$GATE_PROD" != "LIBERADO" ]; then
  echo "BLOQUEADO: SECURITY_REPORT.md indica '$GATE_PROD' — achados CRITICAL não resolvidos"
  echo "  Ver: $SECURITY_REPORT_PATH"
  exit 1
fi

echo "Gate 1: SECURITY_REPORT.md validado — SECVAL $SECVAL_ID — Gate prod: LIBERADO"
```

---



## Fase 1 — Bootstrap Discovery

**Gate IN:** Validation Report `Can Deploy=YES` + SECVAL id disponível (emitido por `skills/security-pipeline/SKILL.md` Fase 3).

**Ler antes:** `assets-library/infra_request/`, `assets-library/tfvars/`, `assets-library/containers/`, `assets-library/docs/deploy-preflight-template.md`, **`references/charge-code-policy.md`**.

**Ações:**
1. **CHARGE CODE VALIDATION GATE:** Antes de qualquer ação, validar o charge code em `infra_request.json`.
   - Normalizar: `charge_code.strip().upper()`
   - Validar regex: `^P\d{6}[A-Z]{2}\d{2}\.\d+\.\d+$`
   - Se regex falhar → **STOP aqui**. Exibir mensagem:
     ```
     Charge code inválido em infra_request.json: {charge_code}
     Formato esperado: P######LL##.#.# (ex: P250632ES01.1.2)
     
     Referência: references/charge-code-policy.md
     Ação: Confirmar o charge code correto com o usuário e atualizar infra_request.json
     ```
   - Se regex passar → prosseguir. Documentar charge code confirmado no ADR.

2. `GET /api/regions` → validar região
3. `POST /api/validate` com `infra_request.json`
4. Pergunta repo espelho (path ou skip)
5. Copy + Substitute:
   - `infra_request.json` → `iac_scripts/`
   - `tfvars/*.tfvars` → `iac_scripts/`
   - `containers/*.json` → `.github/config/{dev,qa,prod}/`
   - `deploy-preflight-template.md` → `docs/planning/DEPLOY_PREFLIGHT.md`
6. Gerar IaC: **`bash "$CONDUTORA_ROOT/scripts/render-iac.sh"`** (template `assets-library/iac_template/`)
   - Fallback opcional: `POST /api/generate` ou `POST /api/scripts/zip` via base_tf_generator API (topologias não-padrão: gradio, mcp, Pattern_B)
7. Workflows: `workflows-cd/initial_trigger_*.yml`, `workflows-ci/final_ci_*.yml` → `.github/workflows/`

**Checks:** região alinhada; `api_domain` distinto entre ambientes; `service_name`; **charge code validado**; FinOps parity; topology coerente com `boas_praticas_e_conhecimentos/biblioteca_de_agent_skills/esteira_de_desenvolvimento/references/webapp-topologies.md`; acesso coerente com `boas_praticas_e_conhecimentos/biblioteca_de_agent_skills/esteira_de_desenvolvimento/references/access-topologies.md`.

**ADR HARD GATE:** todo commit inclui `docs/planning/ADR.md` atualizado com charge code confirmado.

**Gate OUT:** PR bootstrap ou merge conforme política do time; ADR informa bootstrap gerado/aguardando merge.

---

## Fase 2 — Primeiro Deploy Dev

**Gate IN:** PR IaC bootstrap **mergeado** em `main` (ou branch de deploy autorizada).

**BEFORE ACTING:** `assets-library/workflows-cd/`, `assets-library/gates/gate0-iam-checklist.md`, releitura rápida de `01-iam-and-org-policies.md` se necessário.

**Ações:**
1. `grep -rn '<[A-Z_]\+>' iac_scripts/ .github/`
2. Dispatch `CI (dev)` (workflow copiado de `final_ci_dev.yml` como `ci-dev.yml` quando aplicável):

```bash
gh workflow run "CI (dev)" -f ref='<branch_or_sha>' -f force_apply=<true|false>
```

   `force_apply=true` apenas quando lessons em `09-workflows-and-dispatch.md`/`DEBUG_LOG` indicarem fluxo válido para drift não refletido em `.tf/.tfvars`.

3. Monitorar até conclusão; smoke estruturado em `docs/planning/SMOKE_REPORTS/<run-id>.md` (LB → URL map → API GW → Cloud Run → IAM → HTTPS público quando aplicável à topologia)

   **Cross-check app trigger + iac-actions:**

   ```bash
   # Perspectiva 1: App repo (ci-dev trigger)
   APP_RUN_ID=$(gh run list --workflow "CI (dev)" --limit 1 --json databaseId --jq '.[0].databaseId')
   gh run view "$APP_RUN_ID" --json conclusion,jobs --jq '{conclusion, jobs: [.jobs[] | {name, conclusion}]}'

   # Perspectiva 2: iac-actions (run_url disponível no Step Summary do trigger)
   # O job cross-check do ci-dev.yml reporta iac_conclusion + security_passed no Summary
   # A partir de v2.0, cross-check BLOQUEIA (exit 1) se iac_conclusion=failure ou security_passed=false
   gh run view "$APP_RUN_ID" --log | grep -A 5 "Cross-check"

   # Classificar achados:
   # iac_conclusion=failure + security_passed=false → deps CVE não allowlistado ou IaC misconfig → investigar
   # iac_conclusion=failure + security_passed=true  → problema de infra (tofu), não de segurança
   # iac_conclusion=success + security_passed=true  → clean deploy
   # CVE allowlistada: ver .security-allowlist.json na raiz do app repo
   ```

4. Anexar run URL ao ADR; atualizar `REFERENCE_DEPLOYS.md` (**append-only**, template em `reference-deploys-template.md`)

**Gate OUT em sucesso:** seguir **Pós-sucesso — ARCHITECTURE + auto-remoção**.  
**Gate OUT em falha:** `DEBUG_LOG`; entrar na **Fase 2.5**.

---

## Fase 2.5 — Debug Loop (bootstrap apenas)

Leitura obrigatória: `assets-library/docs/debug-loop-protocol.md` (4 tiers).

**Resumo:**
- Tier 1: sintoma → `INDEX.md` → lesson aplicável  
- Tier 2: docs canônicas cruzadas  
- Tier 3: commit mínimo referenciando `lessons-learned/<topic>.md` na mensagem  
- Tier 4: STOP / escalação humana

**Contrato:** sem improviso fora de docs canônicas; sem `terraform_data`, `gcloud run deploy` manual ad-hoc, “commit fantasma”; `MAX_ITERATIONS=3`; depois Tier 4.

Ao resolver: voltar para **Fase 2**.

---

## Pós-sucesso — ARCHITECTURE.md + auto-remoção

1. Gerar/atualizar `docs/planning/ARCHITECTURE.md` (**único** doc além do ADR para orientar futuros debugs arquiteturais):

   Seções obrigatórias:
   - Topologia efetiva + `topology_pattern` + `access_topology` + `sso_provider`
   - `api_domain`, `project_id`(s), regiões
   - Recursos GCP **nomeados** (Cloud Run, LB, URL map, API Gateway, proxies, IAM críticos) conforme último smoke bem-sucedido
   - URL do primeiro workflow run bem-sucedido
   - Link/ponteiro para `REFERENCE_DEPLOYS.md`
   - **“Como debugar”**: invocar `skills/debug-deploy/SKILL.md`; manter pinning `assets_library_pinned_sha`

2. Atualizar `docs/planning/ADR.md`: marcar primeira subida dev concluída; próximas ações com `debug-deploy`; nota que `bootstrap-deploy` será removida.

3. **Auto-destruição (commit único):**

```bash
rm skills/bootstrap-deploy/SKILL.md
git add docs/planning/ARCHITECTURE.md docs/planning/ADR.md docs/planning/REFERENCE_DEPLOYS.md docs/planning/SMOKE_REPORTS/ skills/bootstrap-deploy/SKILL.md
git commit -m "docs: add ARCHITECTURE.md and remove disposable bootstrap-deploy skill

- First dev deploy completed; use skills/debug-deploy for ongoing operations"
```

4. Sem push automático se política exigir revisão — seguir fluxo do time.

---

## Pós-deploy — Checklist FinOps (condicional — somente se blueprint tem seção 13)

> Executar **somente se** o blueprint tem a seção 13 (FinOps e Rateio de Custos).  
> Referência: `assets-library/finops/FINOPS_SCAFFOLD.md` e `references/finops-implementation.md`.

### 1. Verificar que `finops.tf` foi provisionado com sucesso

```bash
# Verificar recursos criados no tofu apply
grep "google_bigquery_table\|google_bigquery_data_transfer\|google_bigquery_dataset_iam\|google_project_iam_member.worker_bq_job_user" docs/planning/SMOKE_REPORTS/*.md | head -20
```

### 2. Confirmar IAM cross-project via IaC

O recurso `google_project_iam_member.worker_finops_cross_project_viewer` em `finops.tf` gerencia automaticamente o binding `roles/bigquery.dataViewer` da worker SA no projeto `amlatamdigital-finops`. Verificar no smoke report que o recurso foi aplicado:

```bash
grep "worker_finops_cross_project_viewer\|bigquery.dataViewer.*amlatamdigital-finops" docs/planning/SMOKE_REPORTS/*.md | head -5
```

Se ausente no smoke, verificar se o tofu apply incluiu `finops.tf` e se a SA do pipeline possui permissão `resourcemanager.projects.setIamPolicy` no projeto `amlatamdigital-finops` (permissão padrão das SAs de infraestrutura do time).

### 3. Registrar no ADR

```markdown
## FinOps
- finops.tf provisionado: costs_history, tb_daily_cost_allocations, Scheduled Query
- IAM cross-project: worker_finops_cross_project_viewer aplicado via IaC
- Após primeiro ciclo d-2: rodar validate_finops.py para validar guardrails
```

### 4. Validação pós-d-2 (aguardar 2 dias após dados reais)

```bash
# Após pelo menos 1 dia de uso + 2 dias de lag de billing:
uv run <path_esteira>/assets-library/finops/scripts/validate_finops.py \
  --project <PROJECT_ID_DEV>
```

---

## Pós-deploy — Checklist PostHog (condicional — somente se blueprint tem seção 14)

> Executar **somente se** o blueprint tem a seção 14 (Observabilidade de Produto) **E** há frontend.  
> Backend-only apps: SKIP — PostHog não funciona sem navegador.
> Referência: `assets-library/posthog/POSTHOG_SCAFFOLD.md` e `references/posthog-implementation.md`.

### 1. Verificar que GitHub secret foi cadastrado

```bash
gh secret list | grep VITE_POSTHOG_API_KEY
# Deve retornar: VITE_POSTHOG_API_KEY
```

Se ausente → STOP. Usuario precisa adicionar em GitHub → Settings → Secrets.

### 2. Smoke test no ambiente dev

```bash
# Deploy foi sucesso em dev?
gcloud run services list --project am-<code>-<project>-d --filter="name=<service>" --format="value(status)"

# Abrir app em browser real (não localhost)
# Login com usuário real
# Fazer fluxo principal (entry → conversion)
# DevTools Console → `window.posthog` deve existir
# DevTools → `posthog._isIdentified()` deve ser true
```

### 3. Verificar eventos no PostHog Live Events

```bash
# Esperados em ~30s:
# - Eventos frontend com app_name = <app_name_do_blueprint>
# - Eventos backend (se houver) com mesma `app_name` super property
# - distinct_id deve ser oid_azure (não UUID)
```

Se nada chegar → Ler `references/posthog-lessons-learned.md` (#1–#8) para debug. Mais comum:
- Build args missing (Lição 1)
- Mock auth sem identify (Lição 2)
- Backend package missing (Lição 3)
- Backend eager init (Lição 4)

### 4. Registrar no ADR

```markdown
## PostHog
- App name: {app_name} (seção 14 blueprint)
- Frontend framework: {framework}
- Build args: VITE_POSTHOG_* or NEXT_PUBLIC_POSTHOG_* wired (Dockerfile + cloudbuild + secret)
- Smoke test: eventos chegando em PostHog Live Events (dev) — distinct_id = oid_azure ✓
- Mock auth: identify() verificado ✓
- Backend lazy-init: verificado ✓
- Próximos: MCP setup (dashboard + survey) em QA/prod
```

---



Todo commit desta skill até a auto-remoção **deve** incluir `docs/planning/ADR.md`.

---

## Pinning

Revalidar `assets_library_pinned_sha` (>30 dias) via `skills/sync-esteira/SKILL.md` antes de novo bootstrap paralelo não recomendado; preferir sempre `sync-esteira` primeiro se o pin estiver velho.
