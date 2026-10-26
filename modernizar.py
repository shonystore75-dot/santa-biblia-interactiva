# -*- coding: utf-8 -*-
"""
Modernizador completo reconstruido a partir de las reglas documentadas
en la memoria del proyecto, para reprocesar Esdras, Ester y Nehemías
(que quedaron con el texto crudo del 1909 sin modernizar).
"""
import re

# --- 1) Ortografía mecánica -------------------------------------------
ORTOGRAFIA = [
    (r'\bfué\b', 'fue'), (r'\bFué\b', 'Fue'), (r'\bFUÉ\b', 'FUE'),
    (r'\bdió\b', 'dio'), (r'\bDió\b', 'Dio'),
    (r'\bvió\b', 'vio'), (r'\bVió\b', 'Vio'),
    # misma familia de monosílabos "-ió" que no llevan tilde en español moderno
    # (fué/dió/vió ya cubiertos arriba): guió/crió/rió/fió y sus mayúsculas
    (r'\bguió\b', 'guio'), (r'\bGuió\b', 'Guio'),
    (r'\bcrió\b', 'crio'), (r'\bCrió\b', 'Crio'),
    (r'\brió\b', 'rio'), (r'\bRió\b', 'Rio'),
    (r'\bfió\b', 'fio'), (r'\bFió\b', 'Fio'),
    (r'\blió\b', 'lio'), (r'\bLió\b', 'Lio'),
    (r'\bfrió\b', 'frio'), (r'\bFrió\b', 'Frio'),
    (r'\bfuí\b', 'fui'), (r'\bFuí\b', 'Fui'),
    (r'\bá\b', 'a'), (r'\bÁ\b', 'A'),
    (r'\bé\b', 'e'),
    (r'\bó\b', 'o'), (r'\bÓ\b', 'O'),
    (r'\bpiés\b', 'pies'), (r'\bPiés\b', 'Pies'),
    (r'\bfuése\b', 'se fue'), (r'\bFuése\b', 'Se fue'),
    (r'\bobscuridad\b', 'oscuridad'), (r'\bObscuridad\b', 'Oscuridad'),
    (r'\bharéle\b', 'le haré'), (r'\bdiréle\b', 'le diré'),
    (r'\bcaiste\b', 'caíste'),
    (r'\bdí\b', 'di'), (r'\bDí\b', 'Di'),
    (r'\bví\b', 'vi'), (r'\bVí\b', 'Vi'),
    # ciento y N -> ciento N (excepto "ciento y de", construcción distinta)
    (r'\bciento y (?!de\b)', 'ciento '),
    (r'\bCiento y (?!de\b)', 'Ciento '),
    # la mar -> el mar, con contracciones
    (r'\bde la mar\b', 'del mar'), (r'\bDe la mar\b', 'Del mar'),
    (r'\ba la mar\b', 'al mar'), (r'\bA la mar\b', 'Al mar'),
    (r'\bla mar\b', 'el mar'), (r'\bLa mar\b', 'El mar'),
    # Jerusalem -> Jerusalén
    (r'\bJerusalem\b', 'Jerusalén'),
    (r'\bAmorrheos\b', 'Amorreos'), (r'\bAmorrheo\b', 'Amorreo'),
    # Arabe -> árabe (gentilicio + tilde faltante)
    (r'\bArabes\b', 'árabes'), (r'\bArabe\b', 'árabe'),
    # diptongo -uído/-uída (y plurales) sin tilde
    (r'uíd', 'uid'), (r'Uíd', 'Uid'),
    # auxiliar+se glued (impersonal/pasiva): reordenar
    (r'\bHase\b', 'Se ha'),
    (r'\bhabíase\b', 'se había'), (r'\bHabíase\b', 'Se había'),
    (r'\boíase\b', 'se oía'), (r'\bOíase\b', 'Se oía'),
    (r'\bEmpero\b', 'Pero'), (r'\bempero\b', 'pero'),
    (r'\bentrambos\b', 'ambos'), (r'\bEntrambos\b', 'Ambos'),
    (r'\bplugo\b', 'agradó'), (r'\bPlugo\b', 'Agradó'),
]

# Imperativo usted+se ya en forma moderna correcta (terminan en -ase/-iese
# por coincidencia de letras, NO son subjuntivo imperfecto): no tocar.
EXCEPCIONES_NO_SUBJUNTIVO = {
    'hágase', 'escríbase', 'concédase', 'concédasele',
}

# --- 2) Nombres propios específicos verificados ------------------------
NOMBRES_ESPECIFICOS = [
    (r'\bMardochêo\b', 'Mardoqueo'),
    (r'\bAssuero\b', 'Asuero'),
    (r'\bJoseph\b', 'José'),
]

# Sufijo "-chías" (con circunflejo) -> "-quías" (regla ya establecida:
# Ezequías, Sedequías) generalizada a cualquier nombre con ese patrón.
def normaliza_chias(t):
    t = re.sub(r'(\w*)ch[îi]as\b', lambda m: m.group(1)+'quías', t)
    t = re.sub(r'(\w*)Ch[îi]as\b', lambda m: m.group(1)+'Quías', t)
    return t

# Circunflejo -> acento agudo (normalización diacrítica general, para
# el resto de nombres propios de las listas genealógicas que no tienen
# una forma estándar verificada específica).
CIRCUNFLEJOS = [
    ('â', 'á'), ('ê', 'é'), ('î', 'í'), ('ô', 'ó'), ('û', 'ú'),
    ('Â', 'Á'), ('Ê', 'É'), ('Î', 'Í'), ('Ô', 'Ó'), ('Û', 'Ú'),
]

def normaliza_circunflejos(t):
    for a, b in CIRCUNFLEJOS:
        t = t.replace(a, b)
    return t

# ph -> f, th -> t (excepciones ya aplicadas antes vía NOMBRES_ESPECIFICOS)
def normaliza_ph_th(t):
    t = re.sub(r'ph', 'f', t)
    t = re.sub(r'Ph', 'F', t)
    t = re.sub(r'PH', 'F', t)
    t = re.sub(r'th', 't', t)
    t = re.sub(r'Th', 'T', t)
    t = re.sub(r'TH', 'T', t)
    return t

# --- 3) Gentilicios mayúscula -> minúscula (regla general ya aplicada) -
GENTILICIOS = [
    r'Ammonitas?', r'Moabitas?', r'Caldeos?', r'Persas?', r'Jud[ií]os?',
    r'Cananeos?', r'Heteos?', r'Ferezeos?', r'Jebuseos?', r'Egipcios?',
    r'Amorreos?',
]

def normaliza_gentilicios(t):
    # Solo minúscula si NO es la primera palabra del versículo
    # (la primera palabra de la oración mantiene mayúscula por regla ortográfica normal).
    palabras = t.split(' ')
    for i in range(1, len(palabras)):
        for pat in GENTILICIOS:
            if re.fullmatch(pat, palabras[i].strip(',.;:()¿?¡!')):
                # preservar puntuacion pegada
                w = palabras[i]
                core_match = re.match(r'^(\W*)(\w+)(\W*)$', w)
                if core_match:
                    pre, core, post = core_match.groups()
                    palabras[i] = pre + core[0].lower() + core[1:] + post
    return ' '.join(palabras)

# --- 4) Pronombres enclíticos pospuestos (reordenamiento) -------------
PRONOMBRES = 'lo|la|los|las|le|les|se|nos|me|te'

def cap_swap(pronombre, raiz, terminacion=''):
    if raiz[0:1].isupper():
        return pronombre.capitalize() + ' ' + raiz.lower() + terminacion
    return pronombre + ' ' + raiz + terminacion

ACENTO_A_PLANO = {'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u'}

def quita_acento_final(s):
    if s and s[-1] in ACENTO_A_PLANO:
        return s[:-1] + ACENTO_A_PLANO[s[-1]]
    return s

# Vocabulario irregular ya establecido (formas glued con pronombre en
# verbos de raíz irregular: hacer/decir/traer)
VOCABULARIO_IRREGULARES = [
    (r'\bdíjole\b', 'le dijo'), (r'\bDíjole\b', 'Le dijo'),
    (r'\bhízole\b', 'le hizo'), (r'\bHízole\b', 'Le hizo'),
    (r'\btrájolo\b', 'lo trajo'), (r'\bTrájolo\b', 'Lo trajo'),
    (r'\btrájola\b', 'la trajo'), (r'\bTrájola\b', 'La trajo'),
    (r'\btrájolos\b', 'los trajo'), (r'\bTrájolos\b', 'Los trajo'),
    (r'\btrájolas\b', 'las trajo'), (r'\bTrájolas\b', 'Las trajo'),
    (r'\bhízose\b', 'se hizo'), (r'\bHízose\b', 'Se hizo'),
    (r'\bpúsose\b', 'se puso'), (r'\bPúsose\b', 'Se puso'),
]

def normaliza_encliticos(t):
    # 1a/3a persona pretérito simple: -é/-í/-ó + pronombre
    def repl_preterito(m):
        raiz, vocal, pron = m.group(1), m.group(2), m.group(3)
        return cap_swap(pron, raiz, vocal)
    t = re.sub(r'\b(\w+?)(é|í|ó)(' + PRONOMBRES + r')\b',
               repl_preterito, t)

    # 2a persona pretérito: -ste + pronombre (nunca lleva tilde al
    # anteponer el pronombre: diste/hiciste/dijiste/etc.)
    def repl_ste(m):
        raiz, pron = m.group(1), m.group(2)
        raiz = quita_acento_final(raiz)
        return cap_swap(pron, raiz, 'ste')
    t = re.sub(r'\b(\w+?)ste(' + PRONOMBRES + r')\b', repl_ste, t)

    # futuro simple: -ré/-rá/-rán + pronombre
    def repl_futuro(m):
        raiz, term, pron = m.group(1), m.group(2), m.group(3)
        return cap_swap(pron, raiz, term)
    t = re.sub(r'\b(\w+?)(ré|rán|rá)(' + PRONOMBRES + r')\b', repl_futuro, t)

    # imperfecto -aba + pronombre (no reflexivo, sin "se")
    PRON_NO_REFL = 'lo|la|los|las|le|les|nos|te|me'
    def repl_aba(m):
        raiz, pron = m.group(1), m.group(2)
        return cap_swap(pron, raiz, 'aba')
    t = re.sub(r'\b(\w+?)aba(' + PRON_NO_REFL + r')\b', repl_aba, t)

    # pretérito 3a plural: -aron/-ieron + pronombre
    def repl_aron(m):
        raiz, term, pron = m.group(1), m.group(2), m.group(3)
        return cap_swap(pron, raiz, term)
    t = re.sub(r'\b(\w+?)(aron|ieron)(' + PRONOMBRES + r')\b', repl_aron, t)

    # pretérito irregular -íje + pronombre (dije/bendije/maldije,
    # nunca lleva tilde en la forma normal: "dije", no "díje")
    def repl_ije(m):
        raiz, pron = m.group(1), m.group(2)
        return cap_swap(pron, raiz, 'ije')
    t = re.sub(r'\b(\w+?)íje(' + PRONOMBRES + r')\b', repl_ije, t)

    # presente "dice/dicen" + pronombre (diálogo típico evangelios)
    def repl_dice(m):
        base, pron = m.group(1), m.group(2)
        return cap_swap(pron, base, '')
    t = re.sub(r'\b([Dd]ice)(' + PRONOMBRES + r')\b',
               lambda m: cap_swap(m.group(2), m.group(1)), t)
    t = re.sub(r'\b([Dd]icen)(' + PRONOMBRES + r')\b',
               lambda m: cap_swap(m.group(2), m.group(1)), t)

    # pretérito irregular "hice" + pronombre
    t = re.sub(r'\b([Hh]ice)(' + PRONOMBRES + r')\b',
               lambda m: cap_swap(m.group(2), m.group(1)), t)

    return t

def limpia_tilde_sobrante(t):
    # Tras anteponer el pronombre, corregir tildes que ya no corresponden
    # en los verbos más comunes que quedaron con acento de esdrújula/aguda
    correcciones = [
        (r'\bhízo\b', 'hizo'), (r'\bHízo\b', 'Hizo'),
        (r'\bdíjo\b', 'dijo'), (r'\bDíjo\b', 'Dijo'),
        (r'\bmándo\b', 'mando'),
    ]
    for pat, rep in correcciones:
        t = re.sub(pat, rep, t)
    return t

# --- 5) Subjuntivo -se -> -ra ------------------------------------------
def normaliza_subjuntivo(t):
    def repl_ase(m):
        if m.group(0).lower() in EXCEPCIONES_NO_SUBJUNTIVO:
            return m.group(0)
        return m.group(1) + 'ara'
    t = re.sub(r'\b(\w+)ases\b', lambda m: m.group(1)+'aras', t)
    t = re.sub(r'\b(\w+)ieses\b', lambda m: m.group(1)+'ieras', t)
    t = re.sub(r'\b(\w+)ase\b', repl_ase, t)
    t = re.sub(r'\b(\w+)iese\b', lambda m: m.group(1)+'iera', t)
    # verbos con raíz en ñ (constreñir/teñir/ceñir/reñir...): -ñese -> -ñera
    t = re.sub(r'\b(\w+ñ)ese\b', lambda m: m.group(1)+'era', t)
    return t

# --- 6) Pipeline general ------------------------------------------------
def aplica_ortografia(t):
    for pat, rep in ORTOGRAFIA:
        t = re.sub(pat, rep, t)
    for pat, rep in VOCABULARIO_IRREGULARES:
        t = re.sub(pat, rep, t)
    return t

def modernizar_texto_general(t):
    for pat, rep in NOMBRES_ESPECIFICOS:
        t = re.sub(pat, rep, t)
    t = normaliza_chias(t)
    t = normaliza_circunflejos(t)
    t = normaliza_ph_th(t)
    t = aplica_ortografia(t)
    t = normaliza_gentilicios(t)
    t = normaliza_subjuntivo(t)
    t = normaliza_encliticos(t)
    t = limpia_tilde_sobrante(t)
    t = aplica_ortografia(t)  # segunda pasada: la reordenación de
                               # pronombres puede volver a exponer
                               # "dió/vió/fué/á/é/ó" que quedaban
                               # protegidos dentro de la palabra pegada
    return t

# --- 7) Mayúscula fija de capítulo -------------------------------------
NOMBRES_PROPIOS = set()  # ninguno de los casos aplica en esd/est/neh

def decapitaliza_inicio_capitulo(t):
    palabras = t.split(' ')
    i = 0
    fijo = []
    while i < len(palabras):
        w = palabras[i]
        core = re.sub(r'[^A-ZÁÉÍÓÚÑ]', '', w)
        if len(core) >= 1 and w == w.upper() and any(c.isalpha() for c in w):
            fijo.append(i)
            i += 1
        else:
            break
    if not fijo:
        return t
    # si alguna es nombre propio conocido, no tocar (no aplica aquí)
    for idx in fijo:
        w = palabras[idx]
        nucleo = re.sub(r'[^A-ZÁÉÍÓÚÑ]', '', w)
        if nucleo.lower() in NOMBRES_PROPIOS:
            continue
        if idx == 0:
            # primera palabra de la oración: solo la primera letra mayúscula
            palabras[idx] = w[0] + w[1:].lower()
        else:
            palabras[idx] = w.lower()
    return ' '.join(palabras)

def modernizar_verso_completo(t):
    t = decapitaliza_inicio_capitulo(t)
    t = modernizar_texto_general(t)
    return t

# --- 8) Correcciones puntuales por versículo (juicio ya verificado) ----
FRASES_POR_VERSO = {
    ('esd', 1, 4): [(r'\bque hubiere quedado\b', 'que haya quedado'),
                    (r'\bdonde peregrinare\b', 'donde peregrine')],
    ('esd', 3, 11): [(r'\bcon grande júbilo\b', 'con gran júbilo')],
    ('esd', 3, 13): [(r'\bcon grande júbilo\b', 'con gran júbilo')],
    ('esd', 4, 13): [(r'\bfuere reedificada\b', 'es reedificada'),
                      (r'\bfueren establecidos\b', 'son establecidos')],
    ('esd', 4, 16): [(r'\bfuere edificada\b', 'es edificada')],
    ('esd', 6, 9): [(r'\blo que fuere necesario\b', 'lo que sea necesario'),
                     (r'\blo que dijeren\b', 'lo que digan')],
    ('esd', 7, 13): [(r'\bque quisiere\b', 'que quiera')],
    ('esd', 7, 20): [(r'\bque te fuere menester dar, daráslo\b',
                       'que te sea menester dar, lo darás')],
    ('esd', 7, 25): [(r'\bno la tuviere\b', 'no la tenga')],
    ('esd', 9, 7): [(r'\ben grande culpa\b', 'en gran culpa')],
    ('esd', 9, 13): [(r'\bnuestro grande delito\b', 'nuestro gran delito')],
    ('esd', 10, 1): [(r'\buna muy grande multitud\b', 'una muy gran multitud')],
    ('esd', 10, 14): [(r'\bhubieren tomado\b', 'hayan tomado')],
    ('esd', 5, 1): [(r'\bHaggeo profeta\b', 'el profeta Haggeo')],
    ('esd', 6, 14): [(r'\bde Haggeo profeta\b', 'del profeta Haggeo')],
    ('esd', 7, 12): [(r'\ba Esdras sacerdote\b', 'al sacerdote Esdras')],
    ('esd', 7, 21): [(r'\bEsdras sacerdote\b', 'el sacerdote Esdras'),
                      (r'\bdemandare\b', 'demande')],
    ('esd', 10, 16): [(r'\bEsdras sacerdote\b', 'el sacerdote Esdras')],
    ('esd', 8, 33): [(r'\bde Urías sacerdote\b', 'del sacerdote Urías')],
    ('esd', 7, 11): [(r'\ba Esdras, sacerdote escriba,\b', 'al sacerdote escriba Esdras,')],
    ('esd', 6, 11): [(r'\bque mudare este decreto\b', 'que mude este decreto')],
    ('esd', 6, 12): [(r'\bque pusiere su mano\b', 'que ponga su mano')],
    ('esd', 7, 16): [(r'\bque hallares\b', 'que halles'),
                      (r'\bofrecieren\b', 'ofrezcan')],
    ('esd', 7, 18): [(r'\bpluguiere hacer\b', 'plazca hacer')],
    ('esd', 7, 26): [(r'\bque no hiciere la ley\b', 'que no haga la ley')],
    ('est', 4, 1): [(r'\bde saco y de ceniza\b', 'de cilicio y de ceniza'),
                     (r'\bcon grande y amargo\b', 'con gran y amargo')],
    ('est', 4, 2): [(r'\bcon vestido de saco\b', 'con vestido de cilicio')],
    ('est', 4, 3): [(r'\bgrande luto\b', 'gran luto'),
                     (r'\bsaco y ceniza era\b', 'cilicio y ceniza era')],
    ('est', 4, 4): [(r'\bquitar el saco\b', 'quitar el cilicio')],
    ('est', 2, 4): [(r'\bque agradare a los ojos\b', 'que agrade a los ojos')],
    ('est', 3, 11): [(r'\bte pareciere\b', 'te parezca')],
    ('est', 4, 11): [(r'\bel rey extendiere el cetro\b', 'el rey extienda el cetro')],
    ('est', 4, 14): [(r'\bsi absolutamente callares\b', 'si absolutamente callas')],
    ('est', 8, 8): [(r'\bos pareciere\b', 'os parezca')],
    ('est', 7, 4): [(r'\bcallárame\b', 'me callara')],
    ('neh', 1, 9): [(r'\bSi fuere vuestro lanzamiento\b',
                      'Si va vuestro lanzamiento')],
    ('neh', 3, 27): [(r'\bla grande torre\b', 'la gran torre')],
    ('neh', 4, 3): [(r'\bsi subiere una zorra\b', 'si sube una zorra')],
    ('neh', 5, 7): [(r'\buna grande junta\b', 'una gran junta')],
    ('neh', 6, 3): [(r'\buna grande obra\b', 'una gran obra')],
    ('neh', 8, 12): [(r'\bde grande alegría\b', 'de gran alegría')],
    ('neh', 9, 1): [(r'\by con sacos\b', 'y con cilicios')],
    ('neh', 9, 25): [(r'\btu grande bondad\b', 'tu gran bondad')],
    ('neh', 9, 29): [(r'\bsi el hombre hiciere\b', 'si el hombre hace')],
    ('neh', 9, 32): [(r'\bno sea tenido en poco delante de ti todo el trabajo\b',
                       'no sea tenida en poco delante de ti toda la aflicción')],
    ('neh', 9, 37): [(r'\ben grande angustia\b', 'en gran angustia')],
    ('neh', 11, 14): [(r'\bde grande vigor\b', 'de gran vigor')],
    ('neh', 12, 43): [(r'\bcon grande contentamiento\b', 'con gran contentamiento')],
    ('neh', 13, 5): [(r'\buna grande cámara\b', 'una gran cámara')],
    ('neh', 4, 12): [(r'\bSucedió pero, que\b', 'Pero sucedió que')],
    ('neh', 9, 17): [(r'\bTú pero, eres Dios de perdones\b', 'Pero tú eres Dios de perdones')],
    ('neh', 9, 33): [(r'\bTú pero eres justo\b', 'Pero tú eres justo')],
    ('neh', 13, 4): [(r'\bEliasib sacerdote\b', 'el sacerdote Eliasib')],
    ('neh', 5, 13): [(r'\bque no cumpliere esto\b', 'que no cumpla esto')],
    ('neh', 6, 14): [(r'\bde Noadías profetisa\b', 'de la profetisa Noadías')],
    ('neh', 13, 13): [(r'\ba Selemías sacerdote\b', 'al sacerdote Selemías'),
                       (r'\ba Sadoc escriba\b', 'al escriba Sadoc')],
    ('neh', 8, 13): [(r'\ba Esdras escriba\b', 'al escriba Esdras')],
    ('neh', 12, 36): [(r'\bEsdras escriba\b', 'el escriba Esdras')],
}

def modernizar_verso(libro, capitulo, versiculo, t, primer_verso=False):
    if primer_verso:
        t = decapitaliza_inicio_capitulo(t)
    t = modernizar_texto_general(t)
    clave = (libro, capitulo, versiculo)
    for pat, rep in FRASES_POR_VERSO.get(clave, []):
        t = re.sub(pat, rep, t)
    return t
