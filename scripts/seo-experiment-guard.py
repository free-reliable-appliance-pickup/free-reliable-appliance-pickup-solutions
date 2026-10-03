#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import date

data=json.loads(Path("data/seo-experiments.json").read_text(encoding="utf-8"))
today=date.today()
print("SEO_EXPERIMENT_FILE_UPDATED", data.get("updated"))

def sh(*args):
    try:
        return subprocess.check_output(args, text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""

def changed_files():
    base=os.environ.get("GITHUB_BASE_REF","").strip()
    if base:
        out=sh("git","diff","--name-only",f"origin/{base}...HEAD")
    else:
        out=sh("git","diff","--name-only","HEAD^","HEAD")
    return {x.strip() for x in out.splitlines() if x.strip()}

def page_file(path):
    slug=(path or "").strip("/")
    return "index.html" if not slug else f"{slug}/index.html"

changed=changed_files()
message=sh("git","log","-1","--pretty=%B")
technical_override=message.lstrip().startswith("[technical-fix]")
if changed:
    print("CHANGED_FILES", len(changed))
    for p in sorted(changed):
        print(" -",p)
if technical_override:
    print("::warning title=SEO experiment technical override::Protected-page change allowed because commit message starts with [technical-fix]. Verify that this is truly technical/factual/indexability/safety work and log the reason.")

running=0
blocked=[]
for e in data.get("experiments",[]):
    if e.get("status")!="running":
        continue
    running+=1
    gate=e.get("evaluateNotBefore")
    pages=set(e.get("pagesChanged",[]))
    owner=e.get("protectedOwner")
    if owner:
        pages.add(owner)
    pages.update(e.get("protectedOwners",[]))
    page_files={page_file(p) for p in pages if p}
    touched=sorted(changed & page_files)

    if gate:
        gate_date=date.fromisoformat(gate)
        if today < gate_date:
            print(f"::notice title=SEO experiment protected::{e['id']} — freeze before {gate}. Pages: {', '.join(sorted(pages))}")
            if touched and not technical_override:
                blocked.append((e["id"],gate,touched))
        else:
            print(f"::notice title=SEO experiment review due::{e['id']} — compare finalized GSC against baseline before more edits. Pages: {', '.join(sorted(pages))}")
    else:
        print(f"::warning title=SEO experiment missing gate::{e['id']} — running experiment has no evaluateNotBefore date. Pages: {', '.join(sorted(pages))}")

print("RUNNING_EXPERIMENTS",running)
if blocked:
    print("\nSEO_EXPERIMENT_GUARD_BLOCK")
    for exp,gate,files in blocked:
        print(f"- {exp}: protected until {gate}; touched: {', '.join(files)}")
    print("Use a separate PR and wait for the observation window. Only verified technical/factual/contact/indexability/safety fixes may bypass with a commit message beginning [technical-fix], and the reason must be recorded.")
    sys.exit(1)
