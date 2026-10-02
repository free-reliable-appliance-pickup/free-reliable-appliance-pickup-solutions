#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import date

data=json.loads(Path("data/seo-experiments.json").read_text(encoding="utf-8"))
today=date.today()
print("SEO_EXPERIMENT_FILE_UPDATED", data.get("updated"))
running=0
for e in data.get("experiments",[]):
    if e.get("status")!="running":
        continue
    running+=1
    gate=e.get("evaluateNotBefore")
    pages=", ".join(e.get("pagesChanged",[]))
    if gate:
        gate_date=date.fromisoformat(gate)
        if today < gate_date:
            print(f"::notice title=SEO experiment protected::{e['id']} — avoid speculative rewrites before {gate}. Pages: {pages}")
        else:
            print(f"::notice title=SEO experiment review due::{e['id']} — compare finalized GSC against baseline before more edits. Pages: {pages}")
    else:
        print(f"::notice title=SEO experiment running::{e['id']} — Pages: {pages}")
print("RUNNING_EXPERIMENTS",running)
