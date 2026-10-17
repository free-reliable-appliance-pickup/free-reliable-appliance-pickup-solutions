"""Read-only site health checks. Never modifies website or SEO experiment state."""
import json
import urllib.request
from datetime import datetime, timezone
from urllib.error import URLError, HTTPError

BASE = 'https://freereliableappliancepickup.com'
PATHS = ['/', '/robots.txt', '/sitemap.xml']
results = []
for path in PATHS:
    url = BASE + path
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'GoldStandardV3Monitor/1.0'})
        with urllib.request.urlopen(req, timeout=20) as response:
            status = response.status
            final_url = response.url
            body = response.read(250000)
            content_type = response.headers.get('Content-Type', '')
        result = {'url': url, 'status': status, 'final_url': final_url, 'content_type': content_type, 'bytes_checked': len(body), 'ok': status == 200}
        if path == '/robots.txt':
            result['has_user_agent'] = b'user-agent' in body.lower()
        if path == '/sitemap.xml':
            result['has_sitemap_xml'] = b'<urlset' in body.lower() or b'<sitemapindex' in body.lower()
    except (URLError, HTTPError, TimeoutError) as exc:
        result = {'url': url, 'ok': False, 'error': str(exc)}
    results.append(result)
report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'read_only': True, 'results': results}
with open('gold-standard-v3-health.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, indent=2)
print(json.dumps(report, indent=2))
if not all(r['ok'] for r in results):
    raise SystemExit('One or more public endpoints failed')
