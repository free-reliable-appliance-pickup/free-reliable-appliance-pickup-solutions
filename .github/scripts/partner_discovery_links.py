from pathlib import Path
import re

# Pages that should prominently expose the legitimate partner network.
targets = [
    Path("index.html"),
    Path("service-areas/index.html"),
    Path("about/index.html"),
    Path("contact/index.html"),
    Path("landlord-property-manager-appliance-pickup/index.html"),
]

for p in targets:
    if not p.exists():
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    href = "partners/" if p == Path("index.html") else "../partners/"
    if f'href="{href}"' in text:
        continue
    block = f'''\n<p class="partner-network-link"><a href="{href}">Appliance Pickup Partner Program</a> — Local appliance pickup operators, repair/refurbishment businesses, recyclers, haulers and resellers can apply for reviewed service-area opportunities.</p>\n'''
    if "</footer>" in text:
        text = text.replace("</footer>", block + "</footer>", 1)
    elif "</main>" in text:
        text = text.replace("</main>", block + "</main>", 1)
    p.write_text(text, encoding="utf-8")

# Also connect every currently indexable local/state/service page from its footer,
# but never force this onto noindex/legal pages or the partners page itself.
for p in Path(".").rglob("index.html"):
    if p in targets or p == Path("partners/index.html") or ".github" in p.parts:
        continue
    text = p.read_text(encoding="utf-8", errors="ignore")
    robot = re.search(r'<meta\b[^>]*\bname=["\']robots["\'][^>]*>', text, flags=re.I)
    if robot and "noindex" in robot.group(0).lower():
        continue
    if 'href="../partners/"' in text or "</footer>" not in text:
        continue
    link = '\n<p><a href="../partners/">Partner Program</a></p>\n'
    text = text.replace("</footer>", link + "</footer>", 1)
    p.write_text(text, encoding="utf-8")
