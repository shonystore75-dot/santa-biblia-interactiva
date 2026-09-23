# -*- coding: utf-8 -*-
import json, sys
sys.path.insert(0, '.')
from modernizar import modernizar_verso

for libro in ['esd', 'est', 'neh']:
    with open(f'libro-{libro}.json', encoding='utf-8') as f:
        data = json.load(f)
    for cap in data:
        c = cap['c']
        for i, (vnum, texto) in enumerate(cap['v']):
            nuevo = modernizar_verso(libro, c, vnum, texto, primer_verso=(i == 0))
            cap['v'][i] = [vnum, nuevo]
    with open(f'libro-{libro}-nuevo.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(libro, 'procesado')
