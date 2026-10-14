#!/usr/bin/env python3
"""Optional weekly Search Console export. No secret => no API request."""
import csv, datetime as dt, json, os
from pathlib import Path
from urllib.parse import urlparse
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

SITE = "https://freereliableappliancepickup.com/"
PAGES = (
    "fresno-appliance-pickup", "fresno-county-appliance-pickup",
    "fresno-washer-dryer-pickup", "rowland-heights-appliance-pickup",
    "rancho-cucamonga-appliance-pickup",
)
def main():
    raw = os.getenv("GSC_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        print("GSC not configured: add authorized service-account JSON as a GitHub Actions secret.")
        return
    creds = service_account.Credentials.from_service_account_info(
        json.loads(raw), scopes=["https://www.googleapis.com/auth/webmasters.readonly"]
    )
    session = AuthorizedSession(creds)
    end = dt.date.today() - dt.timedelta(days=3)
    start = end - dt.timedelta(days=27)
    url = "https://www.googleapis.com/webmasters/v3/sites/" + __import__("urllib.parse", fromlist=["quote"]).quote(SITE, safe="") + "/searchAnalytics/query"
    rows = []
    for page in PAGES:
        body = {
            "startDate": start.isoformat(), "endDate": end.isoformat(),
            "dimensions": ["date", "page", "query", "device", "country"],
            "rowLimit": 25000,
            "dimensionFilterGroups": [{"filters": [{
                "dimension": "page", "operator": "equals", "expression": SITE + page + "/"
            }]}],
        }
        response = session.post(url, json=body, timeout=45)
        response.raise_for_status()
        for item in response.json().get("rows", []):
            keys = item.get("keys", [])
            if len(keys) != 5:
                continue
            rows.append([*keys, item.get("clicks", 0), item.get("impressions", 0),
                         item.get("ctr", 0), item.get("position", 0)])
    path = Path("gsc-priority-28d.csv")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["date", "page", "query", "device", "country", "clicks", "impressions", "ctr", "position"])
        writer.writerows(rows)
    print(f"Exported {len(rows)} Search Console rows for {len(PAGES)} priority pages; data is not committed.")
if __name__ == "__main__":
    main()
