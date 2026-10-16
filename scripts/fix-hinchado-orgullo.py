#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regla de modernización: "hinchado(s)/hincha" en sentido figurado de
orgullo/soberbia (distinto del "henchir" = llenar ya corregido aparte, y
distinto de "hinchazón"/"hinchar(se)" = hinchazón física, que no se tocan).

7 versículos, todos en cartas paulinas.
"""

import json

CAMBIOS = [
    ("libro-1co.json", 4, 6, "hinchándoos por causa de otro el uno contra el otro.", "envaneciéndoos por causa de otro el uno contra el otro."),
    ("libro-1co.json", 4, 19, "los que andan hinchados, sino la virtud.", "los que andan envanecidos, sino la virtud."),
    ("libro-1co.json", 5, 2, "Y vosotros estáis hinchados, y no más bien tuvisteis duelo", "Y vosotros estáis envanecidos, y no más bien tuvisteis duelo"),
    ("libro-1co.json", 8, 1, "La ciencia hincha, mas la caridad edifica.", "La ciencia envanece, mas la caridad edifica."),

    ("libro-1ti.json", 6, 4, "Es hinchado, nada sabe", "Es soberbio, nada sabe"),

    ("libro-2ti.json", 3, 4, "Traidores, arrebatados, hinchados, amadores de los deleites más que de Dios;", "Traidores, arrebatados, soberbios, amadores de los deleites más que de Dios;"),

    ("libro-col.json", 2, 18, "vanamente hinchado en el sentido de su propia carne,", "vanamente orgulloso en el sentido de su propia carne,"),
]

def main():
    applied = 0
    errors = []
    by_file = {}
    for fname, c, v, old, new in CAMBIOS:
        by_file.setdefault(fname, []).append((c, v, old, new))

    for fname, entries in by_file.items():
        with open(fname, encoding="utf-8") as fh:
            raw = fh.read()
        data = json.loads(raw)
        for c, v, old, new in entries:
            chapter = next((ch for ch in data if ch["c"] == c), None)
            if chapter is None:
                errors.append(f"{fname} {c}:{v} - capítulo no encontrado")
                continue
            verse_entry = next((ve for ve in chapter["v"] if ve[0] == v), None)
            if verse_entry is None:
                errors.append(f"{fname} {c}:{v} - versículo no encontrado")
                continue
            verse_text = verse_entry[1]
            if old not in verse_text:
                errors.append(f"{fname} {c}:{v} - texto viejo no encontrado en el versículo: {old!r}")
                continue
            if verse_text.count(old) != 1:
                errors.append(f"{fname} {c}:{v} - texto viejo aparece más de una vez en el versículo: {old!r}")
                continue
            count_raw = raw.count(old)
            if count_raw != 1:
                errors.append(f"{fname} {c}:{v} - texto viejo aparece {count_raw} veces en todo el archivo (esperado 1): {old!r}")
                continue
            raw = raw.replace(old, new)
            applied += 1
        with open(fname, "w", encoding="utf-8") as fh:
            fh.write(raw)

    print(f"Cambios aplicados: {applied} de {len(CAMBIOS)}")
    if errors:
        print("ERRORES:")
        for e in errors:
            print(" -", e)
    else:
        print("Sin errores.")

if __name__ == "__main__":
    main()
