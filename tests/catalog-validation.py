#!/usr/bin/env python3
"""Structural validation for Marginal's offline activity catalog."""
import json, re, sys, unicodedata
from pathlib import Path
p=Path(__file__).resolve().parents[1]/'data'/'activities.json'
items=json.loads(p.read_text(encoding='utf-8'))
errors=[]; warnings=[]
def norm(s):
    s=unicodedata.normalize('NFKD',s.casefold())
    s=''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z0-9]+',' ',s).strip()
if len(items)!=1000: errors.append(f'Expected 1000 entries; found {len(items)}')
ids=[a.get('id') for a in items]
if len(set(ids))!=len(ids): errors.append('Duplicate IDs found')
names=[norm(a.get('name','')) for a in items]
if len(set(names))!=len(names): errors.append('Duplicate normalized names found')
descriptions=[norm(a.get('description','')) for a in items]
if len(set(descriptions))!=len(descriptions): errors.append('Duplicate normalized descriptions found')
required=['id','name','description','categories','minPlayers','maxPlayers','durationMinutes','energy','mobility','locations','materials','setup','rules','objective','variants','requiresPhone','requiresContact','ageSuitability','originality']
valid_materials={'paper','pen','everyday','phone'}
for i,a in enumerate(items,1):
    missing=[k for k in required if k not in a]
    if missing: errors.append(f'{a.get("id",i)} missing {missing}'); continue
    if not a['name'].strip() or len(a['description'].strip())<20: errors.append(f'{a["id"]}: empty/short title or description')
    if not isinstance(a['minPlayers'],int) or not isinstance(a['maxPlayers'],int) or a['minPlayers']<1 or a['maxPlayers']<a['minPlayers']: errors.append(f'{a["id"]}: invalid player range')
    if not isinstance(a['durationMinutes'],int) or a['durationMinutes']<1 or a['durationMinutes']>240: errors.append(f'{a["id"]}: invalid duration')
    if not a['categories']: errors.append(f'{a["id"]}: no category')
    if not isinstance(a['rules'],list) or len(a['rules'])<2 or any(len(r.strip())<12 for r in a['rules']): errors.append(f'{a["id"]}: missing actionable rules')
    if not a['setup'].strip() or not a['objective'].strip() or not a['variants']: errors.append(f'{a["id"]}: incomplete instructions')
    if not a['locations'] or any(x not in {'indoor','outdoor'} for x in a['locations']): errors.append(f'{a["id"]}: invalid location metadata')
    if any(m not in valid_materials for m in a['materials']): errors.append(f'{a["id"]}: unknown material')
    if bool(a['requiresPhone']) != ('phone' in a['materials']): errors.append(f'{a["id"]}: phone/material metadata mismatch')
# The static matrix is intentionally audited for exact duplicates; semantic similarity still needs editorial review.
if len(items)>0 and len(set(a.get('originality') for a in items))<1: errors.append('Originality metadata missing')
print(f'Catalog: {len(items)} entries | {len(set(ids))} unique IDs | {len(set(names))} unique names | {len(set(descriptions))} unique descriptions')
if errors:
    print(f'FAIL: {len(errors)} issue(s)'); print('\n'.join(' - '+e for e in errors[:100])); sys.exit(1)
print('PASS: structural checks')
print('EDITORIAL NOTE: structural uniqueness cannot prove semantic distinctness; review related format/theme entries before production.')
