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
