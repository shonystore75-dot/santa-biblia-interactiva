#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regla de modernización: "caridad" (cuando traduce el griego "ágape" = amor,
no el sentido moderno de "caridad" = dar limosna a los pobres) -> "amor".

Es un sentido único y uniforme en todas las apariciones (no hay mezcla de
sentidos como en "henchir" o "harto"): en ningún caso significa "limosna/
ayuda a los pobres". Además, esta misma Biblia ya usa "amor" para el mismo
concepto en otros libros (1 Juan 4:7-21, "Dios es amor"), así que "caridad"
es solo una palabra distinta para la misma idea, no un sentido aparte.

Incluye los ajustes de género gramatical necesarios (la caridad -> el amor;
adjetivos como "sufrida/benigna/nacida/perfecta" -> "sufrido/benigno/
nacido/perfecto") para que el texto quede bien formado, sobre todo en
1 Corintios 13 (el "capítulo del amor"), incluido el versículo 5, que no
tiene la palabra "caridad" pero continúa gramaticalmente la descripción del
versículo 4 ("No es injuriosa" -> "No es injurioso").
"""

import json

CAMBIOS = [
    ("libro-1co.json", 4, 21, "¿iré a vosotros con vara, o con caridad y espíritu de mansedumbre?", "¿iré a vosotros con vara, o con amor y espíritu de mansedumbre?"),
    ("libro-1co.json", 8, 1, "La ciencia envanece, mas la caridad edifica.", "La ciencia envanece, mas el amor edifica."),

    ("libro-1co.json", 13, 1, "y no tengo caridad, vengo a ser como metal que resuena, o címbalo que retiñe.", "y no tengo amor, vengo a ser como metal que resuena, o címbalo que retiñe."),
    ("libro-1co.json", 13, 2, "y no tengo caridad, nada soy.", "y no tengo amor, nada soy."),
    ("libro-1co.json", 13, 3, "y no tengo caridad, de nada me sirve.", "y no tengo amor, de nada me sirve."),
    ("libro-1co.json", 13, 4, "La caridad es sufrida, es benigna; la caridad no tiene envidia, la caridad no hace sinrazón, no se ensancha;",
                        "El amor es sufrido, es benigno; el amor no tiene envidia, el amor no hace sinrazón, no se ensancha;"),
    ("libro-1co.json", 13, 5, "No es injuriosa, no busca lo suyo, no se irrita, no piensa el mal;", "No es injurioso, no busca lo suyo, no se irrita, no piensa el mal;"),
    ("libro-1co.json", 13, 8, "La caridad nunca deja de ser;", "El amor nunca deja de ser;"),
    ("libro-1co.json", 13, 13, "Y ahora permanecen la fe, la esperanza, y la caridad, estas tres; pero la mayor de ellas es la caridad.",
                         "Y ahora permanecen la fe, la esperanza, y el amor, estas tres; pero la mayor de ellas es el amor."),

    ("libro-1co.json", 14, 1, "Seguid la caridad; y procurad los dones espirituales", "Seguid el amor; y procurad los dones espirituales"),
    ("libro-1co.json", 16, 14, "Todas vuestras cosas sean hechas con caridad.", "Todas vuestras cosas sean hechas con amor."),

    ("libro-1jn.json", 2, 5, "la caridad de Dios está verdaderamente perfecta en él", "el amor de Dios está verdaderamente perfecto en él"),

    ("libro-1p.json", 1, 22, "en caridad hermanable sin fingimiento", "en amor hermanable sin fingimiento"),
    ("libro-1p.json", 4, 8, "tened entre vosotros ferviente caridad; porque la caridad cubrirá multitud de pecados.", "tened entre vosotros ferviente amor; porque el amor cubrirá multitud de pecados."),
    ("libro-1p.json", 5, 14, "Saludaos unos a otros con ósculo de caridad.", "Saludaos unos a otros con ósculo de amor."),

    ("libro-1ti.json", 1, 5, "el fin del mandamiento es la caridad nacida de corazón limpio", "el fin del mandamiento es el amor nacido de corazón limpio"),
    ("libro-1ti.json", 2, 15, "si permanece en la fe y caridad y santidad", "si permanece en la fe y amor y santidad"),
    ("libro-1ti.json", 4, 12, "en conversación, en caridad, en espíritu, en fe, en limpieza.", "en conversación, en amor, en espíritu, en fe, en limpieza."),
    ("libro-1ti.json", 6, 11, "la justicia, la piedad, la fe, la caridad, la paciencia, la mansedumbre.", "la justicia, la piedad, la fe, el amor, la paciencia, la mansedumbre."),

    ("libro-1ts.json", 3, 6, "haciéndonos saber vuestra fe y caridad", "haciéndonos saber vuestra fe y amor"),
    ("libro-1ts.json", 4, 9, "Mas acerca de la caridad fraterna no habéis menester que os escriba", "Mas acerca del amor fraternal no habéis menester que os escriba"),
    ("libro-1ts.json", 5, 8, "vestidos de cota de fe y de caridad", "vestidos de cota de fe y de amor"),

    ("libro-2co.json", 8, 8, "la sinceridad también de la caridad vuestra.", "la sinceridad también del amor vuestro."),
    ("libro-2co.json", 13, 11, "y el Dios de paz y de caridad será con vosotros.", "y el Dios de paz y de amor será con vosotros."),

    ("libro-2ti.json", 2, 22, "sigue la justicia, la fe, la caridad, la paz", "sigue la justicia, la fe, el amor, la paz"),
    ("libro-2ti.json", 3, 10, "fe, largura de ánimo, caridad, paciencia,", "fe, largura de ánimo, amor, paciencia,"),

    ("libro-2ts.json", 1, 3, "la caridad de cada uno de todos vosotros abunda entre vosotros;", "el amor de cada uno de todos vosotros abunda entre vosotros;"),

    ("libro-ap.json", 2, 19, "Yo he conocido tus obras, y caridad, y servicio, y fe,", "Yo he conocido tus obras, y amor, y servicio, y fe,"),

    ("libro-col.json", 3, 14, "vestíos de caridad, la cual es el vínculo de la perfección.", "vestíos de amor, el cual es el vínculo de la perfección."),

    ("libro-flm.json", 1, 5, "Oyendo tu caridad, y la fe que tienes en el Señor Jesús", "Oyendo tu amor, y la fe que tienes en el Señor Jesús"),
    ("libro-flm.json", 1, 7, "tenemos gran gozo y consolación de tu caridad", "tenemos gran gozo y consolación de tu amor"),

    ("libro-gl.json", 5, 6, "sino la fe que obra por la caridad.", "sino la fe que obra por el amor."),
    ("libro-gl.json", 5, 22, "Mas el fruto del Espíritu es; caridad, gozo, paz, tolerancia, benignidad, bondad, fe,", "Mas el fruto del Espíritu es; amor, gozo, paz, tolerancia, benignidad, bondad, fe,"),

    ("libro-lc.json", 11, 42, "mas el juicio y la caridad de Dios pasáis de largo.", "mas el juicio y el amor de Dios pasáis de largo."),

    ("libro-mt.json", 24, 12, "la caridad de muchos se resfriará.", "el amor de muchos se resfriará."),

    ("libro-pr.json", 10, 12, "mas la caridad cubrirá todas las faltas.", "mas el amor cubrirá todas las faltas."),

    ("libro-ro.json", 5, 8, "Mas Dios encarece su caridad para con nosotros", "Mas Dios encarece su amor para con nosotros"),
    ("libro-ro.json", 12, 10, "Amándoos los unos a los otros con caridad fraternal; previniéndoos con honra los unos a los otros;", "Amándoos los unos a los otros con amor fraternal; previniéndoos con honra los unos a los otros;"),
    ("libro-ro.json", 13, 10, "La caridad no hace mal al prójimo; así que, el cumplimento de la ley es la caridad.", "El amor no hace mal al prójimo; así que, el cumplimento de la ley es el amor."),
    ("libro-ro.json", 14, 15, "ya no andas conforme a la caridad.", "ya no andas conforme al amor."),
    ("libro-ro.json", 15, 30, "por la caridad del Espíritu, que me ayudéis con oraciones por mí a Dios,", "por el amor del Espíritu, que me ayudéis con oraciones por mí a Dios,"),

    ("libro-tit.json", 2, 2, "Que los viejos sean templados, graves, prudentes, sanos en la fe, en la caridad, en la paciencia.", "Que los viejos sean templados, graves, prudentes, sanos en la fe, en el amor, en la paciencia."),

    ("libro-2p.json", 1, 7, "Y en el temor de Dios, amor fraternal, y en el amor fraternal caridad.", "Y en el temor de Dios, amor fraternal, y en el amor fraternal amor."),
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
