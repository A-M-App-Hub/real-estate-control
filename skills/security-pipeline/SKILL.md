---
name: security-pipeline
description: "Skill permanente: orquestra os 2 gates de segurança pós-QA (Gates B1/B2), provisiona/verifica workflows, consolida SECURITY_REPORT.md a partir de artifacts JSON dos runs, emite e valida SECVAL id, e bloqueia promoção a prod em achados CRITICAL. Gate A (secrets) é pre-commit hook local por repo."
license: Proprietary
metadata:
  persona: Sentinela
  repo_name: "real-estate-control"
  service_name: "realestatecontrol"
  topology: "FastAPI_Mixed + INTERNAL_CAS"
  project_display_name: "real estate control"
  topology_pattern: "FastAPI_Mixed"
  sso_provider: "CAS"
  assets_library_pinned_sha: "local-dab472b513e1"
  iac_actions_pinned_sha: "local-dab472b513e1"
---

# Security Pipeline — `real estate control`

Skill **permanente** gerada pela esteira (`pipeline-forge`). Assume que bootstrap inicial está concluído e que `skills/debug-deploy/SKILL.md` opera os deploys.

**Responsabilidades exclusivas desta skill:**

1. Provisionar / verificar os 2 workflows de segurança pós-QA no repositório (de `iac-actions/templates/`)
2. Orquestrar auditoria pós-QA (Gate B1 SAST, Gate B2 cloud audit)
3. Baixar artifacts JSON dos runs e consolidar em `docs/planning/SECURITY_REPORT.md`
4. Emitir e validar `security_validation_id` (SECVAL) no SECURITY_REPORT.md
5. Bloquear promoção a prod em achados CRITICAL (drive fix stories via dev-agent)

> **Gate A (secrets)** é responsabilidade do **pre-commit hook local** (`.pre-commit-config.yaml` com gitleaks) e do **dev-agent Passo 2.3** — não é um workflow do GitHub Actions.

**Não faz** deploy IaC — apenas a camada de segurança sobre o ciclo de deploy.

**Fontes dos workflows:**
- `A-M-Digital-Data-AI-LatAm/iac-actions/templates/` pinado em `iac_actions_pinned_sha: local-dab472b513e1`
- Schema de artifacts JSON: `iac-actions/docs/SECURITY-FINDINGS-SCHEMA.md`

---

## Recovery após compactação de contexto

1. Ler `docs/planning/ADR.md` → **Estado Atual** + seção "Gates de Segurança"
2. Ler `docs/planning/DEBUG_LOG.md` → últimas entradas de segurança
3. Ler `docs/planning/SECURITY_REPORT.md` → SECVAL ID + SHA + achados CRITICAL
4. Re-ler este arquivo
5. **Antes de agir:** Fase 0 Preflight & Self-Test abaixo
6. Prosseguir pela **Próxima ação** no ADR

---

## Protocolo BEFORE ACTING (todas as fases)

**SEMPRE nesta ordem:**

1. `assets-library/docs/prohibited-actions.md`
2. `assets-library/docs/lessons-learned/INDEX.md`
3. Confirmar workflows presentes: `ls .github/workflows/security-*.yml` (se ausentes → Fase 1)

---

## Fase 0 — Preflight & Self-Test

**Quando:** Antes de qualquer outra fase OU ao iniciar nova sessão de trabalho de segurança.

**Gate IN:** Nenhum — pode ser executada a qualquer momento.

### 0.1 — Verificar Workflows

```bash
for wf in security-post-qa.yml security-cloud-audit.yml; do
  if [ ! -f ".github/workflows/$wf" ]; then
    echo "AUSENTE: .github/workflows/$wf → invocar Fase 1"
    MISSING=true
  fi
done
[ "$MISSING" = "true" ] && echo "STOP: executar Fase 1 primeiro" && exit 1
echo "Workflows presentes"
```

### 0.2 — Verificar pre-commit hook (Gate A local)

```bash
if [ ! -f ".pre-commit-config.yaml" ]; then
  echo "AVISO: .pre-commit-config.yaml ausente — Gate A (secrets) não protegido localmente"
  echo "Ação: copiar scaffold/.pre-commit-config.yaml e instalar com 'pre-commit install'"
fi
if ! git config --get core.hooksPath > /dev/null 2>&1 && [ ! -f ".git/hooks/pre-commit" ]; then
  echo "AVISO: pre-commit hook não instalado — executar 'pre-commit install' no repo"
fi
```

### 0.2b — Verificar arquivos de allowlist (CVE + OpenGrep)

```bash
# .security-allowlist.json — CVE exceptions (iac-actions v2.0+)
if [ ! -f ".security-allowlist.json" ]; then
  echo "INFO: .security-allowlist.json ausente — nenhuma exceção de CVE configurada (OK)"
  echo "Ação caso necessário: copiar scaffold/.security-allowlist.json e adicionar entradas aprovadas"
fi

# .semgrepignore — OpenGrep SAST exceptions
if [ ! -f ".semgrepignore" ]; then
  echo "INFO: .semgrepignore ausente — todos os arquivos serão escaneados pelo OpenGrep (OK)"
fi

# Validar .security-allowlist.json se existir
if [ -f ".security-allowlist.json" ]; then
  python3 -c "
import json, sys
from datetime import date
data = json.load(open('.security-allowlist.json'))
today = date.today().isoformat()
for e in data.get('cve_allowlist', []):
    exp = e.get('expires_at')
    if exp and exp < today:
        print(f'AVISO: {e[\"id\"]} expirou em {exp} — será enforced como CVE ativa')
    if len(e.get('reason','')) < 30:
        print(f'AVISO: {e[\"id\"]} — reason muito curto (mínimo 30 chars)')
print(f'Allowlist: {len(data.get(\"cve_allowlist\",[]))} entrada(s)')
"
fi
```

### 0.3 — actionlint + SHA-pin check

```bash
# Requer actionlint instalado
actionlint .github/workflows/security-post-qa.yml \
           .github/workflows/security-cloud-audit.yml

# SHA-pin: toda action de terceiros deve ter SHA 40-chars (nunca tag/branch)
grep -n 'uses:' .github/workflows/security-*.yml | grep -v '@[0-9a-f]\{40\}' | grep -v 'uses: ./' && \
  echo "FAIL: action não pinada com SHA 40-chars" && exit 1
echo "actionlint OK; todos os SHAs pinados"
```

### 0.4 — Presença de secrets/vars obrigatórios

```bash
gh secret list --repo real-estate-control | grep -q 'GCP_WORKLOAD_IDENTITY_PROVIDER' || \
  echo "AVISO: GCP_WORKLOAD_IDENTITY_PROVIDER não encontrado em secrets"
gh secret list --repo real-estate-control | grep -q 'GCP_SERVICE_ACCOUNT' || \
  echo "AVISO: GCP_SERVICE_ACCOUNT não encontrado em secrets"
gh variable list --repo real-estate-control | grep -q 'PROJECT_ID' || \
  echo "AVISO: PROJECT_ID não encontrado em vars"
```

> Se qualquer check retornar AVISO, registrar no ADR → "Pré-requisitos ausentes" e STOP.

### 0.5 — WIF Smoke Test

```bash
gh workflow run security-cloud-audit.yml --repo real-estate-control -f dry_run=true
sleep 30
RUN_ID=$(gh run list --workflow security-cloud-audit.yml --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$RUN_ID" --exit-status
echo "WIF smoke test OK"
```

> Falha aqui: documentar no `DEBUG_LOG.md` + ADR → verificar `workloadIdentityUser` binding no IAM do SA.

### 0.6 — Verificar wiring workflow_run (Gates B1/B2)

```bash
QA_WORKFLOW_NAME=$(grep -h 'workflows:' .github/workflows/security-post-qa.yml .github/workflows/security-cloud-audit.yml | head -1 | grep -o '".*"' | tr -d '"')
ACTUAL_QA_NAME=$(gh workflow list --json name --jq '.[].name' | grep -i 'qa' | head -1)

if [ "$QA_WORKFLOW_NAME" != "$ACTUAL_QA_NAME" ]; then
  echo "FAIL: workflow_run aponta para '$QA_WORKFLOW_NAME' mas o workflow QA é '$ACTUAL_QA_NAME'"
  exit 1
fi
echo "workflow_run wiring OK: '$QA_WORKFLOW_NAME'"
```

### 0.7 — Registrar resultado no ADR

```
Data: <YYYY-MM-DD>
actionlint: OK
SHA-pin: OK
Secrets/vars: OK | AVISO (<lista>)
WIF smoke: OK | FAIL (<erro>)
workflow_run wiring: OK | FAIL (<erro>)
pre-commit hook: instalado | AUSENTE
```

**Gate OUT em sucesso total:** prosseguir para a fase relevante (1, 3 ou 5).
**Gate OUT em qualquer falha:** STOP — remediar antes de qualquer operação de segurança.

---

## Fase 1 — Provisionar Workflows de Segurança

**Quando:** `0.1` detectou workflow(s) ausentes ou desatualizados (stale em relação ao pin SHA).

**Gate IN:** Fase 0.1 identificou ausências.

### 1.1 — Baixar de iac-actions/templates/

```bash
IAC_SHA="local-dab472b513e1"
DEST=".github/workflows"

# Baixar via gh api (base64 decode) — apenas Gates B1/B2 (Gate A é pre-commit hook local)
for template in \
  "templates/security/security-post-qa.yml:security-post-qa.yml" \
  "templates/security/security-cloud-audit.yml:security-cloud-audit.yml"; do

  SRC_PATH="${template%%:*}"
  DST_FILE="${template##*:}"

  gh api "repos/A-M-Digital-Data-AI-LatAm/iac-actions/contents/${SRC_PATH}?ref=${IAC_SHA}" \
    --jq '.content' | base64 -d > "${DEST}/${DST_FILE}"
  echo "Copiado: ${DST_FILE}"
done

# Verificar sem placeholders remanescentes
for wf in "$DEST"/security-*.yml; do
  grep -n '<[A-Z_]\+>' "$wf" && echo "FAIL: placeholder em $wf" && exit 1
done
echo "Workflows copiados sem placeholders"
```

### 1.2 — Confirmar wiring workflow_run

Editar `security-post-qa.yml` e `security-cloud-audit.yml` se o nome do workflow QA neste repositório divergir do padrão `CI (qa)`:

```bash
gh workflow list --json name | jq -r '.[].name'
# Se necessário, ajustar:
# sed -i "s/CI (qa)/<NOME_REAL_WORKFLOW_QA>/g" .github/workflows/security-post-qa.yml
# sed -i "s/CI (qa)/<NOME_REAL_WORKFLOW_QA>/g" .github/workflows/security-cloud-audit.yml
```

### 1.3 — Commit e push

```bash
git add .github/workflows/security-*.yml
git commit -m "ci(security): provision security gates B1/B2 from iac-actions@local-dab472b513e1"
git push origin main
```

**Gate OUT:** Fase 0 sem ausências; prosseguir para Fase 3.

---

## Fase 2 — (Removida: Gate A era required status check)

> **Gate A (secrets) não é mais um workflow do GitHub Actions.** A proteção de secrets é feita pelo pre-commit hook local (`.pre-commit-config.yaml` com gitleaks) instalado no app repo e pelo dev-agent Passo 2.3.
>
> Não há required status check de `security/gate-a`. A branch protection deve exigir apenas **PR review** (1 aprovação) e CI lint+test verde. Ver `references/security-gate-contract.md` para detalhes.

Prosseguir diretamente para **Fase 3** após QA deploy.

---

## Fase 3 — Ciclo Pós-QA: Gate B1 (SAST) + Gate B2 (Cloud Audit) + Consolidar SECURITY_REPORT.md

**Quando:** QA deploy concluído com sucesso (workflow `CI (qa)` green).

**Gate IN:** Smoke QA OK conforme `docs/planning/REFERENCE_DEPLOYS.md`.

### 3.1 — Aguardar ou acionar Gate B1 (security-post-qa.yml)

O workflow dispara automaticamente via `workflow_run` após `CI (qa)`. Se precisar acionar manualmente:

```bash
gh workflow run security-post-qa.yml --repo A-M-App-Hub/real-estate-control
RUN_ID=$(gh run list --workflow security-post-qa.yml --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$RUN_ID" --exit-status || true  # não falhar — findings coletados mesmo se RED
```

Registrar `B1_RUN_ID` e `B1_RUN_URL`:

```bash
B1_RUN_ID=$(gh run list --workflow security-post-qa.yml --limit 1 --json databaseId --jq '.[0].databaseId')
B1_RUN_URL=$(gh run view "$B1_RUN_ID" --json url --jq '.url')
B1_SHA=$(gh run view "$B1_RUN_ID" --json headSha --jq '.headSha')
```

### 3.2 — Aguardar ou acionar Gate B2 (security-cloud-audit.yml)

```bash
gh workflow run security-cloud-audit.yml --repo A-M-App-Hub/real-estate-control
B2_RUN_ID=$(gh run list --workflow security-cloud-audit.yml --limit 1 --json databaseId --jq '.[0].databaseId')
gh run watch "$B2_RUN_ID" --exit-status || true
B2_RUN_URL=$(gh run view "$B2_RUN_ID" --json url --jq '.url')
```

### 3.3 — Baixar artifacts JSON dos dois runs

```bash
mkdir -p docs/planning/PROBES/gate-b1-latest docs/planning/PROBES/gate-b2-latest

# Gate B1 — artifact name: security-findings-gate-b1-{run_id}
gh run download "$B1_RUN_ID" \
  --repo A-M-App-Hub/real-estate-control \
  --dir docs/planning/PROBES/gate-b1-latest/

# Gate B2 — artifact name: security-findings-gate-b2-{run_id}
gh run download "$B2_RUN_ID" \
  --repo A-M-App-Hub/real-estate-control \
  --dir docs/planning/PROBES/gate-b2-latest/

echo "Artifacts baixados:"
ls docs/planning/PROBES/gate-b1-latest/
ls docs/planning/PROBES/gate-b2-latest/
```

### 3.4 — Consolidar SECURITY_REPORT.md

```bash
HEAD_SHA=$(git rev-parse HEAD | cut -c1-7)
SECVAL_ID="SECVAL-$(echo "$B1_SHA" | cut -c1-7)-$(date +%Y%m%d)-$(cat /dev/urandom | tr -dc 'a-z0-9' | head -c 4)"

# Extrair contadores dos artifacts JSON
B1_JSON=$(find docs/planning/PROBES/gate-b1-latest/ -name "*.json" | head -1)
B2_JSON=$(find docs/planning/PROBES/gate-b2-latest/ -name "*.json" | head -1)

B1_CRITICAL=$(jq '[.tools[].findings[] | select(.severity == "CRITICAL")] | length' "$B1_JSON" 2>/dev/null || echo 0)
B1_HIGH=$(jq '[.tools[].findings[] | select(.severity == "HIGH")] | length' "$B1_JSON" 2>/dev/null || echo 0)
B1_DECISION=$(jq -r '.decision' "$B1_JSON" 2>/dev/null || echo "unknown")

B2_CRITICAL=$(jq '[.tools[].findings[] | select(.severity == "CRITICAL")] | length' "$B2_JSON" 2>/dev/null || echo 0)
B2_HIGH=$(jq '[.tools[].findings[] | select(.severity == "HIGH")] | length' "$B2_JSON" 2>/dev/null || echo 0)
B2_DRIFT=$(jq -r '.drift_detected' "$B2_JSON" 2>/dev/null || echo false)
B2_DECISION=$(jq -r '.decision' "$B2_JSON" 2>/dev/null || echo "unknown")

TOTAL_CRITICAL=$(( B1_CRITICAL + B2_CRITICAL ))
TOTAL_HIGH=$(( B1_HIGH + B2_HIGH ))

if [ "$TOTAL_CRITICAL" -gt 0 ]; then
  GATE_PROD="BLOQUEADO"
else
  GATE_PROD="LIBERADO"
fi

cat > docs/planning/SECURITY_REPORT.md << REPORT
# Security Report — real estate control

> Gerado por: \`skills/security-pipeline/SKILL.md\` Fase 3
> **Não editar manualmente** — será sobrescrito a cada ciclo pós-QA.

## Identificação

| Campo | Valor |
|-------|-------|
| Security Validation ID | \`$SECVAL_ID\` |
| Commit SHA | \`$B1_SHA\` |
| Report Date | $(date +%Y-%m-%d) |
| Gate prod | **$GATE_PROD** |

## Resumo de Achados

| Gate | Ferramenta | CRITICAL | HIGH | Decisão |
|------|-----------|----------|------|---------|
| B1 — SAST | OpenGrep | $B1_CRITICAL | $B1_HIGH | $B1_DECISION |
| B2 — Cloud Audit | gcloud / GCP | $B2_CRITICAL | $B2_HIGH | $B2_DECISION |
| **Total** | | **$TOTAL_CRITICAL** | **$TOTAL_HIGH** | **$GATE_PROD** |

## Runs

| Gate | Run URL | Status |
|------|---------|--------|
| B1 SAST | $B1_RUN_URL | $([ "$B1_DECISION" = "pass" ] && echo "GREEN" || echo "RED") |
| B2 Cloud Audit | $B2_RUN_URL | $([ "$B2_DECISION" = "pass" ] && echo "GREEN" || echo "RED") |

## Drift

Drift IaC detectado: \`$B2_DRIFT\`

$([ "$B2_DRIFT" = "true" ] && echo "> **ATENÇÃO:** Drift entre IaC e runtime GCP detectado — revisar PROBES/gate-b2-latest/ e re-aplicar IaC." || echo "Sem drift detectado.")

## Notas de Severidade (Gate B2 v2.0)

> Os seguintes achados foram elevados de HIGH → CRITICAL no Gate B2 (v2.0):
> - `Cloud Run ingress=all` → CRITICAL (B2-2b): tráfego direto da internet sem LB/Armor
> - `Image fora do Artifact Registry` → CRITICAL (B2-6b): risco de supply chain

## CVE Allowlist Ativa

$(if [ -f ".security-allowlist.json" ]; then
  python3 -c "
import json; from datetime import date
today = date.today().isoformat()
data = json.load(open('.security-allowlist.json'))
entries = [e for e in data.get('cve_allowlist', []) if not e.get('expires_at') or e['expires_at'] >= today]
if entries:
    print('| ID | Package | Reason | Expires |')
    print('|----|---------|--------|---------|')
    for e in entries:
        print(f\"| {e['id']} | {e.get('package','?')} | {e['reason'][:60]}... | {e.get('expires_at','never')} |\")
else:
    print('Nenhuma entrada ativa.')
" 2>/dev/null || echo "Allowlist não legível"
else
  echo "Nenhum .security-allowlist.json — todas as CVEs são enforced."
fi)

## Achados CRITICAL

$([ "$TOTAL_CRITICAL" -gt 0 ] && echo "> **BLOQUEADO PARA PROD** — $TOTAL_CRITICAL achado(s) CRITICAL encontrado(s). Criar fix stories via dev-agent antes de promover." || echo "Nenhum achado CRITICAL — prod liberado.")

$([ "$B1_CRITICAL" -gt 0 ] && jq -r '.tools[].findings[] | select(.severity == "CRITICAL") | "- **[\(.severity)]** \(.rule_id // .id): \(.message // .title) (\(.file // ""):\(.line // ""))"' "$B1_JSON" 2>/dev/null || echo "")
$([ "$B2_CRITICAL" -gt 0 ] && jq -r '.tools[].findings[] | select(.severity == "CRITICAL") | "- **[\(.severity)]** \(.check): \(.detail)"' "$B2_JSON" 2>/dev/null || echo "")

## Artifacts

- Gate B1: \`docs/planning/PROBES/gate-b1-latest/\`
- Gate B2: \`docs/planning/PROBES/gate-b2-latest/\`

## Histórico

| SECVAL ID | Data | SHA | Gate prod |
|-----------|------|-----|-----------|
| \`$SECVAL_ID\` | $(date +%Y-%m-%d) | \`$B1_SHA\` | $GATE_PROD |
REPORT

echo "SECURITY_REPORT.md gerado: $SECVAL_ID"
echo "Gate prod: $GATE_PROD"
```

### 3.5 — Commit SECURITY_REPORT.md

```bash
git add docs/planning/SECURITY_REPORT.md docs/planning/PROBES/
git commit -m "docs(security): consolidate security report $SECVAL_ID

Gate B1 (SAST): $B1_DECISION — CRITICAL=$B1_CRITICAL HIGH=$B1_HIGH
Gate B2 (Cloud Audit): $B2_DECISION — CRITICAL=$B2_CRITICAL HIGH=$B2_HIGH
Drift: $B2_DRIFT
Gate prod: $GATE_PROD"
git push origin main
```

### 3.6 — Verificar achados CRITICAL e registrar no ADR

```bash
if [ "$TOTAL_CRITICAL" -gt 0 ]; then
  echo "BLOQUEADO: $TOTAL_CRITICAL achados CRITICAL → prod BLOQUEADO"
  echo "Ação: criar fix stories via dev-agent para cada achado CRITICAL"
  echo "Registrar no ADR: prod bloqueado por $SECVAL_ID ($TOTAL_CRITICAL CRITICAL)"
  exit 1
fi
echo "Sem CRITICAL — prod liberado"
```

Atualizar `docs/planning/ADR.md` → seção "Gates de Segurança":

```markdown
| Gate | Run URL | Status | SECVAL | Data |
|------|---------|--------|--------|------|
| B1 SAST | <B1_RUN_URL> | GREEN / RED | <SECVAL_ID> | <data> |
| B2 Cloud Audit | <B2_RUN_URL> | GREEN / RED | <SECVAL_ID> | <data> |
| Prod | — | LIBERADO / BLOQUEADO | <SECVAL_ID> | <data> |
```

**Gate OUT:** SECVAL emitido e commitado em `SECURITY_REPORT.md` sem CRITICAL → `skills/debug-deploy/SKILL.md` pode promover para prod.

---

## Fase 5 — Gate prod: validação final antes de promoção

**Quando:** `skills/debug-deploy/SKILL.md` invoca promoção prod.

**Gate IN:** `docs/planning/SECURITY_REPORT.md` deve conter SECVAL id válido com SHA compatível com HEAD.

```bash
REPORT_PATH="docs/planning/SECURITY_REPORT.md"

if [ ! -f "$REPORT_PATH" ]; then
  echo "BLOQUEADO: SECURITY_REPORT.md não encontrado — executar Fase 3 antes de promover para prod"
  exit 1
fi

SECVAL_ID=$(grep "Security Validation ID" "$REPORT_PATH" | grep -o 'SECVAL-[^`]*' | head -1)
REPORT_SHA=$(grep "Commit SHA" "$REPORT_PATH" | grep -o '\`[^`]*\`' | head -1 | tr -d '`' | cut -c1-7)
HEAD_SHA=$(git rev-parse HEAD | cut -c1-7)
GATE_PROD=$(grep "Gate prod" "$REPORT_PATH" | grep -v "^#" | head -1 | grep -o 'LIBERADO\|BLOQUEADO' | head -1)

if [ -z "$SECVAL_ID" ]; then
  echo "BLOQUEADO: SECVAL não encontrado em SECURITY_REPORT.md — executar Fase 3"
  exit 1
fi

if [ "$REPORT_SHA" != "$HEAD_SHA" ]; then
  echo "BLOQUEADO: SECVAL é de commit diferente (stale)"
  echo "  SECVAL SHA: $REPORT_SHA"
  echo "  HEAD SHA:   $HEAD_SHA"
  echo "  Ação: re-executar Gates B1+B2 (Fase 3) e re-emitir SECVAL"
  exit 1
fi

if [ "$GATE_PROD" != "LIBERADO" ]; then
  CRITICAL_COUNT=$(grep -c "CRITICAL" "$REPORT_PATH" 2>/dev/null || echo "?")
  echo "BLOQUEADO: SECURITY_REPORT.md indica '$GATE_PROD'"
  echo "  Ver achados CRITICAL em $REPORT_PATH"
  exit 1
fi

echo "Gate prod: SECVAL $SECVAL_ID válido — prod liberado"
```

**Gate OUT:** prod liberado ou BLOQUEADO com remediação clara.

---

## Staleness Check

Se mais de 30 dias desde último SECVAL:

```bash
REPORT_DATE=$(grep "Report Date" docs/planning/SECURITY_REPORT.md | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}' | head -1)
DAYS_AGO=$(( ($(date +%s) - $(date -d "$REPORT_DATE" +%s 2>/dev/null || date -j -f "%Y-%m-%d" "$REPORT_DATE" +%s)) / 86400 ))
if [ "$DAYS_AGO" -gt 30 ]; then
  echo "AVISO: Security Report tem $DAYS_AGO dias — re-executar Gates B1+B2 antes de próximo deploy prod"
fi
```

Particularmente importante se houver mudanças em:
- Dependências (`pyproject.toml`, `uv.lock`, `package.json`, `bun.lock`)
- Implementação de auth
- Rotas de API
- IaC (roles, secrets management)

---

## ADR HARD GATE

Todo commit resultante de ações desta skill **deve** incluir atualização de `docs/planning/ADR.md` → seção "Gates de Segurança".

---

## Dívida Técnica Registrada

**Least-privilege SA (SECTECH-001):** `GCP_SERVICE_ACCOUNT` é o SA de deploy (admin-capable); reuso para audits read-only é funcional mas viola least-privilege. Follow-up: adicionar SA dedicado com roles `iam.securityReviewer` + `run.viewer` + `logging.viewer` no `base_tf_generator` + novo org secret `GCP_AUDIT_SERVICE_ACCOUNT`.

---

## Pinning e sincronização

- `iac_actions_pinned_sha` **>30 dias** → executar `skills/sync-esteira/SKILL.md` seção "Protocolo — Atualizar workflows do iac-actions" para atualizar os três security workflows.
- Após sync: re-executar Fase 0 para revalidar actionlint + SHA-pins dos workflows atualizados.
