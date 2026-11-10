#!/usr/bin/env python3
"""Restore stove fuel and safe disconnection questions for expanded SC/NC pages.
Never changes pickup coverage claims, contact routing, photos or robots.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
FUEL = '<label>Stove fuel type<select name="fuel_type" required><option value="">Choose fuel type</option><option>Electric</option><option>Natural gas</option><option>Propane</option><option>Dual fuel</option><option>Not sure</option></select></label>'
CONNECTION = '<label>Safe disconnection status<select name="connection_status" required><option value="">Choose status</option><option>Already safely disconnected</option><option>Qualified professional will disconnect before pickup</option><option>Still connected; professional required</option><option>Not sure</option></select></label>'

def run():
    staged=[]
    checked=0
    for code in ("SC","NC"):
        manifest=json.loads((ROOT/"data/ttg-state-batches"/(code+".json")).read_text(encoding="utf-8"))
        paths=sorted(p for p in manifest["pages"] if "-stove-oven-pickup/index.html" in p)
        if len(paths)!=50:
            raise RuntimeError(f"Expected 50 {code} stove pages; got {len(paths)}")
        for rel in paths:
            path=ROOT/rel
            s=path.read_text(encoding="utf-8")
            old=s
            needs=[]
            if 'name="fuel_type" required' not in s: needs.append(FUEL)
            if 'name="connection_status" required' not in s: needs.append(CONNECTION)
            if needs:
                idx=s.find('name="access"')
                begin=s.rfind("<label",0,idx)
                if idx<0 or begin<s.find('<form ') or idx>=s.find("</form>"):
                    raise RuntimeError("Missing unique access field on "+rel)
                s=s[:begin]+"".join(needs)+s[begin:]
            for wanted in ('name="fuel_type" required','name="connection_status" required','name="access"','name="privacy_acknowledgment"','noindex, follow','formspree.io/f/mvzeapzd'):
                if wanted not in s:
                    raise RuntimeError(f"{rel}: absent {wanted}")
            if len(re.findall(r'<form\b',s))!=len(re.findall(r'<form\b',old)) or len(re.findall(r'<img\b',s))!=len(re.findall(r'<img\b',old)):
                raise RuntimeError("Unexpected structural change "+rel)
            if s != old: staged.append((path,s))
            checked+=1
    for path,s in staged: path.write_text(s,encoding="utf-8")
    print(f"PASS: {checked} SC/NC stove pages include fuel type and safe disconnection; updated {len(staged)}")

if __name__ == "__main__":
    run()
