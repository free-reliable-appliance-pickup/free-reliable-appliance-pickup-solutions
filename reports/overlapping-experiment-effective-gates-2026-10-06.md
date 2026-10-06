# Overlapping SEO Experiment Effective Gates — 2026-10-06

## Purpose

This is an analysis-only guardrail for pages that belong to multiple running SEO experiments with different `evaluateNotBefore` dates.

**Rule:** a page's effective gate is the latest gate among all running experiments touching that page. An earlier experiment reaching its review date never authorizes an edit while another overlapping experiment remains frozen.

Mixed-gate overlap pages found: **14**.

| Page | Effective gate | Running experiment gates |
|---|---|---|
| `/chino-appliance-pickup/` | **2026-10-14** | `2026-10-13` — 2026-10-03-chino-city-focus<br>`2026-10-14` — 2026-10-04-california-anti-template-cleanup |
| `/covina-appliance-pickup/` | **2026-10-14** | `2026-10-13` — 2026-10-03-covina-city-focus<br>`2026-10-14` — 2026-10-04-california-anti-template-cleanup |
| `/la-puente-appliance-pickup/` | **2026-10-14** | `2026-10-13` — 2026-10-03-la-puente-city-focus<br>`2026-10-14` — 2026-10-04-california-anti-template-cleanup |
| `/orange-county-appliance-pickup/` | **2026-10-14** | `2026-10-13` — 2026-10-03-orange-county-hub-parity<br>`2026-10-14` — 2026-10-04-california-anti-template-cleanup |
| `/pasadena-appliance-pickup/` | **2026-10-14** | `2026-10-13` — 2026-10-03-pasadena-city-parity<br>`2026-10-14` — 2026-10-04-california-anti-template-cleanup |
| `/phoenix-appliance-pickup/` | **2026-10-14** | `2026-10-09` — 2026-10-01-phoenix-city-metro-separation<br>`2026-10-14` — 2026-10-01-commercial-authority-links |
| `/san-bernardino-appliance-pickup/` | **2026-10-14** | `2026-10-13` — 2026-10-03-san-bernardino-support-page-handoff<br>`2026-10-14` — 2026-10-04-california-anti-template-cleanup |
| `/stockton-washer-dryer-pickup/` | **2026-10-14** | `2026-10-13` — 2026-10-03-stockton-laundry-owner<br>`2026-10-14` — 2026-10-04-california-anti-template-cleanup |
| `/west-covina-appliance-pickup/` | **2026-10-14** | `2026-10-13` — 2026-10-03-west-covina-city-parity<br>`2026-10-14` — 2026-10-04-california-anti-template-cleanup |
| `/arcadia-appliance-pickup/` | **2026-10-15** | `2026-10-14` — 2026-10-04-arcadia-altadena-top10-ctr-test<br>`2026-10-15` — 2026-10-05-arcadia-laundry-intent-cleanup |
| `/escondido-appliance-pickup/` | **2026-10-15** | `2026-10-14` — 2026-10-04-escondido-people-first-intent-cleanup<br>`2026-10-15` — 2026-10-05-escondido-laundry-support-handoff |
| `/laguna-hills-appliance-pickup/` | **2026-10-15** | `2026-10-14` — 2026-10-04-laguna-hills-niguel-boundary<br>`2026-10-15` — 2026-10-05-south-oc-laundry-support-handoff |
| `/salem-appliance-pickup/` | **2026-10-15** | `2026-10-14` — 2026-10-04-salem-heading-hierarchy-cleanup<br>`2026-10-15` — 2026-10-05-salem-laundry-intent-cleanup |
| `/tustin-appliance-pickup/` | **2026-10-15** | `2026-10-14` — 2026-10-04-tustin-owner-page-cleanup<br>`2026-10-15` — 2026-10-05-south-oc-laundry-support-handoff |

## Operating rule

Before any ranking/content/internal-link/schema-intent edit:
1. Read `data/seo-experiments.json`.
2. Find every running experiment that contains the page in `pagesChanged`, `protectedOwner`, or `protectedOwners`.
3. Use the latest `evaluateNotBefore` as the effective page gate.
4. If the problem involves a sibling/wrong-ranking page, calculate that page's effective gate too.
5. Require finalized GSC evidence after the relevant last change before editing.
