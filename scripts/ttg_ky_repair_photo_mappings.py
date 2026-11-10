#!/usr/bin/env python3
"""Replace historically misclassified specialty photos on KY drafted pages only."""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
IMAGE_OPTIONS={
 "refrigerator":[("/IMG-20240701-WA0026.jpg",1200,1600),
                 ("/assets/rancho-cucamonga/rancho-cucamonga-refrigerator-real-french-door-20261016.jpg",960,720)],
 "freezer":[("/IMG-20240916-WA0063.jpg",1200,1600)],
 "stove-oven":[("/IMG-20240920-WA0084.jpg",1536,2048),
              ("/assets/california/real-appliances/fontana-stove-range-hero.jpg",960,720)]
}
total=0
for kind,choices in IMAGE_OPTIONS.items():
    paths=sorted(ROOT.glob(f"*-ky-{kind}-pickup/index.html"))
    if len(paths)!=50:raise RuntimeError(f"Expected 50 {kind} Kentucky pages, got {len(paths)}")
    for index,path in enumerate(paths):
        src,w,h=choices[index%len(choices)]
        if not (ROOT/src.lstrip("/")).is_file():
            raise RuntimeError("Missing verified photo: "+src)
        original=path.read_text(encoding="utf-8")
        expr=r'(<figure><img src=")[^"]+(" alt="[^"]+" width=")[0-9]+(" height=")[0-9]+(" loading="eager")'
        repl=lambda m:m.group(1)+src+m.group(2)+str(w)+m.group(3)+str(h)+m.group(4)
        updated,n=re.subn(expr,repl,original)
        if n!=1:raise RuntimeError(f"Could not replace one specialty photo in {path}")
        if 'noindex, follow' not in updated or 'formspree.io/f/mvzeapzd' not in updated:
            raise RuntimeError(f"Unverified coverage or form unexpectedly changed in {path}")
        path.write_text(updated,encoding="utf-8")
        total+=1
print(f"PASS: {total} KY refrigerator/freezer/stove pages now use verified actual category photos, with correct dimensions.")
