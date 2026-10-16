#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regla de modernización: "henchir" (arcaico, = llenar) -> "llenar", en todas
sus conjugaciones donde el sentido es "llenar/rellenar".

NO toca:
  - "hinchazón" (sustantivo, hinchazón física) -> ya es español moderno normal.
  - "hinchar/hincharse" (verbo, hincharse físicamente un pie, vientre o río)
    -> ya es español moderno normal.
  - "hinchado(s)/hincha" en sentido figurado de orgullo/soberbia (7 versículos
    en cartas paulinas) -> pendiente de decisión aparte, no incluido aquí.
  - 1 Samuel 16:1 y 16:2 -> ya corregidos manualmente en un paso anterior.

Cada entrada es (archivo, capítulo, versículo, texto_viejo_exacto, texto_nuevo_exacto).
texto_viejo_exacto debe aparecer exactamente una vez en el texto del versículo.
"""

import json

CAMBIOS = [
    ("libro-1co.json", 10, 26, "Porque del Señor es la tierra y lo que la hinche.", "Porque del Señor es la tierra y lo que la llena."),
    ("libro-1co.json", 10, 28, "porque del Señor es la tierra y lo que la hinche", "porque del Señor es la tierra y lo que la llena"),

    ("libro-1r.json", 8, 10, "la nube hinchió la casa de Jehová", "la nube llenó la casa de Jehová"),
    ("libro-1r.json", 8, 11, "había henchido la casa de Jehová", "había llenado la casa de Jehová"),
    ("libro-1r.json", 18, 34, "Henchid cuatro cántaros de agua", "Llenad cuatro cántaros de agua"),
    ("libro-1r.json", 18, 35, "había también henchido de agua la reguera", "había también llenado de agua la reguera"),

    ("libro-1s.json", 2, 33, "henchir tu ánimo de dolor", "llenar tu ánimo de dolor"),

    ("libro-1ts.json", 2, 16, "para henchir la medida de sus pecados siempre", "para llenar la medida de sus pecados siempre"),

    ("libro-2cr.json", 5, 14, "había henchido la casa de Dios", "había llenado la casa de Dios"),
    ("libro-2cr.json", 7, 1, "la gloria de Jehová hinchió la casa", "la gloria de Jehová llenó la casa"),
    ("libro-2cr.json", 7, 2, "había henchido la casa de Jehová", "había llenado la casa de Jehová"),
    ("libro-2cr.json", 16, 14, "la cual hinchieron de aromas", "la cual llenaron de aromas"),
    ("libro-2cr.json", 24, 10, "echaban en el arca hasta henchirla", "echaban en el arca hasta llenarla"),

    ("libro-2r.json", 21, 16, "hasta henchir a Jerusalén de cabo a cabo", "hasta llenar a Jerusalén de cabo a cabo"),
    ("libro-2r.json", 23, 14, "e hinchió el lugar de ellos de huesos de hombres", "y llenó el lugar de ellos de huesos de hombres"),
    ("libro-2r.json", 24, 4, "pues hinchió a Jerusalén de sangre inocente", "pues llenó a Jerusalén de sangre inocente"),

    ("libro-2ts.json", 1, 11, "e hincha de bondad todo buen intento", "y llene de bondad todo buen intento"),

    ("libro-dn.json", 2, 35, "que hinchió toda la tierra", "que llenó toda la tierra"),

    ("libro-dt.json", 6, 11, "que tú no henchiste", "que tú no llenaste"),

    ("libro-ec.json", 1, 7, "y el mar no se hinche", "y el mar no se llena"),
    ("libro-ec.json", 1, 8, "ni los oídos se hinchen de oír", "ni los oídos se llenan de oír"),

    ("libro-ef.json", 1, 23, "hinche todas las cosas en todos", "llena todas las cosas en todos"),

    ("libro-esd.json", 9, 11, "la han henchido de uno a otro extremo", "la han llenado de uno a otro extremo"),

    ("libro-est.json", 7, 5, "ha henchido su corazón", "ha llenado su corazón"),

    ("libro-ex.json", 8, 21, "se henchirán de toda suerte de moscas", "se llenarán de toda suerte de moscas"),
    ("libro-ex.json", 15, 9, "mi alma se henchirá de ellos", "mi alma se llenará de ellos"),
    ("libro-ex.json", 16, 32, "Henchirás un gomer de él", "Llenarás un gomer de él"),
    ("libro-ex.json", 28, 3, "a quienes yo he henchido de espíritu de sabiduría", "a quienes yo he llenado de espíritu de sabiduría"),
    ("libro-ex.json", 29, 9, "henchirás las manos de Aarón y de sus hijos", "llenarás las manos de Aarón y de sus hijos"),
    ("libro-ex.json", 29, 33, "para henchir sus manos para ser santificados", "para llenar sus manos para ser santificados"),
    ("libro-ex.json", 31, 3, "lo he henchido de espíritu de Dios", "lo he llenado de espíritu de Dios"),
    ("libro-ex.json", 35, 31, "lo ha henchido de espíritu de Dios", "lo ha llenado de espíritu de Dios"),
    ("libro-ex.json", 35, 35, "los ha henchido de sabiduría de corazón", "los ha llenado de sabiduría de corazón"),
    ("libro-ex.json", 40, 34, "la gloria de Jehová hinchió el tabernáculo", "la gloria de Jehová llenó el tabernáculo"),

    ("libro-ez.json", 3, 3, "e hinche tus entrañas de este rollo", "y llena tus entrañas de este rollo"),
    ("libro-ez.json", 7, 19, "ni henchirán sus entrañas", "ni llenarán sus entrañas"),
    ("libro-ez.json", 9, 7, "henchid los atrios de muertos", "llenad los atrios de muertos"),
    ("libro-ez.json", 10, 2, "e hinche tus manos de carbones encendidos", "y llena tus manos de carbones encendidos"),
    ("libro-ez.json", 11, 6, "habéis henchido de muertos sus calles", "habéis llenado de muertos sus calles"),
    ("libro-ez.json", 30, 11, "henchirán la tierra de muertos", "llenarán la tierra de muertos"),
    ("libro-ez.json", 32, 5, "henchiré los valles de tu altura", "llenaré los valles de tu altura"),
    ("libro-ez.json", 32, 6, "los arroyos se henchirán de ti", "los arroyos se llenarán de ti"),
    ("libro-ez.json", 35, 8, "Y henchiré sus montes de sus muertos", "Y llenaré sus montes de sus muertos"),
    ("libro-ez.json", 43, 5, "la gloria de Jehová hinchió la casa", "la gloria de Jehová llenó la casa"),
    ("libro-ez.json", 43, 26, "ellos henchirán sus manos", "ellos llenarán sus manos"),
    ("libro-ez.json", 44, 4, "había henchido la casa de Jehová", "había llenado la casa de Jehová"),

    ("libro-gn.json", 1, 22, "henchid las aguas en los mares", "llenad las aguas en los mares"),
    ("libro-gn.json", 1, 28, "henchid la tierra", "llenad la tierra"),

    ("libro-hag.json", 2, 7, "henchiré esta casa de gloria", "llenaré esta casa de gloria"),

    ("libro-hch.json", 2, 2, "el cual hinchió toda la casa", "el cual llenó toda la casa"),
    ("libro-hch.json", 2, 28, "me henchirás de gozo con tu presencia", "me llenarás de gozo con tu presencia"),
    ("libro-hch.json", 14, 17, "hinchiendo de mantenimiento y de alegría nuestros corazones", "llenando de mantenimiento y de alegría nuestros corazones"),

    ("libro-is.json", 2, 6, "porque son henchidos de oriente", "porque están llenos de oriente"),
    ("libro-is.json", 6, 4, "la casa se hinchió de humo", "la casa se llenó de humo"),
    ("libro-is.json", 14, 21, "e hinchan la haz del mundo de ciudades", "y llenen la haz del mundo de ciudades"),
    ("libro-is.json", 15, 9, "las aguas de Dimón se henchirán de sangre", "las aguas de Dimón se llenarán de sangre"),
    ("libro-is.json", 27, 6, "la haz del mundo se henchirá de fruto", "la haz del mundo se llenará de fruto"),
    ("libro-is.json", 34, 1, "Oiga la tierra y lo que la hinche", "Oiga la tierra y lo que la llena"),
    ("libro-is.json", 42, 10, "los que descendéis al mar, y lo que la hinche", "los que descendéis al mar, y lo que la llena"),

    ("libro-jer.json", 13, 12, "Se henchirá de vino todo odre. Y ellos te dirán: ¿No sabemos que todo odre se henchirá de vino?",
                        "Se llenará de vino todo odre. Y ellos te dirán: ¿No sabemos que todo odre se llenará de vino?"),
    ("libro-jer.json", 23, 24, "¿No hincho yo, dice Jehová, el cielo y la tierra?", "¿No lleno yo, dice Jehová, el cielo y la tierra?"),
    ("libro-jer.json", 31, 25, "y henchido toda alma entristecida", "y llenado toda alma entristecida"),
    ("libro-jer.json", 33, 5, "para henchirlas de cuerpos de hombres muertos", "para llenarlas de cuerpos de hombres muertos"),
    ("libro-jer.json", 46, 12, "tu clamor hinchió la tierra", "tu clamor llenó la tierra"),
    ("libro-jer.json", 50, 11, "os henchisteis como becerra de renuevos", "os llenasteis como becerra de renuevos"),
    ("libro-jer.json", 51, 34, "hinchió su vientre de mis delicadezas", "llenó su vientre de mis delicadezas"),

    ("libro-jl.json", 2, 24, "las eras se henchirán de trigo", "las eras se llenarán de trigo"),

    ("libro-jn.json", 2, 7, "Les dice Jesús: Henchid estas tinajuelas de agua. Y las hinchieron hasta arriba.",
                      "Les dice Jesús: Llenad estas tinajuelas de agua. Y las llenaron hasta arriba."),
    ("libro-jn.json", 6, 13, "e hinchieron doce cestas de pedazos", "y llenaron doce cestas de pedazos"),
    ("libro-jn.json", 16, 6, "tristeza ha henchido vuestro corazón", "tristeza ha llenado vuestro corazón"),
    ("libro-jn.json", 19, 29, "hinchieron una esponja de vinagre", "llenaron una esponja de vinagre"),

    ("libro-job.json", 8, 21, "Aun henchirá tu boca de risa", "Aun llenará tu boca de risa"),
    ("libro-job.json", 15, 2, "henchirá su vientre de viento solano", "llenará su vientre de viento solano"),
    ("libro-job.json", 20, 23, "Cuando se ponga a henchir su vientre", "Cuando se ponga a llenar su vientre"),
    ("libro-job.json", 22, 18, "Les había él henchido sus casas de bienes", "Les había él llenado sus casas de bienes"),
    ("libro-job.json", 23, 4, "henchiría mi boca de argumentos", "llenaría mi boca de argumentos"),

    ("libro-js.json", 9, 13, "también los henchimos nuevos", "también los llenamos nuevos"),

    ("libro-lc.json", 1, 53, "A los hambrientos hinchió de bienes", "A los hambrientos llenó de bienes"),
    ("libro-lc.json", 3, 5, "Todo valle se henchirá", "Todo valle se llenará"),
    ("libro-lc.json", 15, 16, "deseaba henchir su vientre de las algarrobas", "deseaba llenar su vientre de las algarrobas"),

    ("libro-lv.json", 9, 17, "e hinchió de él su mano", "y llenó de él su mano"),
    ("libro-lv.json", 19, 29, "y se hincha de maldad", "y se llene de maldad"),
    ("libro-lv.json", 21, 10, "que hinchió su mano para vestir las vestimentas", "que llenó su mano para vestir las vestimentas"),

    ("libro-miq.json", 6, 12, "sus ricos se hinchieron de rapiña", "sus ricos se llenaron de rapiña"),

    ("libro-mt.json", 23, 32, "¡Vosotros también henchid la medida de vuestros padres!", "¡Vosotros también llenad la medida de vuestros padres!"),
    ("libro-mt.json", 27, 48, "la hinchió de vinagre", "la llenó de vinagre"),

    ("libro-nm.json", 3, 3, "cuyas manos él hinchió para administrar el sacerdocio", "cuyas manos él llenó para administrar el sacerdocio"),
    ("libro-nm.json", 14, 21, "mi gloria hinche toda la tierra", "mi gloria llena toda la tierra"),

    ("libro-pr.json", 1, 13, "henchiremos nuestras casas de despojos", "llenaremos nuestras casas de despojos"),
    ("libro-pr.json", 8, 21, "y que yo hincha sus tesoros", "y que yo llene sus tesoros"),
    ("libro-pr.json", 24, 4, "se henchirán las cámaras de todo bien preciado", "se llenarán las cámaras de todo bien preciado"),

    ("libro-ro.json", 11, 12, "¿cuánto más el henchimiento de ellos?", "¿cuánto más la plenitud de ellos?"),

    ("libro-sal.json", 17, 14, "cuyo vientre hinches de tu tesoro", "cuyo vientre llenas de tu tesoro"),
    ("libro-sal.json", 81, 10, "ensancha tu boca, y la henchiré", "ensancha tu boca, y la llenaré"),
    ("libro-sal.json", 126, 2, "nuestra boca se henchirá de risa", "nuestra boca se llenará de risa"),
    ("libro-sal.json", 127, 5, "el hombre que hinchió su aljaba de ellos", "el hombre que llenó su aljaba de ellos"),
    ("libro-sal.json", 129, 7, "no hinchió segador su mano", "no llenó segador su mano"),

    ("libro-sof.json", 1, 9, "los que hinchen de robo y de engaño las casas", "los que llenan de robo y de engaño las casas"),
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
