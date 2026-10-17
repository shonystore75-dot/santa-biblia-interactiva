#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regla de modernización: "enjullo" (el rodillo del telar donde se enrolla
la tela tejida) -> "rodillo".

Es un sentido único y uniforme en todas las apariciones: siempre es la
misma comparación formulaica ("el asta de su lanza era como un enjullo
de tejedor/tejedores/telar") usada para describir el grosor de una lanza
gigantesca, repetida en pasajes paralelos de Samuel y Crónicas. Se corrige
en las cuatro veces que aparece en todo el texto.
"""

import json

CAMBIOS = [
    ("libro-1s.json", 17, 7, "El asta de su lanza era como un enjullo de telar, y tenía el hierro de su lanza seiscientos siclos de hierro; e iba su escudero delante de él.",
                        "El asta de su lanza era como un rodillo de telar, y tenía el hierro de su lanza seiscientos siclos de hierro; e iba su escudero delante de él."),

    ("libro-1cr.json", 11, 23, "El mismo venció a un egipcio, hombre de cinco codos de estatura; y el egipcio traía una lanza como un enjullo de tejedor; mas él descendió a él con un bastón, y arrebató al egipcio la lanza de la mano, y lo mató con su misma lanza.",
                          "El mismo venció a un egipcio, hombre de cinco codos de estatura; y el egipcio traía una lanza como un rodillo de tejedor; mas él descendió a él con un bastón, y arrebató al egipcio la lanza de la mano, y lo mató con su misma lanza."),
    ("libro-1cr.json", 20, 5, "Y se volvió a levantar guerra con los filisteos; e hirió Elhanán hijo de Jair a Lahmi, hermano de Goliat Geteo, el asta de cuya lanza era como un enjullo de tejedores.",
                         "Y se volvió a levantar guerra con los filisteos; e hirió Elhanán hijo de Jair a Lahmi, hermano de Goliat Geteo, el asta de cuya lanza era como un rodillo de tejedores."),

    ("libro-2s.json", 21, 19, "Otra guerra hubo en Gob contra los filisteos, en la cual Elhanan, hijo de Jaare-oregim de Belén, hirió a Goliat Geteo, el asta de cuya lanza era como un enjullo de telar.",
                         "Otra guerra hubo en Gob contra los filisteos, en la cual Elhanan, hijo de Jaare-oregim de Belén, hirió a Goliat Geteo, el asta de cuya lanza era como un rodillo de telar."),
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
