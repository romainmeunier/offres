# SOW — SRE‑02 — Technical Enablement (Observability, SLOs & Incident Ops) (EN)

**Client**: …  ·  **Project**: …  ·  **Effective date**: …  
**Contractor**: Romain Meunier — Head of SRE (Independent) — Quito, Ecuador (UTC‑5)

## 1) Scope
**Platform‑agnostic** implementation (K8s **optional**): instrumentation (OpenTelemetry/agents), SLIs/SLOs, dashboards, budget‑based alerting, runbooks.

## 2) Deliverables
- OpenTelemetry instrumentation plan · Exporters (OTLP/Prom/Datadog/NR/Splunk)
- SLI collectors & 2–3 live SLOs/service (error‑rate, p95/p99, availability, RUM)
- Grafana/Datadog dashboards + tagging/labels
- Budget‑based alerting (Alertmanager/Datadog/NR) + runbooks

## 3) Timeline
1–2 weeks depending on scope.

## 4) Assumptions & Client responsibilities
Org‑level read‑only access; existing CI/CD; test environments available.

## 5) Out of scope
Application refactor; P1 standby (option); major platform tooling deploy (separate project).

## 6) Commercials
Fixed $4,000–$8,000 (40% upfront, balance on delivery).
