#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regla de modernización: "almete" (yelmo/casco de guerra) -> "casco".

Es un sentido único y uniforme en todas las apariciones (siempre se refiere
a la pieza de armadura que cubre la cabeza), así que se corrige en las
cuatro veces que aparece en todo el texto, no solo en 1 Samuel 17.
"""

import json

CAMBIOS = [
    ("libro-1s.json", 17, 5, "Y traía un almete de acero en su cabeza, e iba vestido con corazas de planchas; y era el peso de la coraza cinco mil siclos de metal;",
                        "Y traía un casco de acero en su cabeza, e iba vestido con corazas de planchas; y era el peso de la coraza cinco mil siclos de metal;"),
    ("libro-1s.json", 17, 38, "Y Saúl vistió a David de sus ropas, y puso sobre su cabeza un almete de acero, y le armó de coraza.",
                         "Y Saúl vistió a David de sus ropas, y puso sobre su cabeza un casco de acero, y le armó de coraza."),

    ("libro-2cr.json", 26, 14, "Y les aprestó Uzzías para todo el ejército, escudos, lanzas, almetes, coseletes, arcos, y hondas de tirar piedras.",
                          "Y les aprestó Uzzías para todo el ejército, escudos, lanzas, cascos, coseletes, arcos, y hondas de tirar piedras."),

    ("libro-ez.json", 38, 5, "Persia, Etiopía, y Libia con ellos; todos ellos con escudos y almetes;",
                        "Persia, Etiopía, y Libia con ellos; todos ellos con escudos y cascos;"),
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
