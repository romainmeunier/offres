# SOW — SRE‑02 — Enablement Technique (Observabilité, SLOs & Incident Ops) (FR)

**Client** : …  ·  **Projet** : …  ·  **Date d’effet** : …  
**Prestataire** : Romain Meunier — Head of SRE (Indépendant) — Quito, Équateur (UTC‑5)

## 1) Objet & périmètre
Implémentation **plateforme‑agnostique** (K8s **optionnel**) : instrumentation (OpenTelemetry/agents), SLIs/SLOs, dashboards, alerting budgets, runbooks.

## 2) Livrables
- Plan d’instrumentation OpenTelemetry · Exporters (OTLP/Prom/Datadog/NR/Splunk)
- Collectors SLIs & 2–3 SLO live/service (error‑rate, p95/p99, dispo, RUM)
- Dashboards Grafana/Datadog + tagging/labels
- Budget‑based alerting (Alertmanager/Datadog/NR) + runbooks

## 3) Planning
1–2 semaines selon périmètre.

## 4) Hypothèses & responsabilités du Client
Accès read‑only; CI/CD existants; environnements de test disponibles.

## 5) Exclusions
Refonte applicative; astreinte P1 (option); déploiement outillage plateforme majeur (projet séparé).

## 6) Modalités financières
Forfait 4 000–8 000 USD (40% upfront, solde livraison).
