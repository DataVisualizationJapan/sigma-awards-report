import json, collections, sys, os, re, math
R = sys.argv[1]; OUT = sys.argv[2]
C = collections.Counter
E = json.load(open(os.path.join(R, 'public/data/entries.json')))
meta = {k: v for k, v in E.items() if k != 'entries'}; E = E['entries']
det = {}
for y in range(2020, 2027): det.update(json.load(open(os.path.join(R, f'public/data/details-{y}.json'))))
YEARS = list(range(2020, 2027))
for e in E:
    d = det.get(e['id'], {})
    e['size'] = d.get('size') or ''
    e['rec'] = e['result'] != 'entry'          # shortlist or better
    e['win'] = e['result'] in ('winner',)
    tl = [t.strip() for t in re.split(r'[,;\n]', d.get('tools') or '') if t.strip()]
    TM = {'Adobe': 'Adobe Creative Suite', 'Creative Suite': 'Adobe Creative Suite', '3D modelling': '3D modeling', 'RStudio': 'R'}
    e['tools'] = sorted(set(TM.get(t, t) for t in tl))
    GM = {'Quiz': 'Quiz / game', 'game': 'Quiz / game', 'Podcast': 'Podcast / radio', 'radio': 'Podcast / radio'}
    e['tags'] = sorted(set(GM.get(t.strip(), t.strip()) for t in e['tags']))
rate_y = {y: sum(e['rec'] for e in E if e['year'] == y) / sum(1 for e in E if e['year'] == y) for y in YEARS}
def sir(sub):
    O = sum(e['rec'] for e in sub); Ex = sum(rate_y[e['year']] for e in sub)
    lo = max(0, O - 1.96 * math.sqrt(O)) / Ex if Ex else 0; hi = (O + 1.96 * math.sqrt(O)) / Ex if Ex else 0
    return dict(n=len(sub), rec=O, win=sum(e['win'] for e in sub), exp=round(Ex, 1), ratio=round(O / Ex, 2) if Ex else None, lo=round(lo, 2), hi=round(hi, 2))
res = {'meta': meta}
res['years'] = [dict(year=y, n=sum(1 for e in E if e['year'] == y), rec=sum(e['rec'] for e in E if e['year'] == y), win=sum(e['win'] for e in E if e['year'] == y),
                     mention=sum(e['result'] == 'mention' for e in E if e['year'] == y), countries=len(set(e['country'] for e in E if e['year'] == y)),
                     portfolio=sum(e['kind'] == 'portfolio' for e in E if e['year'] == y), small=sum(e['size'] == 'Small' for e in E if e['year'] == y)) for y in YEARS]
res['total'] = dict(n=len(E), rec=sum(e['rec'] for e in E), win=sum(e['win'] for e in E), countries=len(set(e['country'] for e in E)))
res['size'] = {s: sir([e for e in E if e['size'] == s]) for s in ('Big', 'Small')}
res['kind'] = {s: sir([e for e in E if e['kind'] == s]) for s in ('project', 'portfolio')}
cc = C(e['country'] for e in E)
res['countries'] = [dict(name=c, **sir([e for e in E if e['country'] == c])) for c, n in cc.most_common() if n >= 40 or c in ('Japan', 'Korea, Republic of', 'Hong Kong S.A.R., China')]
res['win_countries'] = C(e['country'] for e in E if e['win']).most_common(15)
tg = C(t.strip() for e in E for t in e['tags'])
def canon(t): return t.strip()
res['tags'] = []
for t, n in tg.most_common():
    if n < 80: continue
    sub = [e for e in E if t in [x.strip() for x in e['tags']]]
    by = {y: round(100 * sum(1 for e in sub if e['year'] == y) / sum(1 for e in E if e['year'] == y), 1) for y in YEARS}
    res['tags'].append(dict(name=t, share=by, **sir(sub)))
tl = C(t for e in E for t in set(e['tools']))
res['tools'] = []
for t, n in tl.most_common(60):
    if n < 60: continue
    sub = [e for e in E if t in e['tools']]
    by = {y: round(100 * sum(1 for e in sub if e['year'] == y) / sum(1 for e in E if e['year'] == y), 1) for y in YEARS}
    res['tools'].append(dict(name=t, share=by, **sir(sub)))
ntags = [len(e['tags']) for e in E]
jp = [e for e in E if e['country'] == 'Japan']
res['japan'] = dict(stats=sir(jp), by_year={y: dict(n=sum(1 for e in jp if e['year'] == y), rec=sum(e['rec'] for e in jp if e['year'] == y)) for y in YEARS},
                    entries=[dict(id=e['id'], year=e['year'], title=e['title'], titleJa=e.get('titleJa') or '', org=e['org'], result=e['result'], kind=e['kind'], tags=e['tags']) for e in sorted(jp, key=lambda e: (e['year'], e['id']))])
res['winners'] = [dict(id=e['id'], year=e['year'], title=e['title'], titleJa=e.get('titleJa') or '', org=e['org'], country=e['country'], label=e['resultLabel'], kind=e['kind'], size=e['size'], tags=e['tags'], tools=e['tools'][:12]) for e in E if e['result'] in ('winner', 'mention')]
D = json.load(open(os.path.join(R, 'public/data/dja/entries.json')))
DE = D['entries']
res['dja'] = dict(count=D['count'], years=[dict(year=y, winner=sum(1 for e in DE if e['year'] == y and e['result'] == 'winner'), mention=sum(1 for e in DE if e['year'] == y and e['result'] == 'mention'), shortlist=sum(1 for e in DE if e['year'] == y and e['result'] == 'shortlist')) for y in range(2012, 2020)],
                  win_countries=C((e['country'] or '不明') for e in DE if e['result'] == 'winner').most_common(12),
                  japan=[dict(id=e['id'], year=e['year'], title=e['title'], org=e['org'], result=e['result']) for e in DE if e['country'] == 'Japan'])
allshare = {t['name']: t['n'] / len(E) for t in res['tags']}
res['japan']['tagprofile'] = sorted([dict(name=t, jp=round(100 * sum(1 for e in jp if t in e['tags']) / len(jp), 1), all=round(100 * a, 1)) for t, a in allshare.items()], key=lambda r: -(r['jp'] - r['all']))
res['rate_y'] = {y: round(100 * r, 1) for y, r in rate_y.items()}
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
p = print
p('rate_y', {y: round(100 * r, 1) for y, r in rate_y.items()}); p('total', res['total'])
p('size', res['size']); p('kind', res['kind'])
p('countries'); [p('  ', c['name'][:22].ljust(22), c['n'], c['rec'], c['win'], c['ratio'], (c['lo'], c['hi'])) for c in res['countries']]
p('win_countries', res['win_countries'])
p('tags by ratio'); [p('  ', t['name'][:30].ljust(30), t['n'], t['rec'], t['win'], t['ratio'], (t['lo'], t['hi']), t['share'][2020], t['share'][2023], t['share'][2026]) for t in sorted(res['tags'], key=lambda t: -t['ratio'])]
p('tools by ratio'); [p('  ', t['name'][:26].ljust(26), t['n'], t['rec'], t['win'], t['ratio'], (t['lo'], t['hi']), t['share'][2020], t['share'][2023], t['share'][2026]) for t in sorted(res['tools'], key=lambda t: -t['ratio'])]
p('japan', res['japan']['stats'], res['japan']['by_year'])
p('dja win countries', res['dja']['win_countries'])
