# SEO change and decision register

## 2026-10-23 — Seven existing Valley forms: optional paid-quote choice without JavaScript
- **Verified customer-intake inconsistency:** The published San Fernando Valley hub, Van Nuys, Granada Hills, Pacoima, Northridge, Mission Hills and Sylmar customer Formspree forms contain no static `paid_removal_preference` selector. `assets/paid-removal-choice.js` supplies the choice only after JavaScript loads, so customers without the enhancement cannot express the owner-approved paid quote interest or explicitly choose free-only. Existing San Fernando and North Hollywood forms already use a working static fallback and are left untouched. There is no evidence of actual lost leads or script failure.
- **Bounded technical exception:** Insert exactly one blank-default optional selector on each of those seven original forms using the previously merged San Fernando wording: `free_only` or `quote_ok` (interest in reviewing a separate quote, not a booking/payment). The JavaScript enhancer already detects `[name="paid_removal_preference"]` and skips duplicates. Extend the pre-existing SFV audit from 3 to 10 page contracts and add six tampered negative fixtures. Original Formspree POST, source_page, service, telephone, route, conditions, appliance rules, contacts, optional photos, titles, internal links, images, canonical, schema, sitemap and robots are unchanged.
- **Experiment control:** Seven Valley photo/SEO observation pages are protected through 2026-11-06 in the current decision log. This is a narrowly documented source-level *customer-form technical fix*, not a speculative organic ranking rewrite; use `[technical-fix]` commits. Do not interpret source consistency as evidence of conversion gains.
- **Validation and rollback:** Require exact-head CI including 10/10 SFV static quote contracts, positive/negative fixtures, 97 existing general-intake contracts, SEO Experiment Guard and GitHub Pages deploy after reviewed PR merge. Confirm the unchanged free-first language and optional choices on live URLs. Do not send test customer Formspree submissions or claim delivery without a controlled receipt test. Revert this isolated PR if form submission or free-only consent regresses.

## 2026-10-23 — Fresno general request form: mobile keypad hints (technical exception)
- **Verified source defect:** The existing Fresno general-appliance customer form has a required `type=tel` telephone field and required ZIP field but neither explicitly declares an `inputmode` hint. Other priority forms already use these mobile hints. This is a mobile usability consistency gap, not evidence of failed form delivery.
- **Minimal technical-only correction:** Add `inputmode=tel` to the existing telephone field and `inputmode=numeric` to the existing ZIP field. Extend the 97-page read-only customer-form regression guard with a Fresno-only assertion for these hints. Preserve every field name, value, required flag, endpoint, phone number, attribution, appliance policy, image, title, canonical, link and ranking copy. Inputmode is a keyboard hint, not a validation rule.
- **Experiment protection:** Fresno general appliance page remains listed in running SEO experiments with prior 2026-10-14 review gates. This narrowly scoped verified technical/mobile correction is documented under the registry's technical exception; it does not authorize speculative content changes. Daily SEO Ranking Countermove owns ranking experiments; Website Technical Repair owns emergencies.
- **Validation/rollback:** Require 97-page source contracts, fixture tests, experiment guard and exact-head GitHub checks before merge. Confirm live HTML separately after deployment; actual Formspree delivery and ranking impact are not claimed. Revert this isolated PR for any regression. GSC Wizard subscription remains blocked; no paid action taken.

## 2026-10-23 — SFV general appliance intake: restore service classification (six existing forms)
- **Verified technical defect:** Current main customer POST forms for Van Nuys, Granada Hills, Pacoima, Northridge, Mission Hills and the San Fernando Valley regional hub have one required telephone and correct static `source_page` but lack `service`. Other California general appliance forms explicitly send `service=General major appliance pickup`. The shared customer routing script is not relied on to fill this hidden field; missing classification is a form-data consistency issue, not proof of delivery failure.
- **Minimal exception:** Add exactly one static `service=General major appliance pickup` hidden field after `source_page` on each of these six already published request forms. Expand the existing source-only intake regression from 91 to 97 pages (five city pages and one regional hub); no new location page or lead recipient.
- **Preserve experiment gates:** The seven-page Valley photo experiment is frozen through 2026-11-06; its photo assets and ranking content remain unchanged despite the six form-field-only HTML edits. No images, preloads, social cards, title, canonical, schema, SEO body, internal links, sitemap or robots changes. The experiment guard requires a documented `[technical-fix]` commit prefix for this narrowly verified intake exception. Keep existing Formspree POST, telephone, paid-removal enhancement, pickup eligibility, local routing and partner-availability language unchanged. This is a documented factual/technical intake exception, not a ranking experiment; Daily SEO Ranking Countermove retains ranking/content tests and Website Technical Repair retains emergency fixes.
- **Evidence and rollback:** Verify only six one-line form insertions plus regression guard and this register; require positive/negative fixture tests, all 97 source contracts and exact-head GitHub CI. Check live HTML after deployment before claiming production. Do not submit real Formspree leads without consent. No ranking, delivery or local-partner improvement is claimed. Revert isolated PR if a regression occurs. GSC Wizard is currently subscription-blocked; no paid action authorized.


## 2026-10-23 — Southern California hub: repair missing SFV / Malibu / Ventura Coast navigation
- **Verified source issue:** The already published Southern California appliance regional hub links to broad Los Angeles County and SGV pages but has no links to the existing San Fernando Valley, Malibu, Ventura, Oxnard or Central Coast appliance request owners. Direct GitHub file lookups confirmed all five destination pages already exist, and the Central Coast hub already connects Ventura/Oxnard (so no edits needed there).
- **Small repair:** Add two navigational cards to the current Los Angeles County section and a short Ventura Coast request-only section with three existing-city links. Clearly state route/partner availability must be confirmed. No pages created and no changes to any city/Valley photo experiment, SEO meta or canonical, appliance qualification, sitewide phone/form, sitemap, robots or schema.
- **Guard:** New `scripts/audit-socal-hub-valley-coast-links.py` checks all five destinations exist, exact outbound link uniqueness, geographic section placement and no coverage promise; register in existing internal-link CI workflow.
- **Measurement:** Connected free-tier GSC Oct 18–20 returned no row for this regional page. This is a navigational repair, not evidence of organic ranking lift. After green CI/merge confirm live production HTML and deployment; future finalized impressions/clicks and qualified leads must be measured separately. Revert this isolated PR for regressions.

## 2026-10-23 — Extend priority California customer-form regression to seven Orange County cities (test-only)
- **Verified main-source contracts:** Existing Anaheim, Irvine, Huntington Beach, Santa Ana, Garden Grove, Fullerton and Yorba Linda general-appliance pages each contain one Formspree POST to the established customer endpoint, the correct city-specific `source_page`, `service=General major appliance pickup`, and a required telephone field. The pages are already published; this check does not imply successful real submissions or deliveries.
- **Bounded change:** Register those seven existing city pages in the established read-only `scripts/audit-priority-intake-contract.py` guard, expanding its expected page inventory from 84 to 91. No page HTML, phones, eligibility, Formspree endpoint, photographs, rankings, SEO text, canonicals, or active experiment assets are changed.
- **Validation and rollback:** Require existing positive/negative self-test, all 91 source contract checks, exact-head GitHub Actions and clean PR diff. Revert this test-only PR if the added guard has an unexpected regression. Source tests cannot prove live Formspree delivery or search rankings.


## 2026-10-23 — Restore Valley and Ventura coast navigation from Service Areas directory
- **Verified gap:** `/service-areas/` contains ~453 links, but its source has no direct links to 16 verified, already published Valley/Coast request URLs, including existing San Fernando, Van Nuys, North Hollywood, Ventura, Malibu and Oxnard pages. The visible city finder builds its choices from `main a[href]` already present on this page; without those links, exact city searches cannot return those destinations. Direct GitHub fetch confirmed all 16 targets exist. This is navigational/source-level evidence, **not** evidence of zero Google indexing.
- **Bounded repair:** Add one small descriptive section just beneath the existing directory search with eight San Fernando Valley and eight coastal links; explicitly state pickup qualification and route availability. Link to established city/intent owners only, no new indexable pages, no unsupported local partner claims. Keep all original location search logic, directory title/meta, canonical, schema, existing sitewide links and target pages unchanged, including the frozen SFV photo experiment.
- **Regression gate:** New `scripts/audit-valley-coast-directory.py` verifies all 16 link destinations, exactly one of each, finder unchanged and truthful availability qualification. Wire into already established priority city internal-links CI for PR and push.
- **GSC window:** Connected finalized three-day free sample Oct 18–20 shows 15 impressions, 0 clicks and mean position 3.73 for the directory; too small to prove persistent rank/CTR. Review user navigation and future finalized search signals, not rank claims. Revert isolated PR if a navigation regression appears.

## 2026-10-23 — Repair West LA / Valley appliance pickup service attribution (5 existing pages)
- **Confirmed source inconsistency:** Santa Monica, Calabasas, West Hollywood, North Hollywood and Santa Clarita each have exactly one customer Formspree POST and a required telephone + correct `source_page`, but lack the hidden `service` classification consistently present on gold-model California general-appliance forms. The site JS does not auto-add `service`. No live lost-lead or ranking injury is proven.
- **Minimal repair:** Add `service=General major appliance pickup` as one static hidden field in each existing customer form. Expand the already-running `scripts/audit-priority-intake-contract.py` to enforce the standard on these five existing pages (total 84 inspected including homepage and Idaho). This is not a content/SEO-rank experiment.
- **Strict preservation:** No modification to customer-written form data, original Formspree destination, required phone, paid quote choice, phones or routing, eligibility, heroes, city assertions, title, schema, canonical, links, sitemap, robots or other SEO copy. San Fernando seven-page photo experiment remains untouched. All the same mandatory source and service fields must occur once; no new location pages.
- **Gates:** Verify five-file form delta, one audit and changelog only, require all exact-head GitHub Actions green, then confirm public HTML after deployment. Real Formspree submission/receipt and ranking claims remain untested. Roll back by reverting isolated PR.

## 2026-10-23 — Fix missing service classification on three California coastal pickup forms
- **Verified source defect:** Existing Ventura, Oxnard and Malibu *general appliance* Formspree POST requests each had an original required telephone and correct `source_page`, but none had the hidden `service` value that established California owner forms and `scripts/audit-priority-intake-contract.py` require. The shared routing JavaScript does not add a `service` field. This is a request classification/consistency defect, **not** proof of a failed email, missed appointment, or ranking loss.
- **Bounded fix:** Add only `<input type="hidden" name="service" value="General major appliance pickup">` inside the three existing forms, after their `source_page`. Expand the existing priority intake contract check by these three already-published city pages (now 79 total if the previous 76 pass). The user-facing form, optional blank-default paid-quote consent, original approved Formspree action, source/phone routing, title, description, images, canonical, schema, links, sitemap, robots and text remain unchanged.
- **Acceptance and review:** Exact-head PR CI must pass, including form, market routing and gold-standard guards. Check change scope and public HTML after the merge. Do not submit a real customer test request without appropriate consent. No SEO ranking improvement claimed. Rollback through isolated PR revert.

## 2026-10-23 — Protect paid-quote consent on six existing Malibu/Ventura/Oxnard pickup forms
- **Verified issue:** All six already-published first-party Formspree forms had required telephone inputs, approved POST action, correct source attribution and existing shared JS customer routing, but no static `paid_removal_preference` field. The site script can insert an optional choice; a static fallback avoids depending entirely on the secondary enhancement. No live script failure, failed lead delivery or ranking issue is claimed.
- **Minimal fix:** Add a single optional blank-default `paid_removal_preference` select to general appliance and washer/dryer forms in Ventura, Oxnard and Malibu; `free_only` prohibits paid offers, `quote_ok` is only consent to consider a separate quote when free pickup is unavailable. No automatic price, booking, charge, or lead resale. JS enhancer already skips forms where a choice exists.
- **Preserved:** Original Formspree recipient, required phone and working-condition fields, sources, photos, call links, city eligibility, titles, content, canonical/indexing/schema, robots and sitemap unchanged; no new location URLs or claims of partner availability. Preserve seven-page Valley photo experiment untouched.
- **GSC baseline:** SMEPost connected domain, finalized Oct 18–20, 2026: Oxnard general page 2 impressions, 0 clicks, average position 4.5 across those 2 impressions only; other five pages returned no page row in this limited free window, not evidence of zero historical visibility. Do not claim rank or conversion lift.
- **Evidence gates:** Assert six existing source contracts, consent options, blank/default and JS duplicate guard; exact-head GitHub Actions. After merge verify public HTML for all six, GitHub Pages deployment, source-only field uniqueness; real submissions and lead receipt require separate permissioned test. Rollback by reverting this isolated PR.

## 2026-10-23 — Customer-form service attribution repair (South Pasadena, Glendale, Burbank)
- **Verified source defect:** Each existing general-appliance request form had a required telephone field and correct Formspree destination/source page, but omitted the hidden `service` classification used by the priority intake contract.
- **Bounded technical exception:** Add exactly one `service=General major appliance pickup` hidden field to each form and extend the existing read-only regression guard from 73 to 76 existing pages. South Pasadena city-boundary and Glendale/Burbank anti-template SEO experiments remain frozen for speculative changes; no titles, body, links, photos, canonicals, phones, acceptance rules, or routing changed.
- **Verification gate:** Run `python3 scripts/audit-priority-intake-contract.py --self-test` and `python3 scripts/audit-priority-intake-contract.py` in CI; verify branch diff, checks and deployment independently. Passing source tests does not prove Formspree receipt.

## 2026-10-23 — San Fernando Valley static paid quote fallback (3 existing forms)
- **Verified source gap:** San Fernando general appliance, San Fernando washer/dryer, and North Hollywood forms had no built-in paid-removal quote preference; existing site JavaScript provides the choice dynamically, but the important customer preference is invisible if that enhancement fails or is blocked. No production script failure or customer delivery loss has been established.
- **Minimal operational improvement:** Add one optional, blank-by-default consent choice to each existing Formspree form: free pickup only or consider a separate paid removal quote if free pickup cannot be offered. Review of a future price is not a booking, automatic charge, consent to release contact details to another business, or promise of availability. Dynamic enhancer skips forms already containing this field.
- **Guardrails:** Unchanged existing Formspree endpoint, required phone, source attribution, original qualification policy, city claims, photos, canonical, indexability, titles and social metadata. Do not modify any of the seven frozen photo-experiment pages from PR #410. No new city pages or scaled location copy.
- **Verification:** Check exact-head CI, three static form contracts and no duplicate selector; after deployment separately inspect live source and run a real permitted test form submission before claiming lead delivery. This is a customer intake reliability fix, not an SEO ranking claim. Roll back by reverting this isolated PR.

## 2026-10-23 — San Fernando Valley real appliance hero pilot (7 existing pages)
- **Verified issue:** Van Nuys, Granada Hills, Pacoima, Northridge, Mission Hills, Sylmar and the San Fernando Valley hub had only the brand logo in rendered source and logo-only social previews. Seven already-owned, visually inspected multi-appliance group photos exist in the repository; one different existing image is assigned to each page. Images are examples from the appliance photo collection, **not** claims that a job was done in the named neighborhood.
- **Baseline:** SMEPost GSC free three-day finalized window **2026-10-18 to 2026-10-20**: Granada Hills one impression, zero clicks (one-impression average position 1); the other six pages have no page-performance row in this limited window. Zero rows are not proof that Google has never shown those pages. No historical comparison available. Live/source pages inspected Oct 23. Current search competition exists: AppliancePickupNow Van Nuys and Woodland Hills, PickupMyAppliance Pacoima.
- **Hypothesis / page ownership:** A genuine non-logo hero and aligned social preview on each already-published owner page improve visitor trust and clarity without changing query intent; monitor exact city + free appliance pickup and associated page query/CTR/impressions, while keeping the San Fernando Valley hub as the regional owner. **No promise of ranking improvement.** Isolate just the hero/photo metadata variable.
- **Bounded change:** Add one 4:3 hero photo and align existing `og:image` and `twitter:image`, with factual collection-example alt text, on seven existing HTML pages. No new city URLs, title/meta description, body copy, phone, Formspree form/action, paid-quote preference, routing, canonical, schema, qualification, sitemap or robots changes. San Fernando's existing photos remain untouched.
- **Freeze/review:** Do not change speculative SEO content on these seven pages until Nov 6, 2026. Preferred comparison **Nov 9 or later** using finalized GSC and competitor visibility; keep/revise/revert based on evidence. Photo markup is a hypothesis, not proof of better ranking. Rollback: revert the one isolated PR. Verify CI exact head, image HTTP 200, mobile rendering and live HTML after merge separately.

## 2026-10-23 — Expand California priority intake regression coverage (test-only)
- **Evidence:** Rechecked 12 already-published California general-appliance pages on `main`: Chino, Chino Hills, West Covina, Covina, Glendora, Monrovia, Duarte, San Gabriel, El Monte, Azusa, Rosemead and Temple City. Each has exactly one existing customer Formspree POST, the expected `source_page`, `service=General major appliance pickup`, and a required `type=tel` phone input. This is source-contract verification, not evidence of actual submission delivery.
- **Change:** Expand `scripts/audit-priority-intake-contract.py` from 61 to 73 inspected pages (including homepage and Idaho). The already-connected CI check now covers these 12 existing city forms. No page HTML, phone, routing, photo, SEO content, schema, canonical, indexing, experiment registry or live customer behavior is modified.
- **Coordination:** Read `data/seo-experiments.json`; test-only scope does not modify protected experiments or emergency technical repair work. Preserve open PRs #328, #343 and #56. Require exact-head CI and 73-page/zero-error audit before merging. Source audit cannot establish Formspree receipt or organic ranking changes.

## 2026-10-23 — Four California customer-form attribution/mobile corrections (technical exception)
- **Evidence:** Current main `c9740811` contains existing Formspree POST pickup forms on Walnut, Rowland Heights and La Crescenta with `source_page` and a required phone field but no static hidden `service` classification. La Crescenta and Sierra Madre have required phone inputs lacking `type="tel"`; Sierra Madre already has the correct service classification. These are source-level intake/mobile inconsistencies, not evidence of failed submissions.
- **Minimal scope:** Add `service=General major appliance pickup` to the three existing forms; add `type="tel"` and `autocomplete="tel"` to La Crescenta and Sierra Madre phone inputs; extend `scripts/audit-priority-intake-contract.py` from 57 to 61 existing pages including homepage and Idaho. No changes to Formspree endpoint, requiredness, phone routing, service eligibility, customer copy, photos, SEO titles/meta, canonical, indexability, or experiment registry.
- **Coordination:** Preserve Walnut, Rowland Heights and Sierra Madre running SEO experiments. This is a documented factual/technical intake exception, not a ranking test. Diamond Bar is excluded because open PR #328 also edits that page; Westminster without `-ca` is Colorado and excluded from this California batch. Website Technical Repair retains emergency work.
- **Acceptance:** Require exact-head GitHub Actions checks, positive/negative fixture self-test, 61-page intake contract audit, and branch diff review before merge; verify public HTML separately. No real Formspree submission, dispatch or organic ranking improvement is claimed. Revert scoped PR on regression.
- **Status:** Proposed on isolated repair branch; deployment and real lead receipt unverified. Review 2026-10-24.


Use `SEO-CHANGE-CONTROL.md` for process rules. This public record contains no customer details. Existing experiment histories remain in `data/seo-experiments.json`; do **not** duplicate or overwrite them.


## 2026-10-23 — Idaho state request-form service attribution (technical exception)
- **Evidence:** Existing Idaho Treasure Valley/request-review page has a working-configuration Formspree POST form with `source_page=idaho-appliance-pickup` and required telephone input, but lacks a static `service` classification. This is a lead categorization inconsistency, not evidence of lost submissions.
- **Scope:** Add only `service=General major appliance pickup` after the existing source marker. Extend the existing intake contract audit to cover this existing state hub (57 inspected pages including homepage). No new cities, coverage claims, phone numbers, copy, photos, endpoints, canonicals, indexing directives or SEO experiments are changed. `data/market-routing.json` labels Idaho/Treasure Valley partner-recruiting; no active partner is claimed.
- **Safety:** Verified no Idaho-specific experiment in the registry; this technical intake correction is not a ranking experiment. Require positive/negative audit fixtures and exact PR-head CI before merge. Check deployed HTML separately; do not infer Formspree receipt or ranking changes from CI. Roll back this scoped PR if attribution or routing regresses.
- **Status:** Proposed branch/PR pending exact-head checks and deployment verification; review 2026-10-24.

## 2026-10-23 — Five High Desert California intake classifications (technical exception)
- **Evidence:** At main `24004ceb`, Hesperia, Apple Valley, Adelanto, Phelan and El Mirage existing general-appliance Formspree POST forms each have a city-specific `source_page` and a required `type=tel` phone input but no static hidden `service` classification. This is an attribution inconsistency, **not** evidence of failed submissions or lost leads.
- **Minimal fix:** Add exactly one `service=General major appliance pickup` hidden input after `source_page` on each of five existing forms. Extend the existing priority intake contract guard from 51 to 56 pages including homepage. Preserve all endpoints, phone numbers, routing, acceptance policy, customer-visible text, photos, metadata, schema, links, canonicals and indexing.
- **Experiment protection:** Reviewed `data/seo-experiments.json`: Hesperia, Adelanto and Phelan have protected ranking experiments. This verified form-metadata defect is a logged technical exception, not a ranking/content experiment; no experiment or emergency-repair ownership is modified.
- **Acceptance and limits:** Require exact-head PR checks, positive/negative fixtures and `PRIORITY_INTAKE_PAGES_INSPECTED 56` with zero failures before merging. Verify public HTML after deployment separately. Do not claim Formspree receipt, partner dispatch or ranking impact. Revert the scoped PR if regression occurs.

## 2026-10-23 — Four Inland/Pass California customer form classifications (technical exception)
- **Source evidence:** Main `a2d917f6` has existing Formspree POST pickup forms on Loma Linda, Banning, Beaumont and Hemet general-appliance pages, each with exactly one city-specific hidden `source_page`, a required `type=tel` phone input, and no hidden `service` field. The shared routing script does not supply that service classification. This is an attribution consistency gap, **not evidence of lost leads or failed submission**.
- **Narrow change:** Add one hidden `service=General major appliance pickup` input immediately after `source_page` on each existing form; expand `scripts/audit-priority-intake-contract.py` from 47 to 51 pages including homepage. Existing endpoint, phone numbers, customer fields, pickup qualifications, quotes/consent, routing, copy, photos, links, canonical, robots, sitemap and SEO experiment registry remain unchanged.
- **Change control:** Existing California SEO experiments remain protected; this is a documented operational technical exception, not a ranking experiment. Website Technical Repair retains emergency ownership and Daily SEO Ranking Countermove retains ranking/content experiments.
- **Required evidence:** Review exact six-file diff, run contract negative fixtures and 51-page source checks, verify PR CI before merge, then verify main, GitHub Pages and public HTML separately. No paid action, fake customer submission or claimed Formspree inbox receipt.
- **Rollback/status:** Revert the scoped PR if intake regresses. Proposed on isolated branch; merge, live deployment, delivery and ranking effect not yet verified at the time of entry.

## 2026-10-23 — Five California customer-form service classifications (technical exception)
- **Evidence:** Main at `66d607ed` has one Formspree POST customer form with a required `type=tel` phone input and `source_page`, but no static `service` field, on Norwalk, Long Beach, South El Monte, San Fernando and Sylmar general-appliance pages. No customer submission failure is established.
- **Change:** Add only `service=General major appliance pickup` after the existing `source_page` input on these five forms; extend the already-running priority intake contract audit to 43 pages including homepage.
- **Experiment coordination:** Long Beach's content experiment remains marked running (evaluate-not-before Oct 16). This technical intake attribution correction changes no title, body copy, schema, canonical, internal links, images, phone routing, service eligibility or ranking variables; all other experiments remain untouched.
- **Verification:** Require source contract audit, negative fixture self-tests, PR checks, exact branch diff, merge and live HTML confirmation separately. No fake test leads or paid actions. Passing checks cannot prove actual Formspree delivery or improved rankings.
- **Rollback:** Revert the bounded PR if the new attribution field interferes with intake.
- **Status:** Proposed on isolated repair branch; deployment and Formspree receipt not yet verified.

## 2026-10-23 — Enforce existing priority intake contract in CI
- **Verified gap:** The existing `scripts/audit-priority-intake-contract.py` was expanded to 38 pages, but the `Audit Priority Pickup Forms` workflow only ran `scripts/audit-priority-pickup-forms.py`. Its green 61-form audit did not independently demonstrate the 38-page guard or negative fixtures executed.
- **Change:** Add the existing contract script to both workflow path triggers and run its positive/negative fixture self-test and full source contract check as separate CI steps. No public page, form destination, routing, content, indexability or SEO experiment changed.
- **Verification/rollback:** PR must show both new steps succeeded and `PRIORITY_INTAKE_PAGES_INSPECTED 38`, `PRIORITY_INTAKE_FAILURES 0`, plus fixture results before merge. Revert this workflow-only change if it creates false positives. CI source checks do not prove live form receipt.
- **Status:** Branch proposal pending exact-head CI and merge at time of entry.

## 2026-10-23 — Southeast California Formspree service-attribution corrections (operational exception)
- **Classification:** Verified source-level customer intake metadata inconsistency, not a ranking experiment or reported delivery failure.
- **Pages:** `/la-mirada-appliance-pickup/`, `/cerritos-appliance-pickup/`, `/pico-rivera-appliance-pickup/`, `/downey-appliance-pickup/`.
- **Evidence:** Current main source had exactly one Formspree POST customer form on each page, with required telephone input and source-page attribution, but no static hidden `service` field. Each retains the established `https://formspree.io/f/mvzeapzd` destination. This does **not** prove any submission was lost.
- **Technical exception:** `data/seo-experiments.json` contains running Downey and Pico Rivera SEO tests (evaluate-not-before Oct 14). This change does not touch title, meta, body copy, schema, canonical, navigation, imagery, indexability or ranking variables; it only supplies the existing service classification consistently with PR #400. No ranking experiment was initiated.
- **Change:** Add exactly one hidden `service=General major appliance pickup` field after each existing `source_page` field; extend `scripts/audit-priority-intake-contract.py` by four existing pages (38 total including homepage).
- **Preserved:** Form action/method, mandatory contact fields, phone numbers and routing, optional customer fields, appliance eligibility, pickup claims, partner status, quote preferences and current SEO experiments.
- **Risk/rollback:** Medium-risk customer-form metadata update; review CI and branch diff before merge, revert the bounded PR on regression. No paid action, fake test lead, or end-to-end submission is authorized. Source assertions alone cannot verify actual receipt.
- **GSC context:** Connected SMEPost finalized Oct 18–20 only (three days, no comparisons). Too little for an SEO impact claim; operational field correction does not require a ranking hypothesis.
- **Status:** Feature-branch commits pending PR CI and merge; production deployment and real Formspree receipt unverified at time of entry.

## 2026-10-23 — Four California intake source and mobile input repairs (operational exception)
- **Classification:** Verified source-level customer-form attribution/mobile usability defects, not an SEO experiment or an emergency incident.
- **Pages:** `/palm-springs-appliance-pickup/`, `/la-canada-flintridge-appliance-pickup/`, `/altadena-appliance-pickup/`, `/san-marino-appliance-pickup/`.
- **Evidence:** Current `main` source on Oct 23 had one Formspree POST form on each page with required contact fields and `source_page` but no static hidden `service`. La Cañada Flintridge, Altadena and San Marino also had a required `phone` field without `type="tel"`. Shared `assets/customer-routing.js` does not automatically supply missing `service` fields. **No form-delivery failure is established.**
- **Existing controls:** Related merged PR #393 fixed the same class on other cities. The authoritative `data/seo-experiments.json` lists protected Coachella, Altadena, La Cañada Flintridge and San Marino experiments (evaluate-not-before dates Oct 9–15). This is a documented **technical exception**, not a ranking/content change. No registry values or experiment variables were changed.
- **Change:** Add exactly one static `service=General major appliance pickup` field to each existing form; add `type="tel"` to the three required phone inputs; extend `scripts/audit-priority-intake-contract.py` to include all four pages.
- **Unchanged:** Formspree action/method, customer field requiredness, customer text, pickup eligibility, paid-quote preference, telephone numbers, market/partner routing, images, SEO title/meta/body, canonical, robots, sitemap and internal links.
- **Risk and rollback:** Medium-risk customer-form source change; revert the bounded PR if validation finds a regression. No paid action or live test submission authorized.
- **Baseline:** Connected GSC free finalized Oct 18–20, 2026 window; Palm Springs page insight returned no page-level data. GSC is not a prerequisite for verified operational input corrections and no ranking effect is claimed.
- **Tests and deployment:** Branch source assertions passed for changed fields; expanded regression guard pending CI. PR merge, GitHub Pages deployment, public form rendering and actual Formspree receipt must be verified separately.
- **Status:** Committed to feature branch; **not yet merged/live verified** at time of entry. Review after CI/PR inspection; no speculative ranking experiment launched.

## 2026-10-22 — Process audit: quality checks were not triggered for ordinary HTML PRs
- **Finding:** `audit-content-uniqueness-fast.yml` only ran on sitemap/workflow changes; `audit-page-concentration.yml` ran on push but not PR. The quality reports therefore did not reliably appear **before merging city-page content edits**.
- **Evidence:** workflow trigger definitions read in GitHub on 2026-10-22.
- **Change:** PR [#385](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/pull/385); merged as `bc7674ce84974838f437b47c9142bd3519ff2818`.
- **Scope:** Two GitHub Actions workflow trigger files. No customer HTML, copy, images, phones, forms, redirects or canonical tags changed.
- **Verification:** All 13 available PR workflow runs completed successfully on head SHA `47504e0f6e689f67d0a79206913b3f9eb0a345ce`; the two intended diagnostics appeared in that run.
- **Status:** **Merged to main; CI execution verified.** This does not demonstrate that quality-score thresholds block a poor page or that a deliberate negative fixture was detected. No organic-impact claim.
- **Follow-up:** Test nonzero audit coverage and deliberate fail fixtures before claiming a complete preventive quality gate. Verify branch protection separately (GitHub integration returned 403 to a branch-protection read).

## 2026-10-22 — California lead classification normalization
- **Change:** PR [#384](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/pull/384); merged as `9b72927ee66767b1e038d3b76515f4592af46bb4`.
- **Scope:** Added missing hidden `service` attribution field to 26 existing California general pickup forms, leaving their existing source-page field intact.
- **Verification currently recorded:** GitHub merge; source-level change. **No independent live form receipt or organic ranking improvement is documented in this record.**
- **Status:** **Merged to main; live receipt and business effect unverified in this register.**
- **Follow-up:** Check a controlled form receipt for representative affected pages without exposing customer data.

## 2026-10-22 — Open limitations, not confirmed SEO defects
- **Google indexing:** Sitewide Page Indexing counts and per-priority-page Google-selected canonicals were not available from connected GSC Wizard (subscription required); the limited connected GSC performance window is not an indexing inventory. **Status: unverified**.
- **Production governance:** GitHub branch-protection read returned a 403 from the integration. **Status: governance configuration unverified**, not proof of protection or lack thereof.
- **Organic search:** Keyword.com and Ubersuggest metrics have different scopes and freshness. The 100-keyword tracking snapshot and estimated monthly domain traffic must not be conflated with each other or treated as proof of any single edit's impact.
- **Pending decision:** Avoid mass rewriting/deleting/redirecting pages until indexing inventory, real business coverage, search intent, and measurement are established.

## Template for subsequent changes
```text
Change ID / date:
Type / severity:
Issue and verified evidence:
Existing experiment ID / prior related PRs:
URL(s) / shared components affected:
Owner-approved business facts checked:
Hypothesis (for SEO experiments) or defect description:
Finalized baseline, last data date and source (or operational exception):
One variable / scope and exclusions:
Risk / approvals / rollback path:
PR and commit SHA:
Test scope, actual execution, results:
Live URL and receipt verification (or reason unavailable):
Status (proposed/branch/checks/merged/live/indexed/measured):
Observation window and review date:
Verdict (pending/improved/unchanged/regressed/inconclusive):
Next action / no-revisit-before:
```

## 2026-10-22 — Phoenix general form service classification
- **Type:** Verified operational attribution inconsistency; not a ranking experiment.
- **URL:** https://freereliableappliancepickup.com/phoenix-appliance-pickup/
- **Evidence:** Live HTML and main source lack a static service field; customer-routing.js does not add one. Existing city, state and source_page fields remain present. This does not establish failed delivery.
- **Change:** Add one hidden service=General major appliance pickup field on branch fix/phoenix-form-service-20261022. Base main: 9c8a791181d55a0f21ead95454e4e995f0311abe.
- **Prior work:** PR #384 applied the same classification to 26 California forms; all 26 live pages were checked on October 22 and contain the expected service and source fields and required phone input.
- **Risk/verification:** One additive hidden input; existing endpoint, visible fields, phones, content and indexability unchanged. Exact removal of the new line restores the original file. Review PR checks before merge; verify public HTML after deployment. No test submission or inbox receipt has been verified.
- **Baseline exception:** Operational field consistency does not require a search-ranking baseline; no SEO experiment variables changed.
- **Status:** Committed to branch; deployment and business impact pending. Rollback: remove the single added input. Review after deployment.


## 2026-10-22 — VGM homepage static form attribution
- **Type:** Verified operational intake attribution inconsistency; not an SEO experiment.
- **URL:** https://freereliableappliancepickup.com/#request
- **Evidence:** The homepage Formspree form in main contained no static `source_page` or `service` input. Shared customer-routing.js supplies `source_page` only when its submission handler runs, and does not supply `service`. Other priority city forms have both inputs. This does not prove failed delivery or missing leads.
- **Prior work / experiment check:** PRs #384 and #387 standardized the same inputs on city pages. `data/seo-experiments.json` includes an ongoing homepage title/meta CTR test with an evaluation gate of 2026-10-14; no title/meta, internal links, canonical, or indexability settings are changed here.
- **Change:** Add two static hidden homepage pickup-form fields: `source_page=home` and `service=General major appliance pickup`. Preserve the existing Formspree endpoint, visible inputs, required phone, ZIP, state, city, qualification, routing JavaScript and all customer-facing content.
- **Pre-merge source tests:** Exact-one-form-anchor check; positive assertions for both fields; baseline negative fixture without both fields; exact diff reconstruction confirms no other homepage changes. Tests passed locally in the connected GitHub read/write session, not an end-to-end submission.
- **Risk / rollback:** Narrow medium-risk operational attribution fix. Rollback is removal of the two added hidden input elements.
- **Status:** Committed to review branch `fix/vgm-homepage-intake-attribution-20261022`. PR/CI, merge, actual public HTML, Google effects and Formspree inbox receipt are not yet verified at the time of this record.
- **Follow-up:** Review PR checks; verify deployed public HTML and complete an authorized controlled inbox receipt test. Do not treat missing lead attribution as proof of lost leads.


## 2026-10-22 — VGM organic ranking and competitor scoreboard codified
- **Type:** Documentation and repeatable verification method; no live page, form, phone, schema, canonical, link or routing modification.
- **Evidence:** The existing `SEO-GOLD-MODEL.md` already advised SERP and competitor analysis but had no single mandatory per-market/per-query scoreboard defining comparability, missing-rank notation and decision gates. Owner requested that organic search and competitor rankings become mandatory parts of "Use VGM."
- **Change:** Defined VGM command, baseline fields, competitor SERP comparison, GSC query/page/device measures, qualified-lead outcome, experiment gate and reporting standard; connected it to `SEO-CHANGE-CONTROL.md`. No ranking performance improvement is claimed.
- **Safety:** Preserves `data/seo-experiments.json` as the only experiment calendar and `data/market-routing.json` as operational market truth; prevents changes based on missing evidence.
- **Review:** [PR #389](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/pull/389). This is a documentation-only change; verify its current merge state in GitHub. No CI check was triggered on the documentation-only PR at initial inspection.


## 2026-10-22 — VGM priority customer form regression gate
- **Type / evidence:** Verified missing CI assertion, not a confirmed form-delivery failure. The existing `Audit Approved Request Actions` workflow checked for a Formspree endpoint and same-page request links, but did not assert a required customer phone or consistent `source_page` and `service` tracking fields on the homepage/priority city forms. The homepage source/service omission was repaired in PR #388; this check is designed to prevent recurrence.
- **Scope:** Add `scripts/audit-priority-intake-contract.py` (root home and 23 existing priority general city pages) and invoke its one positive plus seven negative fixtures and read-only source audit in the existing approved-actions PR workflow. Preserve original customer HTML, scripts, business routing, images, titles, metadata, and experiment registry.
- **Baseline observations:** The reviewed priority forms contain static source/service fields and required phone inputs. Phoenix has the existing label `Phoenix city page` and Columbus has lowercase `general appliance pickup`; this audit respects those established values rather than altering customer-facing forms as part of a CI change.
- **Acceptance:** CI must report 24 inspected HTML pages with zero failures; test fixtures must demonstrate that a missing/wrong attribution, unrequired phone, wrong method/endpoint and duplicate customer form are rejected. Record actual PR checks, not just test presence.
- **Scope limits:** The test checks repository HTML; it is not evidence of GitHub Pages deployment, Google indexing, organic positions, call tracking, or successful receipt by Formspree.
- **Vancouver routing:** Existing issue #378 already records a distinct unresolved mismatch between the public partner-supported description and `data/market-routing.json` recruiting status. Do not infer approved partner forwarding or override market truth in this CI change.
- **Rollback:** Revert the added script and workflow step; no production content to undo.
- **Status:** Review branch `ci/vgm-priority-intake-regression-20261022`; merge and check outcomes are separate verification steps.


## 2026-10-23 — VGM four-city California intake attribution technical exception
- **Source evidence:** Current main at `a3fb49140090c35274a48160caaef1f9d9f6df6f` had one existing Formspree POST pickup form, a correct `source_page`, and a required `type=tel` phone on Temecula, Murrieta, Victorville and Palm Desert general-appliance pages, but no hidden `service` classification. Missing classification is not proof of a failed submission or lost lead.
- **Technical-only repair:** Add exactly one hidden `service=General major appliance pickup` field to each of those four existing forms. Extend `scripts/audit-priority-intake-contract.py` from 43 to 47 existing pages including homepage. No customer-visible content, phone routing, Formspree destination, condition eligibility, canonical, schema, internal links, photo, market routing or SEO experiment change.
- **Freeze/ownership:** Reviewed `data/seo-experiments.json`; Temecula, Murrieta, Victorville and Palm Desert have ranking experiments. This is the permitted verified technical-attribution exception, not a speculative SEO change; leave the Daily SEO Ranking Countermove and emergency Website Technical Repair work untouched.
- **Acceptance:** Exact six-file branch diff; required-phone/source/service assertions and positive/negative fixture tests; 47-page priority intake audit with zero failures; passing relevant GitHub Actions on exact PR head before any merge. Verify deployment separately. No real Formspree receipt, organic ranking gain or new local service capability is claimed.
- **Rollback:** Revert the scoped pull request if regression occurs.
