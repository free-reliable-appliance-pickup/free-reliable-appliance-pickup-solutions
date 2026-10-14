# Puget Sound indexing policy restoration — October 14, 2026

## Verified problem

The final SEO safety audit failed for Seattle, Tacoma, Everett and Olympia: all four were indexable and included in sitemap.xml despite being absent from approved-indexable-locations.txt. The operational market-routing.json identifies Puget Sound as partner-recruiting with no assigned partner. Its rules allow city indexing for direct or partner-supported markets only.

## Technical correction and observation-window exception

Restore noindex,follow on the four city request pages and remove only their four sitemap entries. Keep the pages, forms and self-canonicals intact. Replace the recently added city-guide link blocks on Washington and Puget Sound with a regional coverage-review path and truthful recruiting language. The regional hub remains indexable. This corrects indexability and internal-link consistency under the existing technical/safety exception; it is not a speculative ranking experiment or permission to expand approved coverage. Do not approve these cities until operational coverage is verified.

## Validation

Locally executed the repository's existing final SEO safety audit, approved sitemap validation and noindex-link audit: all passed. Results: 699 approved indexable URLs, 129 noindex pages, zero links from indexable pages to noindex aliases. No sitemap dates or unrelated pages were changed. All four Colorado static source attribution repairs from the preceding batch are now independently confirmed on the public website.

Before deployment, compare branch HTML and sitemap byte-for-byte with the locally audited files, then inspect pull request checks. No ranking gain or new backlink is claimed.
