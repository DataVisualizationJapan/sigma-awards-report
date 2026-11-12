"""stats.json を template.html に埋め込み、index.html を生成する。"""
import json, os
here = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(here, 'stats.json'), encoding='utf-8'))
t = open(os.path.join(here, 'template.html'), encoding='utf-8').read()
js = json.dumps(d, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
open(os.path.join(here, 'index.html'), 'w', encoding='utf-8').write(t.replace('__DATA__', js))
print('index.html written')
