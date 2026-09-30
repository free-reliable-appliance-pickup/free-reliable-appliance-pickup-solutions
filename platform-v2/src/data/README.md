# Location Data Rules

This directory is the single source of truth for reusable location-page data in Platform V2.

## Why this exists
The live site currently contains many separate HTML files. V2 will keep the public URLs but move repeatable facts into structured data so updates can be made consistently without hand-editing hundreds of pages.

## What belongs in structured data
- city/state/county/market
- phone routing
- canonical URL
- page title and meta description
- hero image and alt text
- qualification summary
- neighborhoods and ZIPs when accurate/useful
- appliance-specific links
- nearby-city links
- FAQs

## What must stay unique
Structured data is **not** permission to mass-produce thin pages. Every indexable city page must still include useful local information that is genuinely relevant to that market.

## Migration rule
A live page is not replaced simply because a V2 data record exists. It must first pass SEO-parity and content-quality review.
