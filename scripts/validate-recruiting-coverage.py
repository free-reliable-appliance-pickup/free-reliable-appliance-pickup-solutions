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
for p in Path('.').glob('*-appliance-pickup/index.html'):
    rel=p.parent.name
    root=rel[:-len('-appliance-pickup')]
    is_recruiting=(root in state_names and state_names[root] in recruiting_states) or (root.replace('-',' ') in recruiting_regions)
    if not is_recruiting:
        continue
    checked+=1
    low=p.read_text(encoding='utf-8',errors='ignore').lower()
    if 'noindex' in low:
        continue
    if not any(t in low for t in safe_terms):
        errors.append(f'MISSING QUALIFIER {p}')
    for pat in risky:
        if re.search(pat,low) and not any(t in low for t in ('subject to','confirm','confirmed','availability','not guaranteed')):
            errors.append(f'OVERPROMISE {p}: {pat}')

print(f'Checked {checked} recruiting hub pages')
if errors:
    print('\n'.join(errors))
    sys.exit(1)
print('PASS: recruiting hub coverage language is qualified')
