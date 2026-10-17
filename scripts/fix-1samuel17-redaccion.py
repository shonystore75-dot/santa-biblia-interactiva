#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correcciones puntuales de redacción en 1 Samuel 17 (historia de David y
Goliat), a diferencia de los otros scripts de esta carpeta, estas NO se
aplican en el resto de la Biblia, porque los giros que corrigen ("el un...
de la una parte", "de con", "conturbar") son parte del estilo general de
esta traducción de 1909 y aparecen cientos de veces en otros libros;
cambiarlos ahí sería un proyecto aparte, mucho más grande. Aquí solo se
arregla este capítulo puntual, donde Diego reportó que se leían mal o no
se entendían.
"""

import json

CAMBIOS = [
    ("libro-1s.json", 17, 3, "Y los filisteos estaban sobre el un monte de la una parte, e Israel estaba sobre el otro monte de la otra parte, y el valle entre ellos;",
                        "Y los filisteos estaban sobre un monte de una parte, e Israel estaba sobre el otro monte de la otra parte, y el valle entre ellos;"),
    ("libro-1s.json", 17, 11, "Y oyendo Saúl y todo Israel estas palabras del Filisteo, se conturbaron, y tuvieron gran miedo.",
                         "Y oyendo Saúl y todo Israel estas palabras del Filisteo, se turbaron, y tuvieron gran miedo."),
    ("libro-1s.json", 17, 15, "Pero David había ido y vuelto de con Saúl, para apacentar las ovejas de su padre en Belén.",
                         "Pero David había ido y vuelto de estar con Saúl, para apacentar las ovejas de su padre en Belén."),
    ("libro-1s.json", 17, 18, "Llevarás asimismo estos diez quesos de leche al capitán, y cuida de ver si tus hermanos están buenos, y toma prendas de ellos.",
                         "Llevarás asimismo estos diez quesos de leche al capitán, y cuida de ver si tus hermanos están bien, y toma prendas de ellos."),
    ("libro-1s.json", 17, 20, "Se levantó pues David de mañana, y dejando las ovejas al cuidado de un guarda, se fue con su carga, como Isaí le había mandado; y llegó al atrincheramiento del ejército, el cual había salido en ordenanza, y tocaba alarma para la pelea.",
                         "Se levantó pues David de mañana, y dejando las ovejas al cuidado de un guarda, se fue con su carga, como Isaí le había mandado; y llegó al campamento del ejército, el cual había salido en orden de batalla, y tocaba alarma para la pelea."),
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
