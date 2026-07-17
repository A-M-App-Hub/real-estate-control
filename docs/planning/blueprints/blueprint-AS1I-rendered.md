# Blueprint: real-estate-control (AS1I)

**Arquétipo:** AS1I — Front interno, sem persistência  
**Topologia:** FastAPI_Mixed + INTERNAL_CAS  
**Data:** 2026-07-16

---

## 1. Visão Geral

### Objetivos
- Ver solution-brief.yaml

### Escopo MVP
- UI/dashboard interno para consultores A&M
- **Sem banco de dados** — dados estáticos ou APIs externas read-only
- Acesso via CAS (auth-proxy)

### Restrições AS1I
- Proibido: PostgreSQL, Firestore, persistência local de usuário
- Se persistência necessária → migrar para AS3I

---

## 2. Arquitetura

**Topologia:** Minimal ([webapp-topologies.md §2.1](../../references/webapp-topologies.md))  
**Acesso:** INTERNAL_CAS ([access-topologies.md §2.1](../../references/access-topologies.md))

### tfvars congelados (dev)

```hcl
mixed_container_count    = 1
frontend_container_count = 0
backend_container_count  = 0
access_topology          = "internal_corp"
access_pattern           = "INTERNAL_CAS"
enable_auth_proxy        = true
sso_provider             = "CAS"
```

---

## 3. Stack

| Camada | Tecnologia |
|--------|------------|
| Frontend | React + Vite + bun |
| Backend embutido | FastAPI (mixed) ou static SPA |
| Auth | CAS via auth-proxy |
| BD | **N/A** |

---

## 4. SSO

**SSO: CAS** — pós-deploy: ticket `#infra-platform` ALLOWED_APPS

---

## 5. FinOps / PostHog

**Desativado** (v1 AS1I)
