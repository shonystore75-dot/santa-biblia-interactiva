# -*- coding: utf-8 -*-
"""
Modernizador ligero de la Reina Valera Antigua (1909) -> "RV 1909 Actualizada"
Criterio acordado: corregir SOLO ortografía obsoleta y vocabulario genuinamente
confuso para un lector de hoy. No parafrasear, no tocar lo que ya se entiende.
"""
import re, json, glob, os

# --- 1) Capa ortográfica (mecánica, muy segura) --------------------------
ORTOGRAFIA = [
    (r'\bfué\b', 'fue'), (r'\bFué\b', 'Fue'),
    (r'\bdió\b', 'dio'), (r'\bDió\b', 'Dio'),
    (r'\bvió\b', 'vio'), (r'\bVió\b', 'Vio'),
    (r'\bfuí\b', 'fui'), (r'\bFuí\b', 'Fui'),
    # NOTA: "crió"/"criado" NO se tocan de forma automática, porque "criado"
    # casi siempre significa "sirviente" en este texto (ej. "el criado de
    # Abraham"), y cambiarlo a "creado" altera el significado. Solo el verbo
    # "crió" en el sentido preciso de "creó" (Dios crió los cielos) se
    # revisa caso por caso, no con regex ciego.
    (r'\bá\b', 'a'), (r'\bÁ\b', 'A'),
    (r'\bé\b', 'e'),  # conjunción "é" (como "y") -> "e"
    (r'\bó\b', 'o'), (r'\bÓ\b', 'O'),  # disyunción "ó" -> "o"
    (r'\bpiés\b', 'pies'), (r'\bPiés\b', 'Pies'),
    (r'\bfuése\b', 'se fue'), (r'\bFuése\b', 'Se fue'),
    (r'\bobscuridad\b', 'oscuridad'), (r'\bObscuridad\b', 'Oscuridad'),
    (r'\bharéle\b', 'le haré'), (r'\bdiréle\b', 'le diré'),
    # Pronombre enclítico pospuesto en verbos con -óse/-óle al final ->
    # se antepone el pronombre a la forma moderna (patrón general, regex).
]

def normaliza_encliticos(t):
    def cap_swap(pronombre, raiz, terminacion):
        # Si la raíz original empezaba con mayúscula, la mayúscula pasa
        # al pronombre y el verbo queda en minúscula (regla de capitalización
        # en español: el pronombre antepuesto es la primera palabra).
        if raiz[0:1].isupper():
            return pronombre.capitalize() + ' ' + raiz.lower() + terminacion
        return pronombre + ' ' + raiz + terminacion

    t = re.sub(r'\b(\w+)óse\b', lambda m: cap_swap('se', m.group(1), 'ó'), t)
    t = re.sub(r'\b(\w+)óle\b', lambda m: cap_swap('le', m.group(1), 'ó'), t)
    t = re.sub(r'\b(\w+)éme\b', lambda m: cap_swap('me', m.group(1), 'é'), t)
    # "escondíme" (raíz + íme) -> "me escondí"
    t = re.sub(r'\b(\w+)íme\b', lambda m: cap_swap('me', m.group(1), 'í'), t)
    return t

# Subjuntivo imperfecto en -se -> -ra (equivalentes en español, mecánico)
SUBJUNTIVO_SE_RA = re.compile(r'\b(\w+)ase\b')
SUBJUNTIVO_ESE_RA = re.compile(r'\b(\w+)(i|ie)se\b')

def normaliza_subjuntivo(texto):
    # hablase -> hablara ; temiese/hiciese -> temiera/hiciera
    texto = re.sub(r'\b(\w+)ases\b', lambda m: m.group(1)+'aras', texto)
    texto = re.sub(r'\b(\w+)ieses\b', lambda m: m.group(1)+'ieras', texto)
    texto = re.sub(r'\b(\w+)ase\b', lambda m: m.group(1)+'ara', texto)
    texto = re.sub(r'\b(\w+)iese\b', lambda m: m.group(1)+'iera', texto)
    return texto

# --- 2) Capa de vocabulario arcaico -> claro (curada a mano, se amplía) ---
VOCABULARIO = [
    (r'\bEmpero\b', 'Pero'), (r'\bempero\b', 'pero'),
    (r'\bentrambos\b', 'ambos'), (r'\bEntrambos\b', 'Ambos'),
    (r'\bcalcañar\b', 'talón'), (r'\bcalcañares\b', 'talones'),
    (r'\btornado\b', 'vuelto'), (r'\btornar\b', 'volver'),
    (r'\bse enseñoreará\b', 'tendrá dominio'),
    (r'\benseñorear(á|se)?\b', 'dominar'),
    (r'\bpreñeces\b', 'embarazos'), (r'\bpreñez\b', 'embarazo'),
    (r'\bhaz del abismo\b', 'superficie del abismo'),
    (r'\bhaz de las aguas\b', 'superficie de las aguas'),
    (r'\bhaz de la tierra\b', 'superficie de la tierra'),
    (r'\bciencia del bien y del mal\b', 'conocimiento del bien y del mal'),
    (r'\bdelicioso a la vista\b', 'agradable a la vista'),
    (r'\bansí\b', 'así'),
    (r'\baqueste\b', 'este'), (r'\baquesta\b', 'esta'),
    (r'\bde la mar\b', 'del mar'), (r'\bDe la mar\b', 'Del mar'),
    (r'\ba la mar\b', 'al mar'), (r'\bA la mar\b', 'Al mar'),
    (r'\btrájolas\b', 'las trajo'), (r'\bTrájolas\b', 'Las trajo'),
    (r'\btrájola\b', 'la trajo'), (r'\bTrájola\b', 'La trajo'),
    (r'\btrájolo\b', 'lo trajo'), (r'\bTrájolo\b', 'Lo trajo'),
    (r'\btrájolos\b', 'los trajo'), (r'\bTrájolos\b', 'Los trajo'),
    (r'\bAdam\b', 'Adán'),
    (r'\bdíjole\b', 'le dijo'), (r'\bDíjole\b', 'Le dijo'),
    (r'\bhízole\b', 'le hizo'), (r'\bHízole\b', 'Le hizo'),
    (r'\bpor amor de ti\b', 'a causa de ti'), (r'\bPor amor de ti\b', 'A causa de ti'),
    (r'\ben el sudor de tu rostro\b', 'con el sudor de tu frente'),
    (r'\bEn el sudor de tu rostro\b', 'Con el sudor de tu frente'),
    (r'\breptil de ánima viviente\b', 'seres vivientes que se muevan'),
    (r'\balentó en su nariz\b', 'sopló en su nariz'),
    (r'\bsoplo de vida\b', 'aliento de vida'),
    (r'\bapartar el día y la noche\b', 'separar el día y la noche'),
]

def modernizar_texto(t):
    original = t
    for pat, rep in ORTOGRAFIA:
        t = re.sub(pat, rep, t)
    for pat, rep in VOCABULARIO:
        t = re.sub(pat, rep, t)
    t = normaliza_subjuntivo(t)
    t = normaliza_encliticos(t)
    return t

# --- 3) Excepciones por versículo exacto ---------------------------------
# "simiente" tiene dos sentidos en el texto: literal (semilla de planta) y
# de descendencia/linaje (NO se debe tocar, cambiaría el significado).
# Se revisó cada aparición a mano; solo estos versículos son sentido literal.
SIMIENTE_LITERAL = {
    ('gn', 1, 11), ('gn', 1, 12), ('gn', 1, 29),
    ('gn', 47, 19), ('gn', 47, 23),
}

# "crió/criado(s)" = "creó/creado(s)" SOLO en estos versículos revisados
# (donde el sujeto es Dios creando). En el resto del texto "criado" casi
# siempre significa "sirviente" y no se debe tocar.
CRIO_CREADOR = {
    ('gn', 1, 1), ('gn', 1, 21), ('gn', 1, 27), ('gn', 2, 3), ('gn', 2, 4),
}

# "género" = "especie" solo en contexto botánico/zoológico revisado
# (en otros lugares "género" puede tener otros sentidos).
GENERO_ESPECIE = {
    ('gn', 1, 11), ('gn', 1, 12), ('gn', 1, 21),
}

FRASES_POR_VERSO = {
    ('gn', 3, 1): [(r'\bde todo árbol del huerto\b', 'de ningún árbol del huerto')],
    ('gn', 3, 19): [(r'\bserás tornado\b', 'volverás')],
}

def modernizar_verso(libro, capitulo, versiculo, t):
    t = modernizar_texto(t)
    clave = (libro, capitulo, versiculo)
    if clave in SIMIENTE_LITERAL:
        t = re.sub(r'\bsimiente\b', 'semilla', t)
        t = re.sub(r'\bSimiente\b', 'Semilla', t)
    if clave in CRIO_CREADOR:
        t = re.sub(r'\bcrió\b', 'creó', t); t = re.sub(r'\bCrió\b', 'Creó', t)
        t = re.sub(r'\bcriado\b', 'creado', t); t = re.sub(r'\bCriado\b', 'Creado', t)
        t = re.sub(r'\bcriados\b', 'creados', t); t = re.sub(r'\bCriados\b', 'Creados', t)
    if clave in GENERO_ESPECIE:
        t = re.sub(r'\bgénero\b', 'especie', t); t = re.sub(r'\bGénero\b', 'Especie', t)
    for pat, rep in FRASES_POR_VERSO.get(clave, []):
        t = re.sub(pat, rep, t)
    return t

if __name__ == "__main__":
    import sys
    print(modernizar_texto(sys.argv[1]))
