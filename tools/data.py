import json, re, subprocess, os
import sys
R=(sys.argv[1] if len(sys.argv)>1 else '/tmp/cka').rstrip('/')+'/'
def load(n):
    d=json.load(open(R+'assets/static_data/'+n+'.json')); return d.get('items', d) if isinstance(d, dict) else d
bth={}
for b in load('buildings'):
    if b['name'] in ('Barracks','Dark Barracks','Spell Factory','Dark Spell Factory','Workshop'):
        bth[b['name']]={l['level']:l['required_townhall'] for l in b['levels']}
def slug(s): return re.sub(r'[^a-z0-9]+','_',s.lower().replace("'",'')).strip('_')
items=[]; paths=[]
troops=[t for t in load('troops') if t.get('village')=='home' and not t.get('is_seasonal')]
byid={t['_id']:t for t in troops}
def th_of(t): return bth[t['production_building']][t['production_building_level']]
for t in troops:
    nm=t['name']; s=slug(nm).replace('p_e_k_k_a','pekka')
    p=f'assets/troops/{s}/icon.webp'; paths.append(p)
    if t['production_building']=='Workshop': c='siege'; th=th_of(t)
    elif t.get('super_troop'):
        c='super'; base=byid[t['super_troop']['original_id']]; th=max(11, th_of(base))
    else: c='troop'; th=th_of(t)
    items.append({'id':s,'n':nm,'c':c,'th':th,'hs':t['housing_space'] if c!='siege' else None,'fly':t['is_flying'],'img':f'icons/{s}.webp','src':p})
for sp in load('spells'):
    if sp.get('is_seasonal'): continue
    s=slug(sp['name']); p=f'assets/spells/{s}.webp'; paths.append(p)
    items.append({'id':s,'n':sp['name'].replace(' Spell',''),'c':'spell','th':bth[sp['production_building']][sp['production_building_level']],'hs':sp['housing_space'],'img':f'icons/{s}.webp','src':p})
HC={'Barbarian King':'BK','Archer Queen':'AQ','Grand Warden':'GW','Royal Champion':'RC','Minion Prince':'MP','Dragon Duke':'DD'}
HTH={'BK':7,'AQ':8,'MP':9,'GW':11,'RC':13,'DD':15}
for e in list(json.load(open(R+'assets/static_data/equipment.json')).values())[0]:
    if e['rarity']!='Epic': continue
    s=slug(e['name']); p=f'assets/equipment/{s}.webp'; paths.append(p); h=HC[e['hero']]
    items.append({'id':s,'n':e['name'],'c':'epic','h':h,'th':HTH[h],'img':f'icons/{s}.webp','src':p})
heroes={}
for name,code in HC.items():
    p=f'assets/heroes/{slug(name)}/icon.webp'; paths.append(p); heroes[code]={'n':name,'img':f'icons/hero_{code}.webp','src':p,'th':HTH[code]}
subprocess.run(['git','-C',R,'checkout','HEAD','--']+paths,check=True)
import shutil
for it in items: shutil.copy(R+it['src'],'icons/'+it['img'].split('/')[1])
for h in heroes.values(): shutil.copy(R+h['src'],'icons/'+h['img'].split('/')[1])
for it in items: it.pop('src')
for h in heroes.values(): h.pop('src')
json.dump({'items':items,'heroes':heroes},open('data.json','w'),separators=(',',':'))
from collections import Counter
print(Counter(i['c'] for i in items)); print(sorted((i['th'],i['n']) for i in items if i['th']>=15))
