# Rancho Cucamonga — protected SEO title restoration record

**Recorded:** 2026-11-18 (local project date)  
**Pull request:** #1466, currently proposed, **not approved or deployed by this record**  
**Experiment:** `2026-11-12-rancho-laundry-exact-city-title` in `data/seo-experiments.json`

## Verified technical reason for protected-page correction

The title experiment registered on November 12 uses the dedicated page HTML title and WebPage structured-data name:

`Free Washer & Dryer Pickup in Rancho Cucamonga, CA`

A subsequent, unrelated website change (#1451) changed these two fields to `Free Washer & Dryer Pickup Rancho Cucamonga, CA | Request` while the registered experiment remained protected until November 29. Restoring exactly the registered title and structured-data name is a technical correction to preserve the original experiment, **not** a new SEO experiment.

Separately, #1464 modified the Rancho **general** pickup page title, description, OG metadata and WebPage metadata. The exact-head California City Gold Model audit failed because the title lost the required `Removal` term and the description lost `washers` and `dryers`. Reverting those six search-metadata values restores the pre-#1464 Gold Model terms, retaining `dateModified=2026-11-18`.

## Scope and protections

- Restored `rancho-cucamonga-washer-dryer-pickup/index.html` HTML title and WebPage.name only.
- Restored `rancho-cucamonga-appliance-pickup/index.html` six search-metadata values only; kept its other code unchanged.
- No changes to either page's H1, body, photos, Formspree forms, source tracking, phone, canonical, indexability, appliance qualifications, or operational promises.
- No new city or specialty URLs.
- The experiment observation gate stays **2026-11-29**; preferred review **2026-12-03**.

## Measurement and safeguards

Google Search Console through Windsor.ai for 2026-10-20 to 2026-11-16 reported 522 impressions and 5 clicks for the general page, versus 9 impressions and 0 clicks for the dedicated washer/dryer page. These historical measurements do not establish causality or predict ranking improvement.

The earlier standalone general-page correction passed 50 GitHub workflows on its former head. This updated combined correction **must pass all relevant workflows again on the new head**; previous checks are not transferable. GitHub CodeQL, California Gold Model, Search Appearance and SEO Experiment Guard must be green before approval. Independent review and an explicit accountable maintainer approval are required by `docs/TTG_RELEASE_POLICY.md`. Do not merge or declare a live release merely because the tests pass.

After approval and merge, verify public page source, actual mobile form and contact flows, and later settled GSC data. Avoid speculative changes to the protected Rancho washer/dryer page before November 29.
