#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regla de modernización: "harto(s)/harta(s)" cuando significa "lleno,
satisfecho" (sin un "de algo malo" que lo aclare) -> "saciado(s)/saciada(s)"
o el verbo "saciar" correspondiente.

NO toca el resto de la familia "harto/hartar" (más de 75 versículos),
porque:
  - "hartarse" de comer/beber (quedar lleno de comida) sigue siendo español
    moderno normal ("comieron y se hartaron").
  - "harto de [algo malo]" (menosprecio, holocaustos, males, deshonra,
    sinsabores, etc.) ya se entiende hoy como "fastidiado/cansado de algo",
    que es justamente el sentido original.

Estos 13 versículos son los únicos donde "harto(s)/harta(s)" describe a
alguien "lleno/satisfecho" sin esa aclaración, con riesgo real de leerse
hoy como "fastidiado" (incluidas las Bienaventuranzas de Mateo 5:6 y Lucas 6:25).
"""

import json

CAMBIOS = [
    ("libro-1co.json", 4, 8, "Ya estáis hartos, ya estáis ricos", "Ya estáis saciados, ya estáis ricos"),
    ("libro-mt.json", 5, 6, "porque ellos serán hartos.", "porque ellos serán saciados."),
    ("libro-lc.json", 6, 25, "los que estáis hartos! porque tendréis hambre.", "los que estáis saciados! porque tendréis hambre."),
    ("libro-sal.json", 37, 19, "y en los días de hambre serán hartos.", "y en los días de hambre serán saciados."),
    ("libro-jer.json", 50, 10, "todos los que la saquearen, saldrán hartos, dice Jehová.", "todos los que la saquearen, saldrán saciados, dice Jehová."),
    ("libro-jer.json", 5, 8, "Como caballos bien hartos fueron a la mañana", "Como caballos bien alimentados fueron a la mañana"),
    ("libro-jer.json", 44, 17, "y fuimos hartos de pan, y estuvimos alegres", "y nos saciamos de pan, y estuvimos alegres"),
    ("libro-pr.json", 12, 14, "El hombre será harto de bien del fruto de su boca", "El hombre será saciado de bien del fruto de su boca"),
    ("libro-pr.json", 27, 7, "El alma harta huella el panal de miel", "El alma saciada huella el panal de miel"),
    ("libro-sal.json", 104, 28, "abres tu mano, se hartan de bien.", "abres tu mano, se sacian de bien."),
    ("libro-sal.json", 17, 14, "hartan sus hijos, y dejan el resto a sus chiquitos.", "sacian a sus hijos, y dejan el resto a sus chiquitos."),
    ("libro-is.json", 58, 11, "y en las sequías hartará tu alma", "y en las sequías saciará tu alma"),
    ("libro-is.json", 55, 10, "sino que harta la tierra, y la hace germinar y producir", "sino que sacia la tierra, y la hace germinar y producir"),
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
