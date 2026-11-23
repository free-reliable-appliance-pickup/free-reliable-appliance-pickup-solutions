#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import date, timedelta

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
base_ref=os.environ.get("GITHUB_BASE_REF","").strip()
if base_ref:
    # PR workflows use a synthetic merge commit. Inspect every non-merge
    # branch commit rather than only the final, potentially misleading title.
    subjects=sh("git","log","--no-merges","--format=%s",f"origin/{base_ref}..HEAD")
else:
    # On a two-parent merge push, inspect the complete introduced branch.
    # Otherwise the one direct push commit is the candidate being checked.
    parents=sh("git","rev-list","--parents","-n","1","HEAD").split()
    if len(parents)==3:
        subjects=sh("git","log","--no-merges","--format=%s","HEAD^1..HEAD^2")
    else:
        subjects=sh("git","log","-1","--format=%s")
commit_subjects=[line.strip() for line in subjects.splitlines() if line.strip()]
# A speculative earlier commit must never be laundered by a final commit
# whose title happens to start with [technical-fix].
technical_override=bool(commit_subjects) and all(
    line.startswith("[technical-fix]") for line in commit_subjects
)

# Allow the one-time introduction of a brand-new experiment and its initial page change.
# After merge, that experiment exists in the base data and its freeze is enforced.
base_ref=os.environ.get("GITHUB_BASE_REF","").strip()
base_spec=f"origin/{base_ref}:data/seo-experiments.json" if base_ref else "HEAD^:data/seo-experiments.json"
base_raw=sh("git","show",base_spec)
try:
    base_data=json.loads(base_raw) if base_raw else {"experiments":[]}
except Exception:
    base_data={"experiments":[]}
base_ids={e.get("id") for e in base_data.get("experiments",[]) if e.get("id")}
current_ids={e.get("id") for e in data.get("experiments",[]) if e.get("id")}
new_experiment_ids=current_ids-base_ids
if new_experiment_ids:
    print("NEW_EXPERIMENTS", ", ".join(sorted(new_experiment_ids)))

if changed:
    print("CHANGED_FILES", len(changed))
    for p in sorted(changed):
        print(" -",p)
if technical_override:
    print("::warning title=SEO experiment technical override::Protected-page change allowed because commit message starts with [technical-fix]. Verify that this is truly technical/factual/indexability/safety work and log the reason.")

integrity_errors=[]
seen_ids=set()
for e in data.get("experiments",[]):
    if e.get("status")!="running":
        continue
    exp_id=e.get("id")
    if not exp_id:
        integrity_errors.append("running experiment missing id")
        continue
    if exp_id in seen_ids:
        integrity_errors.append(f"{exp_id}: duplicate running experiment id")
    seen_ids.add(exp_id)
    last_changed=e.get("lastChanged")
    gate=e.get("evaluateNotBefore")
    if not last_changed:
        integrity_errors.append(f"{exp_id}: missing lastChanged")
    if not gate:
        integrity_errors.append(f"{exp_id}: missing evaluateNotBefore")
    if last_changed and gate:
        try:
            last_date=date.fromisoformat(last_changed)
            gate_date=date.fromisoformat(gate)
            if gate_date < last_date + timedelta(days=7):
                integrity_errors.append(
                    f"{exp_id}: evaluateNotBefore {gate} is less than 7 days after lastChanged {last_changed}"
                )
        except ValueError as exc:
            integrity_errors.append(f"{exp_id}: invalid experiment date: {exc}")

if integrity_errors:
    print("\nSEO_EXPERIMENT_REGISTRY_INTEGRITY_ERROR")
    for item in integrity_errors:
        print("-",item)
    sys.exit(1)

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
                if e["id"] in new_experiment_ids:
                    print(f"::notice title=SEO experiment initial setup::{e['id']} — initial protected-page change is allowed in the same change set that creates the experiment. Future edits are frozen until {gate}.")
                else:
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
