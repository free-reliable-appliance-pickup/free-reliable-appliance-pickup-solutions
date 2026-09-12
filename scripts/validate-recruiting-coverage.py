from pathlib import Path
import json, re, sys

routing=json.loads(Path('data/market-routing.json').read_text(encoding='utf-8'))
recruiting_regions={str(r.get('region','')).strip().lower() for r in routing.get('markets',[]) if r.get('status')=='partner-recruiting'}
recruiting_states={str(r.get('state_code','')).upper() for r in routing.get('state_defaults',[]) if r.get('status')=='partner-recruiting'}
state_names={'arizona':'AZ','california':'CA','florida':'FL','idaho':'ID','nevada':'NV','oregon':'OR','texas':'TX','utah':'UT','washington':'WA'}

safe_terms=('request','review','availability','coverage','confirm','confirmed','partner','not guaranteed','qualification','qualifying','subject to','recruit')
risky=(r'\bwe serve\b',r'\bwe service\b',r'\bfree pickup throughout\b',r'\bfree pickup across\b',r'\bavailable throughout\b',r'\bavailable across\b')
errors=[]
checked=0


def visible_text(html):
    html=re.sub(r'<script\b[^>]*>.*?</script>',' ',html,flags=re.I|re.S)
    html=re.sub(r'<style\b[^>]*>.*?</style>',' ',html,flags=re.I|re.S)
    html=re.sub(r'<[^>]+>',' ',html)
    return re.sub(r'\s+',' ',html).strip().lower()


def jsonld_blocks(html):
    return re.findall(r'<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',html,re.I|re.S)


for p in Path('.').glob('*-appliance-pickup/index.html'):
    rel=p.parent.name
    root=rel[:-len('-appliance-pickup')]
    is_recruiting=(root in state_names and state_names[root] in recruiting_states) or (root.replace('-',' ') in recruiting_regions)
    if not is_recruiting:
        continue

    checked+=1
    raw=p.read_text(encoding='utf-8',errors='ignore')
    low=raw.lower()
    if 'noindex' in low:
        continue

    text=visible_text(raw)
    lead=text[:1800]

    # A recruiting page must qualify coverage in the main visible copy, not only
    # somewhere deep in the footer or hidden metadata.
    if not any(t in lead for t in safe_terms):
        errors.append(f'MISSING LEAD QUALIFIER {p}')

    # Risky service claims must be qualified close to the claim itself.
    for pat in risky:
        for m in re.finditer(pat,text):
            window=text[max(0,m.start()-180):m.end()+260]
            if not any(t in window for t in ('subject to','confirm','confirmed','availability','coverage','request','review','not guaranteed','qualifying')):
                errors.append(f'OVERPROMISE {p}: {pat}')

    # If a recruiting page publishes Service structured data, serviceType should
    # describe request/review/qualification rather than imply unconditional service.
    for block in jsonld_blocks(raw):
        try:
            data=json.loads(block)
        except Exception:
            continue
        nodes=[]
        if isinstance(data,dict):
            nodes.extend(data.get('@graph',[]) if isinstance(data.get('@graph'),list) else [])
            nodes.append(data)
        for node in nodes:
            if not isinstance(node,dict) or node.get('@type')!='Service':
                continue
            service_type=node.get('serviceType','')
            if isinstance(service_type,list):
                service_type=' '.join(map(str,service_type))
            st=str(service_type).lower()
            if st and not any(t in st for t in ('request','review','qualif')):
                errors.append(f'UNQUALIFIED SERVICE STRUCTURED DATA {p}: {service_type}')

print(f'Checked {checked} recruiting hub pages')
if errors:
    print('\n'.join(sorted(set(errors))))
    sys.exit(1)
print('PASS: recruiting hub coverage language and Service structured data are qualified')
