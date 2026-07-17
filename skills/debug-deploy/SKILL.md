---
name: debug-deploy
description: "Skill permanente pós-bootstrap: deploy canônico (dev/qa/prod), recovery com ARCHITECTURE.md, loop de debug doc-first (4 tiers), correção operacional autônoma + validação CAS, e gates humanos de prod."
license: Proprietary
metadata:
  persona: Forge
  repo_name: "real-estate-control"
  service_name: "realestatecontrol"
  topology: "FastAPI_Mixed + INTERNAL_CAS"
  project_display_name: "real estate control"
  topology_pattern: "FastAPI_Mixed"
  sso_provider: "CAS"
  assets_library_pinned_sha: "local-dab472b513e1"
---

# Debug Deploy — `real estate control`

Skill **permanente** gerada pela esteira (`pipeline-forge`). Assume **bootstrap inicial já concluído** e `docs/planning/ARCHITECTURE.md` presente após remoção da `bootstrap-deploy`.

Cobre:
- Recuperação de contexto (ADR + arquitetura + logs + referências de deploy)
- Deploy **dev/qa** com dispatch canônico e smoke
- **Debug** doc-first (loop 4 tiers, `MAX_ITERATIONS=3` por sessão)
- **Prod** com gates humanos (0/4/5) e checklist pós-deploy manual (DNS/CAS)

**Fontes permitidas:**
- `assets-library/` (pinned SHA: `local-dab472b513e1`)
- `base_tf_generator` HTTP API quando validação/bootstrap incremental for necessária
- Espelho read-only **se** o usuário fornecer `A-M-App-Hub/real-estate-control` (registrar repo no ADR, sem persistir em assets)

**NÃO** referenciar repositórios externos por nome em commits ou assets.

---

## Recovery após compactação de contexto

1. `docs/planning/ADR.md` → **Estado Atual**
2. `docs/planning/ARCHITECTURE.md` → topologia e recursos vivos
3. `docs/planning/DEBUG_LOG.md` → últimas entradas
4. `docs/planning/REFERENCE_DEPLOYS.md` → última entrada do ambiente alvo
5. Re-ler este arquivo
6. **Antes de agir:** protocolo **BEFORE ACTING** + (se deploy ou falha nova) **Pré-deploy doc refresh** abaixo

---

## Pré-deploy doc refresh (Fase “0-lite”)

**Quando:** antes de novo deploy após falha **ou** se `ADR`/`DEBUG_LOG` indicar sintoma novo **ou** pin `assets_library` >30 dias (`skills/sync-esteira` recomendado).

**Ações:**
1. `prohibited-actions.md`
2. `symptom-fix-catalog.md`
3. `lessons-learned/INDEX.md`
4. Reaplicar o mapa de leituras da topologia igual à `bootstrap-deploy` Fase 0 (topics 01–11 conforme `FastAPI_Mixed` + `04` se CAS).

Registrar bullets curtos no ADR (**Docs relidas para este deploy**) — não reproduza o relatório inteiro se já consta em ciclo anterior, salvo mudança de incidente/topologia.

### Staleness Check — Security Reports

Se mais de 30 dias desde última auditoria:

- Ler ADR seção "Gates de Segurança"
- Verificar data do `security_validation_id` mais recente
- Se STALE: invocar `skills/security-pipeline/SKILL.md` Fase 3 (Gates B1+B2 + re-emitir SECVAL)
- Particularmente importante se houver mudanças recentes em:
  - Dependências (requirements.txt, package.json)
  - Auth implementation
  - API routes
  - IaC (role, secrets management)

### Cloud Runtime + CI/CD Security (Gate B2)

- `security-cloud-audit.yml` roda automaticamente após `CI (qa)` via `workflow_run`
- Pode ser acionado manualmente: `gh workflow run security-cloud-audit.yml`
- Drift vs IaC → `docs/planning/DRIFT_REPORT.md`
- Orquestração e interpretação de resultados: `skills/security-pipeline/SKILL.md` Fase 3




---

## Protocolo BEFORE ACTING

1. `assets-library/docs/prohibited-actions.md`
2. `assets-library/docs/lessons-learned/INDEX.md`
3. `gh auth status` e, se necessário, seguir `references/gh-cli-prerequisite.md`
4. `base_tf_generator` se validação infra for necessária
5. Pergunta: *Tem deploy de referência similar? `A-M-App-Hub/real-estate-control` ou `skip`.* (mesmo contrato das outras skills)

---

## Protocolo Copy + Substitute

```bash
cp <assets-library>/<categoria>/<arquivo> <destino>
sed -i "s|<placeholder>|<valor>|g" <destino>
grep -n '<[A-Z_]\+>' <destino> && echo "FAIL: placeholder remanescente" && exit 1
```

---

## Fase 2 — Deploy Dev ou QA

**Gate IN:** `iac_scripts/` + `.github/config/` consistentes; sem placeholders fugidos.

**Ler antes:** `assets-library/workflows-cd/`, `assets-library/gates/gate0-iam-checklist.md` quando IAM for suspeito.

**Pré-dispatch obrigatório — sync de origin:**

```bash
git log --oneline origin/main..HEAD
# Se houver linhas: git push origin main
```

> `gh workflow run` usa `origin/main` HEAD — commits locais não pushed não entram no build.
> Lesson: `09-workflows-and-dispatch.md` § push-before-dispatch

**Dev dispatch:**

```bash
gh workflow run "CI (dev)" -f ref='<branch_or_sha>' -f force_apply=<true|false>
```

**QA dispatch:** usar workflow copiado do asset `final_ci_qa.yml` com o **nome** registrado no repositório (ex.: `CI (qa)` — confirmar em `.github/workflows/`).

**Após run:** smoke em `docs/planning/SMOKE_REPORTS/<run-id>.md`; append `REFERENCE_DEPLOYS.md`; atualizar ADR com URL do run.

**Falhas:** atualizar `DEBUG_LOG.md`; entrar em **Fase 2.5**.

---

## Fase 2.5 — Debug especializado

**Fluxo:**
1. **Tier 0 — Cross-check app trigger + iac-actions (SEMPRE PRIMEIRO ao debugar deploy falho):**

   ```bash
   # Perspectiva 1: App repo (ci-dev/ci-qa/cd-prod)
   APP_RUN_ID=$(gh run list --workflow "CI (dev)" --limit 1 --json databaseId --jq '.[0].databaseId')
   # Ou CI (qa), CD (prod) conforme o ambiente que falhou
   APP_CONCLUSION=$(gh run view "$APP_RUN_ID" --json conclusion --jq '.conclusion')
   APP_JOBS=$(gh run view "$APP_RUN_ID" --json jobs --jq '.jobs[] | "\(.name): \(.conclusion)"')
   echo "App trigger: $APP_CONCLUSION"
   echo "$APP_JOBS"

   # Perspectiva 2: iac-actions (run_url via Step Summary do trigger)
   # Ver job "Cross-check iac-actions security" no Step Summary do run acima
   gh run view "$APP_RUN_ID" --log | grep -E "iac_conclusion|security_passed|iac-actions run"

   # Se você tem o run_id do iac-actions:
   IAC_RUN_ID="<run_id do iac-actions>"
   gh api "repos/A-M-Digital-Data-AI-LatAm/iac-actions/actions/runs/${IAC_RUN_ID}" --jq '{conclusion, status}'
   gh api "repos/A-M-Digital-Data-AI-LatAm/iac-actions/actions/runs/${IAC_RUN_ID}/jobs" \
     --jq '.jobs[] | "\(.name): \(.conclusion)"'
   ```

   **Diagnóstico:**
   - `iac_conclusion=failure` + job `deps-audit` falhou → CVE não allowlistada em deps → `uv audit --format json` / `bun audit --json` localmente; adicionar a `.security-allowlist.json` se exceção aprovada (ver `iac-actions/docs/SECURITY-ALLOWLIST.md`)
   - `iac_conclusion=failure` + job `Trivy IaC` falhou → IaC misconfig → revisar policy em `iac-actions/policies/`
   - `iac_conclusion=failure` + job `Conftest` falhou → recurso não na allowlist OPA → abrir issue em `iac-actions`
   - `iac_conclusion=failure` + todos security jobs passaram → problema de infra (tofu plan/apply), não de segurança
   - `iac_conclusion=success` mas app trigger falhou → problema no caller (build, checkout, config)
   - Ambos falharam → diagnosticar separadamente
   - Cross-check bloqueando (exit 1): a partir de v2.0, `security_passed=false` causa falha do job `cross-check` no app repo — não apenas warning

2. **Tier 1 — Catálogo + INDEX:** iniciar por `symptom-fix-catalog.md`, depois `lessons-learned/INDEX.md` → arquivo de lesson alvo  
3. **Tier 2 — Cruzadas:** `base_tf_generator` docs pertinentes + `central-auth-service` apenas se CAS + `prohibited-actions.md` sempre  
4. **Tier 3 — Fix mínimo:** commit citing `lessons-learned/<topic>.md` literal na mensagem; verificar `git log origin/main..HEAD` e push se ahead; dispatch canônico; aguardar  
5. **Tier 4:** parar e registrar perguntas objetivas em `DEBUG_LOG.md` + ADR

**Integração `log-hunter`:** se a skill `log-hunter` existir no ambiente Cursor do repositório, use-a para condensar logs GitHub Actions / Cloud Run **antes** de Hipóteses Tier 2–3.

**Contrato inviolável:** mesmo da `bootstrap-deploy` (sem atalhos proibidos; `MAX_ITERATIONS=3` por sessão de debug salvo reset explícito humano documentado no `DEBUG_LOG`).

**Gate OUT:** verde para novo deploy **ou** Tier 4 documentado.

---

## Fase 2.6 — Correção Operacional

**Gate IN:** Root cause identificada (Tier 1–3 da Fase 2.5) — estratégia de fix conhecida.

### Step 1 — Pré-requisitos operacionais

1. Verificar `gcloud --version` → se ausente, **STOP**: instruir instalação da Google Cloud CLI.
2. Verificar `gcloud auth list` → confirmar conta ativa e projeto configurado.
3. Verificar IAM do operador para o recurso alvo:
   - `gcloud run services describe <svc> --region=<region> --project=<project_id>`
   - Se 403 / permissão negada → ir para sub-passo de infra de acesso (abaixo).

### Step 2 — Aplicar correção

Dois tipos de correção:

**Correção de configuração via gcloud** (ex: variáveis de ambiente, revisão, service account):
- Executar comando `gcloud` diretamente
- Documentar comando no `DEBUG_LOG.md`
- Exemplo: `gcloud run services update <svc> --region=<region> --project=<project_id> --update-env-vars=<VAR>=<VALUE>`

**Correção de infraestrutura** (Terraform/IaC):
- Dispatch workflow CD canônico: `gh workflow run "CI (dev)" -f force_apply=true`
- Seguir padrão smoke + `REFERENCE_DEPLOYS.md` da Fase 2
- Atualizar `DEBUG_LOG.md` com nova entrada

**Sub-passo: falta de acesso**

Se o operador não possui permissões IAM necessárias para aplicar a correção:
1. Identificar a role/binding faltante em `assets-library/gates/gate0-iam-checklist.md`
2. Dispatch infra deploy para conceder o binding antes de prosseguir
3. Re-verificar com `gcloud auth list` + describe command

### Step 3 — Testes pós-correção

1. **Health check:** `gcloud run services describe <svc>` para revisar revisão nova **OU** `curl https://<public-url>/health`

2. **Functional test (endpoint):**
   - Se `CAS == CAS`: **STOP** → Solicitar ao usuário um CAS token válido antes de prosseguir
     - Mensagem: _"Para executar o teste real no endpoint, preciso de um CAS token válido. Por favor, gere um token em `<cas_issuer_url>` e cole aqui."_
     - Formato esperado: JWT bearer passado como cookie nas requisições curl
     - Usar padrão: `curl -H "Cookie: cas_token=<TOKEN>" https://<public-url>/api/<endpoint>`
   - Montar curl contra a URL pública (Load Balancer / DNS), não direto na Cloud Run URL
   - Testar endpoint relevante (ex: `/api/health`, `/api/pov/{id}`, `/generate`)

3. **Registrar resultado:**
   - Se teste OK → append `REFERENCE_DEPLOYS.md`, update ADR, commit citing a correção
   - Se teste FAIL → re-entrar em Fase 2.5 com nova entrada no `DEBUG_LOG.md` (incrementar iteração)

**Gate OUT:** Teste funcional verde + ADR atualizado + commit documentado.

---

## Fase 3 — Deploy Prod (Gates humanos)

**Gate IN:** smoke dev/qa OK + release processual completo conforme ADR.

### Gate 0 — IAM

**STOP — APROVAÇÃO HUMANA**

`assets-library/gates/gate0-iam-checklist.md` com o e-mail do operador de deploy e o `project_id` do ambiente alvo (vide ADR / `*.tfvars`).

### Gate 4 — Dispatch IaC Prod

**STOP — APROVAÇÃO HUMANA**

`assets-library/gates/gate4-iac-dispatch.md`.

### Gate 5 — Cloud Run Prod

**STOP — APROVAÇÃO HUMANA**

`assets-library/gates/gate5-cloud-run-approval.md` — parse outputs tofu; aprovar imagens conforme runbook.

**Checklist pós-deploy (manual, nunca automatizar nesta skill):**
- DNS A/AAAA para o `api_domain` de produção registrado nos tfvars / ADR
- CAS `ALLOWED_APPS` se auth-proxy
- Smoke externo após propagação

**Gate OUT:** ADR → “Deploy prod concluído”.

---

## ADR HARD GATE

Commits resultantes de ações desta skill **devem** manter `docs/planning/ADR.md` coerente (Estado Atual + Dívidas).

---

## Pinning e sincronização

- `assets_library_pinned_sha` **>30 dias** → preferir executar `skills/sync-esteira/SKILL.md` antes de mudanças estruturais  
- Revalidar `base_tf_generator` antes de qualquer geração nova de IaC
