---
name: sync-esteira
description: "Única função: comparar a esteira oficial (boas_praticas) com o SHA pinado neste repositório e, se houver mudanças, regerar skills locais a partir dos templates mais recentes (bootstrap-deploy, debug-deploy, sync-esteira, security-pipeline) e workflows de segurança. A partir da v2.0, workflows de segurança e CI/CD são buscados de iac-actions/templates/ (não mais da assets-library)."
license: Proprietary
metadata:
  org: "A-M-App-Hub"
  boas_praticas_repo: "boas_praticas_e_conhecimentos"
  esteira_github_path: "biblioteca_de_agent_skills/esteira_de_desenvolvimento"
  assets_library_pinned_sha: "local-dab472b513e1"
  iac_actions_repo: "A-M-Digital-Data-AI-LatAm/iac-actions"
  iac_actions_pinned_sha: "local-dab472b513e1"
---

# Sync Esteira — `real-estate-control`

Skill permanente (`pipeline-forge`) para **sincronização** com a fonte da verdade da esteira em `A-M-Digital-Data-AI-LatAm/boas_praticas_e_conhecimentos` (pasta `biblioteca_de_agent_skills/esteira_de_desenvolvimento`).

**Não faz** bootstrap, deploy nem debug — apenas mantém `skills/bootstrap-deploy/SKILL.md`, `skills/debug-deploy/SKILL.md`, `skills/security-pipeline/SKILL.md` e **esta** skill alinhadas aos templates oficiais quando a esteira evolui.

**NUNCA** persistir nomes de outros repositórios de aplicação em commits além do necessário ao diff local; referências a paths absolutos de espelho ficam só no ADR, como nas outras skills.

---

## Recovery após compactação de contexto

1. Ler este arquivo (`skills/sync-esteira/SKILL.md`) → `metadata.assets_library_pinned_sha`
2. Ler `docs/planning/ADR.md` → **Estado Atual**
3. Executar o protocolo **Detectar upstream** abaixo antes de regerar qualquer coisa

---

## Pré-requisitos

```bash
gh auth status
```

---

## Protocolo — Detectar upstream

**Duas fontes de verdade a monitorar:**
1. `boas_praticas_e_conhecimentos` (skills/skills templates) — `assets_library_pinned_sha`
2. `iac-actions` (workflows de segurança e CI/CD) — `iac_actions_pinned_sha`

### A) Detectar mudanças na esteira (boas_praticas)

1. Ler `pinned_sha` = `metadata.assets_library_pinned_sha` deste frontmatter.
2. Obter SHA upstream:

```bash
gh api "repos/A-M-App-Hub/boas_praticas_e_conhecimentos/commits?path=biblioteca_de_agent_skills/esteira_de_desenvolvimento&per_page=1" --jq '.[0].sha'
```

Registrar como `upstream_sha`.

3. Se `upstream_sha` == `pinned_sha` → **Nenhuma alteração na esteira** — pular para B.
4. Se diferente → identificar impacto nos templates sob `pipeline-forge/assets/`:
   - `bootstrap-deploy-template/SKILL.md`
   - `debug-deploy-template/SKILL.md`
   - `sync-esteira-template/SKILL.md` (esta skill)
   - `security-pipeline-template/SKILL.md`

### B) Detectar mudanças no iac-actions (workflows)

1. Ler `iac_actions_pinned_sha` = `metadata.iac_actions_pinned_sha` deste frontmatter.
2. Obter SHA upstream do iac-actions:

```bash
gh api "repos/A-M-Digital-Data-AI-LatAm/iac-actions/commits?path=templates&per_page=1" --jq '.[0].sha'
```

Registrar como `iac_upstream_sha`.

3. Se `iac_upstream_sha` == `iac_actions_pinned_sha` → **Nenhuma alteração nos templates** — fim.
4. Se diferente → listar arquivos alterados em `templates/`:

```bash
gh api "repos/A-M-Digital-Data-AI-LatAm/iac-actions/compare/<iac_actions_pinned_sha>...<iac_upstream_sha>" \
  --jq '.files[] | select(.filename | startswith("templates/")) | .filename'
```

Identificar quais workflows do app repo precisam ser atualizados.

---

## Protocolo — Regerar skills afetadas (boas_praticas)

**Fonte dos templates (rede, read-only):**

`https://raw.githubusercontent.com/A-M-Digital-Data-AI-LatAm/boas_praticas_e_conhecimentos/<upstream_sha>/biblioteca_de_agent_skills/esteira_de_desenvolvimento/pipeline-forge/assets/<template-folder>/SKILL.md`

**Valores para substituir** — extrair de `skills/debug-deploy/SKILL.md` **antes** de sobrescrever:

| Campo | Fonte |
|-------|--------|
| org | `metadata.org` deste arquivo |
| repo_name | `skills/debug-deploy/SKILL.md` → `metadata.repo_name` |
| service_name | idem |
| topology | idem |
| project_display_name | idem |
| topology_pattern | idem |
| sso_provider | idem |
| assets_library_pinned_sha | novo valor = `upstream_sha` |
| iac_actions_pinned_sha | manter valor atual (separar dos dois SHAs) |

1. Baixar cada template necessário no `upstream_sha`.
2. Aplicar substituições. Validar: `grep -rn '<[A-Z_]\+>' <arquivos>` não deve retornar fora de blocos de exemplo.
3. Escrever:
   - `skills/bootstrap-deploy/SKILL.md`
   - `skills/debug-deploy/SKILL.md`
   - `skills/sync-esteira/SKILL.md`
   - `skills/security-pipeline/SKILL.md` (se template alterado)
4. Atualizar `metadata.assets_library_pinned_sha` para `upstream_sha`.
5. Atualizar ADR.

---

## Protocolo — Atualizar workflows do iac-actions

**Quando:** `iac_actions_pinned_sha` != `iac_upstream_sha`.

**Fonte dos templates:**

```bash
# Para cada arquivo alterado em templates/, baixar via gh api:
# Exemplo: atualizar trigger-deploy.yml
gh api "repos/A-M-Digital-Data-AI-LatAm/iac-actions/contents/templates/cd/trigger-deploy.yml?ref=<iac_upstream_sha>" \
  --jq '.content' | base64 -d > .github/workflows/trigger-deploy.yml
```

**Mapeamento `iac-actions/templates/` → `app-repo/.github/workflows/`:**

| Template (iac-actions) | Destino no app repo |
|------------------------|---------------------|
| `templates/ci/release-please.yml` | `.github/workflows/release-please.yml` |
| `templates/ci/auto-merge-release.yml` | `.github/workflows/auto-merge-release.yml` |
| `templates/cd/ci-dev.yml` | `.github/workflows/ci-dev.yml` |
| `templates/cd/ci-qa.yml` | `.github/workflows/ci-qa.yml` |
| `templates/cd/cd-prod.yml` | `.github/workflows/cd-prod.yml` |
| `templates/cd/trigger-deploy.yml` | `.github/workflows/trigger-deploy.yml` |
| `templates/cd/trigger-build-and-push.yml` | `.github/workflows/trigger-build-and-push.yml` |
| `templates/cd/deploy-app-manual.yml` | `.github/workflows/deploy-app-manual.yml` |
| `templates/security/security-post-qa.yml` | `.github/workflows/security-post-qa.yml` |
| `templates/security/security-cloud-audit.yml` | `.github/workflows/security-cloud-audit.yml` |

**Mapeamento de arquivos de scaffold (root do app repo):**

| Template (assets-library) | Destino no app repo | Observação |
|--------------------------|---------------------|------------|
| `scaffold/.security-allowlist.json` | `.security-allowlist.json` | CVE allowlist — criar se não existe; **não sobrescrever** se já existe |
| `scaffold/.semgrepignore` | `.semgrepignore` | OpenGrep ignores — criar se não existe; **não sobrescrever** se já existe |

> **IMPORTANTE:** `.security-allowlist.json` e `.semgrepignore` nunca devem ser sobrescritos em syncs subsequentes se o app repo já os customizou. Copiar apenas se o arquivo não existe no app repo.

> **Nota:** `templates/ci/security-checks.yml` não existe mais — Gate A (secrets) é pre-commit hook local por repo. Ver `references/security-gate-contract.md`.

**NOTA:** `scaffold/ci.yml` e `scaffold/cd-qa.yml` só são copiados durante bootstrap (pipeline-forge Fase 0). Não sobrescrever em syncs subsequentes se o app repo já tem CI/CD real.

**Após copiar:**
1. Exibir diff de cada arquivo para revisão humana antes de commitar.
2. Atualizar `metadata.iac_actions_pinned_sha` para `iac_upstream_sha`.
3. Commit:

```
chore(workflows): sync iac-actions templates <old>..<new>

- Updated from A-M-Digital-Data-AI-LatAm/iac-actions@<iac_upstream_sha>
- Files changed: <lista dos arquivos>
```

4. Atualizar ADR: registrar sync `iac_pinned` → `iac_upstream`, data, arquivos tocados.

---

## Gate OUT

- Relatório textual:
  - Skills atualizadas (bootstrap-deploy, debug-deploy, sync-esteira, security-pipeline) ou "sem mudanças"
  - Workflows atualizados de `iac-actions/templates/` ou "sem mudanças"
  - Novos `assets_library_pinned_sha` e `iac_actions_pinned_sha`
  - Próxima ação: se trigger-deploy.yml ou trigger-bdc.yml atualizados, testar via deploy dev; se security-pipeline-template atualizado, rodar Fase 0 para revalidar gates.
