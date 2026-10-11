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
