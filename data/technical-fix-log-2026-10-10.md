# Technical pickup-intake fixes — 2026-10-10

## Reason for interrupting protected SEO experiment pages
Customer pickup forms had missing or defaulted condition data, omitted floor/property/photo information, and in several cases invalid nested HTML `label` elements. These are verified technical and customer-accuracy issues, not a ranking-copy experiment. Partners need dependable machine condition, property type, stairs and access before accepting a route.

Changes to protected experiment pages were made under the technical/factual exception in `data/seo-experiments.json`. Do **not** reset experiment baselines or assume that these fixes improved rankings. Evaluate protected SEO experiments after their existing 2026-10-13/14 review gates using finalized Search Console data.

## Changes made
- Repaired nested condition-field labels on Chino, Chino Hills, Covina, West Covina, Pasadena and El Monte.
- Added descriptive condition details, blank default appliance/condition selections, property type, stairs/floor and photo availability where missing; preserved the working condition, approximately 80% mixed-load qualification, dishwasher and microwave limits.
- Ensured source-city attribution in the form submissions where absent.
- Corrected misleading default floor/stair selections on Altadena.
- Added location-specific pickup-access and mixed-load clarification in Montclair for more accurate customer disclosure; no city intent/keyword ownership was intentionally changed.
- Preserved existing Formspree endpoint, telephone contact and canonical page targeting.

## Source pages reviewed / updated
Montclair, San Bernardino, Chino, Chino Hills, La Verne, San Dimas, Pomona, Upland, Claremont, Covina, West Covina, Pasadena, Duarte, Altadena, Temple City, San Marino, Alhambra, El Monte, Baldwin Park, La Puente, Diamond Bar, Rowland Heights, Whittier, Pico Rivera, Montebello, Irwindale, Azusa, Arcadia, Monrovia, Bradbury, Sierra Madre, La Cañada Flintridge, La Crescenta, Rosemead, Fresno, Sacramento, Stockton, Phoenix, Denver, Aurora, Portland and Salem.

## Representative commit evidence
- Chino nested-label repair: `6db1ed0476be915973d0400c3a892abb9f9c98f6`
- Chino Hills nested-label repair: `f11b90d35b89731bb48bfb04cc1817c05f6d1034`
- West Covina label repair: `4a65efa9773c79dd6d351f59c56729778bd04a69`
- Pasadena label repair: `66a714bd083ac6779366c4dba2ed173d968f6ac1`
- El Monte label repair: `7f8de1159b689e29265c91358b886eb85a5fe0b6`
- Altadena accessibility / intake repair: `160f39a0f7ffeb60f15c3a4d556b5ee2013b18fd`
- Rosemead intake completeness: `ed8203124d0ed82d5381a58ec1a3fcbe952c8fbe`
- Fresno photos field: `6ad7c719cf95fbc59ff64fc336c63ddfaa4312fb`
- Phoenix photos field: `069b5c7b00d65bfa264eada5d6cd04fb450a8f26`
- Portland photos field: `2a8c5285dc97f1ab2d4d6fad034e21bb99714fe9`

## Verification and remaining work
Source checks verified the forms and required fields on the edited pages. A fresh public, CSS-scoped form read on 2026-10-10 confirmed Rosemead's new fields were deployed and separately confirmed Fresno's photo-availability question. A submitted lead was **not** sent, so form delivery remains untested. The new `scripts/audit-priority-pickup-forms.py` with its workflow should help prevent future regressions; confirm its GitHub Actions run separately.

This change log records technical exceptions for the protected pages without changing the content experiment hypotheses or review dates.

## Additional form-audit remediation
- Initial GitHub Actions intake audit run #38102955357 checked 42 pages and found two missing `source_page` fields (Duarte and Altadena).
- Added Duarte `source_page` attribution in commit `b06110197a27fcf641d079a95b5e5c01b54f2eb4`.
- Added Altadena `source_page` attribution in commit `d0eca7f493ffa804472e8d3fbcff6e1f6adefac2`.
- These are attribution/technical corrections only. A subsequent CI result must be checked independently before marking the automated audit as passed.

## Final automated verification
- Audit Priority Pickup Forms workflow run [#38103074005](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/actions/runs/38103074005) **PASSED** after the Duarte and Altadena attribution corrections: `PRIORITY_INTAKE_FORMS_CHECKED 42`, `PRIORITY_INTAKE_ERRORS 0`.
- This verifies repository-source form structure and required fields; it is not a live customer form submission test or Google ranking measurement.

## Next Inland Empire / San Gabriel Valley intake batch
On 2026-10-10, fixed confirmed request-form technical defects in Rialto, Bloomington, Colton, Highland, Grand Terrace, Redlands, Yucaipa, Moreno Valley, Jurupa Valley, Eastvale, Corona, Norco, Walnut, Hacienda Heights, Avocado Heights, South San Jose Hills, San Gabriel, Monterey Park and City of Industry. Added missing `condition_details`, `location`, `stairs`, `property_type`, `photos_available`, `city` and `source_page` fields as applicable; corrected nonblank auto-selections where found. These updates are customer-accuracy/lead-routing repairs, **not speculative title, main content, internal-link or schema experiments**. The 909 regional numbers and Formspree endpoint were preserved.

The audit script now covers 61 city pages. The related same-city, head-to-head competitor observations and dated ranking-experiment gates are recorded in `data/competitor-parity-2026-10-10-rialto-redlands-sgv.md`. Review its evidence before changing any protected page's substantive SEO structure. The 61-city GitHub Actions result must be checked independently and should not be described as passed until confirmed.

## Verified result — expanded local batch
- The 61-city audit passed in [GitHub Actions run #38103500707](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/actions/runs/38103500707), printing `PRIORITY_INTAKE_FORMS_CHECKED 61` and `PRIORITY_INTAKE_ERRORS 0`.
- A GitHub Pages build/deployment run [#38103624310](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/actions/runs/38103624310) completed with successful build, deploy and report jobs.
- Fresh public form-scoped reads (without test POSTs) of **all 19 newly repaired city pages** confirmed city/source attribution, condition explanation, floor/location, stairs, property type, photo availability, a blank required condition selection, and the existing Formspree destination. The first reads before the successful deployment showed older content; the subsequent reads showed the new fields.
- This verifies deployment of the HTML form changes, **not** a live form email-delivery test, a Google indexing/ranking improvement, or local-partner availability.

## Sitemap freshness verification — 2026-10-10
- Commit `54b4bdb259a1b974f10bcee1b9a7e4efd7f54c41` updated the `<lastmod>` value of **18 recently repaired Inland Empire / San Gabriel Valley city URLs** to `2026-10-10`, excluding Rialto (already current). Preserved all **698 existing URL entries** and their ordering. This is a truthful source-change marker, not a guarantee of Google reindexing.
- GitHub Actions **Audit Active Sitemap Pages**, [run #38105561044](https://github.com/free-reliable-appliance-pickup/free-reliable-appliance-pickup-solutions/actions/runs/38105561044), **PASSED**. The audit examined 17 sitemap files, identified 314 active market pages, found 314 with request links and shared branding, 313 with local forms, and **0 active noindex** pages.
- The observed `313/314` local-form count is not automatically an error: the remaining active page has a request link and the existing audit passed. Do not misrepresent it as 314 validated forms or as proof of Google indexing.
- This checks repository source / CI, not a Google Search Console inspection or a live customer request submission.
