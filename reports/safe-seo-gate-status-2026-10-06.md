# Safe SEO Gate Status — 2026-10-06

## Decision

Do not force another customer-facing ranking edit today.

The current experiment registry contains **192 running experiments** and **274 distinct protected page paths** when both `pagesChanged` and `protectedOwner(s)` are honored. The remaining unfrozen Search Console candidates have samples too small to justify a speculative rewrite.

## Search Console / sitemap health

Finalized GSC evidence used for ranking decisions is available through **2026-10-03**.

Current Search Console sitemap status:
- `https://freereliableappliancepickup.com/sitemap.xml`
- latest observed submitted URL count: **697**
- errors: **0**
- warnings: **0**
- Google last downloaded the sitemap again on **2026-10-06**

## Performance

Current PageSpeed lab results:
- Mobile LCP: **2.0 s**
- Mobile CLS: **0**
- Mobile TBT: **67 ms**
- Desktop LCP: **988 ms**
- Desktop CLS: **0**
- Desktop TBT: **42 ms**

Performance is not the primary ranking bottleneck in the current priority markets.

## Full-site schema follow-up

A previous automated full-site alert reported 22 pages with duplicate WebPage JSON-LD IDs.

On current `main`, all 22 formerly flagged source files were rechecked:
- each now contains exactly **one** WebPage schema node
- each now contains exactly **one** matching page-specific `#webpage` ID

Live deployment spot-checks were also performed for:
- Coachella Valley
- San Diego
- Bakersfield
- Whittier washer/dryer
- San Jose

All five returned HTTP 200, a self-referencing canonical, one WebPage node, and one matching `#webpage` ID.

## Technical safeguard completed today

Commit `83fe6ada22474b905166c871e223a65e6e04c11d` updates the Final SEO Safety Audit so direct HTML pushes to `main` now trigger the full approved-path, sitemap, canonical, title, H1 and retired-link validation.

This closes a monitoring gap without changing customer-facing experiment variables.

## Unfrozen GSC candidates after correct experiment exclusion

The opportunity filter now uses the union of:
- `pagesChanged`
- `protectedOwner`
- `protectedOwners`

That corrected an earlier false-safe classification for Fontana stove/oven and the San Bernardino County support page.

Remaining unfrozen zero-click candidates are low-volume:
- Hayward appliance pickup — 4 impressions, weighted avg position ~9.75
- Ventura appliance pickup — 4 impressions, ~23.25
- Hillsboro appliance pickup — 3 impressions, ~4.33
- Temple City washer/dryer — 3 impressions, ~7.33, but overlaps a protected city-owner test
- Temecula washer/dryer — 3 impressions, ~17.33

These samples are not strong enough to justify a new page rewrite on October 6.

## Next evidence gates

### 2026-10-09
Review finalized post-change GSC first for:
- Coachella Valley
- Denver
- Phoenix

Use the saved October 6 baseline. Protect page-one signals; if exact city modifiers remain weak, make at most one minimal authority/ownership improvement per experiment.

### 2026-10-13
First review window opens for multiple October 3 experiments including:
- El Monte
- West Covina
- Pasadena
- Orange County hub
- Temple City
- Covina
- Monrovia
- Chino
- La Puente
- Stockton
- San Bernardino support handoff

### 2026-10-14
Major ownership/anti-template review gate:
- Rancho Cucamonga
- Fontana
- Ontario
- Upland
- Fresno / Central Valley ownership
- Sacramento
- homepage
- California priority anti-template pages
- many October 4 city tests

## Rule

At each gate:
1. Pull finalized GSC first.
2. Compare against the recorded baseline.
3. Protect working/page-one signals.
4. Identify exact wrong-page ownership before editing.
5. Make one minimal evidence-backed change, validate it, reset the observation window.
6. Do not create thin city × appliance pages or copy competitor promises.


## Additional technical safeguards completed

### Priority health-monitor expansion

Commit `e66e3b9742e746aee5f9375a5e5f9873edbbd899` expanded the fast priority monitor beyond the original 22-page set.

New high-priority checks include:
- Fontana
- Ontario
- San Bernardino city + county
- Riverside city + county
- Phoenix Metro
- Sacramento
- Stockton
- Coachella Valley
- Palm Desert
- Aurora

This is monitoring-only and does not modify any ranking experiment.

### All advertised sitemap validation

Commit `a8f453055d3b6048e7a82de108911677d47986f6` changed the Final SEO Safety Audit so it reads every same-domain `Sitemap:` directive from `robots.txt`, verifies the advertised file exists, and validates the URLs from all advertised sitemap files against the approved indexable inventory.

Current validation:
- Rancho Cucamonga sitemap: 5 URLs, all present in main sitemap
- Fontana: 5 / clean
- Ontario: 5 / clean
- Pomona: 5 / clean
- Riverside: 5 / clean
- Los Angeles: 5 / clean
- San Bernardino: 5 / clean
- Fresno: 5 / clean
- Stockton: 5 / clean
- Sacramento: 6 / clean
- Denver: 11 / clean
- Phoenix: 37 / clean
- priority SGV/IE: 50 / clean
- regular washer/dryer sitemap: 97 / clean
- image sitemap: 563 page URLs; all 563 also appear in the main sitemap

No advertised priority sitemap was missing and no tested priority sitemap contained a foreign or main-sitemap-orphan URL.

## October 9 dependency clarification

The Denver exact-query ownership problem overlaps the running Lakewood/Denver boundary experiment:
- `denver appliance pickup` → `/lakewood-appliance-pickup/` — 5 impressions, avg position 10 in the finalized baseline.
- Lakewood boundary experiment evaluateNotBefore: **2026-10-14**.

Therefore the October 9 Denver review must not force a Denver/Lakewood ownership edit. The first combined ownership decision is October 14+.

Phoenix exact city-modifier rows currently route to `/phoenix-appliance-pickup/`, so Phoenix's measured problem is ranking strength rather than wrong-page city/metro ownership.

## October 14–16 ownership sequencing

Because wrong-page URLs have their own active experiments:
- Oct 14: first review for Fresno, Upland, and the mature portions of Rancho/Fontana.
- Oct 15: Rancho overlap involving `/southern-california-freezer-pickup/`.
- Oct 16: Fontana overlap involving `/rialto-washer-dryer-pickup/`.

Do not invalidate a support-page experiment to accelerate an owner-page experiment.
