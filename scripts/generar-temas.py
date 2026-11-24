# Genera temas.css a partir de las 9 paletas (y calcula los colores derivados).
# Uso: python scripts/generar-temas.py  -> escribe temas.css, imprime la tabla de contraste
# Los iconos de la barra inferior (nav-<icono>-<paleta>.png) se generan con scripts/generar-iconos-nav.py
def rgb(h): return [int(h[i:i+2],16) for i in (1,3,5)]
def hx(c): return '#%02X%02X%02X'%tuple(int(round(v)) for v in c)
def L(h):
    c=[v/255 for v in rgb(h)]
    c=[x/12.92 if x<=.03928 else ((x+.055)/1.055)**2.4 for x in c]
    return .2126*c[0]+.7152*c[1]+.0722*c[2]
def cr(a,b):
    x,y=sorted([L(a),L(b)],reverse=True);return round((x+.05)/(y+.05),2)
def mix(a,b,t):  # t=0 -> a ; t=1 -> b
    return hx([x+(y-x)*t for x,y in zip(rgb(a),rgb(b))])
def hasta(color,destino,fondos,minimo=4.6):
    """acerca 'color' a 'destino' hasta que contraste >= minimo con todos los fondos"""
    t=0
    while t<=1.0001:
        c=mix(color,destino,min(t,1))
        if all(cr(c,f)>=minimo for f in fondos): return c
        t+=0.01
    return destino
def triple(h): return ','.join(str(v) for v in rgb(h))

PALETA_POR_DEFECTO='turquesa'
NOMBRES={'azul':'Azul clásico','borgona':'Borgoña real','olivo':'Verde olivo','tierra':'Tierra bíblica','purpura':'Púrpura espiritual','turquesa':'Turquesa renovación','nocturna':'Nocturna','marfil':'Marfil clásico','ambar':'Ámbar inspirador'}
P={ # fondo, tarjeta, texto, nav, acento  (los colores base NO se tocan)
'azul':('#F7F5F0','#FFFCF6','#172B47','#102F50','#D6A84E'),
'borgona':('#FAF3EB','#FFFDF7','#56202B','#641D2B','#D5A348'),
'olivo':('#F4F3E7','#FFFDF5','#2E4129','#344C2B','#C9A34E'),
'tierra':('#F8F0E5','#FFF9EF','#543526','#78452D','#D9A54D'),
'purpura':('#F6F2F8','#FFFFFF','#49325F','#49325F','#D7AD58'),
'turquesa':('#EFF7F5','#FFFFFF','#184A51','#12616A','#D6AC55'),
'nocturna':('#18212D','#293545','#F5F0E5','#202A38','#D5AC60'),
'marfil':('#FCF8EF','#FFFFFF','#59392D','#F2E7D1','#A96835'),
'ambar':('#FFF3E5','#FFFCF6','#71391F','#93421D','#D7A044')}
# ---- DORADO METALICO DE TERMINO MEDIO (opcion B) (ajustar aqui; el resto sale de estas constantes) ----
ORO_LINEA='linear-gradient(90deg, #8A6420, #F0D27A 30%, #FFF1B8 50%, #E2B94F 70%, #8A6420)'   # lineas finas (encabezado/barra/separadores)
ORO_BORDE='#E2B94F'                  # bordes de tarjetas y detalles
ORO_ICONO='#F0CF72'                  # color de referencia de los iconos de la barra (el dibujo lleva ademas luces y sombras)
ORO_TEXTO='#F0D27A'                  # dorado de la etiqueta activa y subtitulos (se aclara si hace falta para 4,5:1)
ORO_BRILLO='rgba(255,226,140,0.75)'    # resplandor de los iconos
ORO_RADIO_BRILLO='3px'
ORO_LINEA_PX='3px'                   # espesor de las lineas doradas del encabezado y de la barra inferior
ORO_BORDE_PX='1.5px'                 # espesor del borde dorado de las tarjetas
# Marfil (barra clara): el dorado vivo se pierde sobre claro; iconos de bronce metalico y lineas con extremos mas oscuros
BRONCE_OSCURO='#7A4A1F'; BRONCE_CLARO='#B07A33'
MARFIL_LINEA='linear-gradient(90deg, #5E3A0C, #B9770E 30%, #F0C14B 50%, #C48414 70%, #5E3A0C)'
MARFIL_BORDE='#C9921A'
# Nocturna (fondo oscuro): resplandor un poco mas fuerte
NOCTURNA_RADIO_BRILLO='5px'
# ---- Azul clasico (piloto de texturas por capas): cuero en encabezado/barra, papel en el fondo, algodon en tarjetas ----
INTENSIDAD_CUERO=1.0      # opacidad del cuero fotografico sobre #102F50 liso (1 = 100 %; 0,7 = grano mas suave)
TEX_CUERO='texturas/cuero_azul_realista.webp'      # 1000x1000, color medio #102F50 (scripts/generar-cuero-realista.py); NO repite en mosaico: una sola imagen
TAM_CUERO='500px auto'                              # ancho aprox. 460-520 px (el telefono no pasa de 480 px de ancho)
POS_CUERO_ENCABEZADO='left top'; POS_CUERO_BARRA='right bottom'   # zonas distintas de la imagen para que no sean identicas
TEX_PAPEL='texturas/02_papel_marfil_grisaceo.webp'  # overlay, alfa fijo 12/255
TEX_ALGODON='texturas/03_papel_blanco_marfil.webp'  # overlay, alfa fijo 7/255
INTENSIDAD_PAPEL=3        # multiplica la opacidad del papel del fondo (1 = la del archivo). Elegido en la comparacion x1/x3/x5
INTENSIDAD_ALGODON=2.5    # idem para las tarjetas
CUERO_BRILLO=0.03        # degradado vertical blanco leve sobre el cuero (arriba)
TAM_PAPEL='256px'; TAM_ALGODON='256px'
# ---- Texturas reales de Turquesa (scripts/generar-texturas-turquesa.py) y Borgona (scripts/generar-texturas-borgona.py) ----
# cuero: encabezado y barra | papel: fondo (una sola imagen que cubre el telefono) y tarjetas (velo del color de la tarjeta encima) | boton: botones redondos del encabezado y boton flotante de Leer
REAL={
'turquesa':dict(cuero='texturas/cuero_turquesa_realista.webp',papel='texturas/papel_marfil_verdoso.webp',boton='texturas/cuero_turquesa_oscuro.webp',   # media #12616A / #EFF7F5 / #184A51
                i_cuero=1.0,i_papel=1.0,velo_tarjeta=0.65,tam_cuero='500px auto',rep_cuero='no-repeat',tam_papel='cover',tam_tarjeta='600px auto',tam_boton='200px auto',color_boton='#184A51'),
'borgona':dict(cuero='texturas/piedra_borgona.webp',papel='texturas/papel_borgona.webp',boton='texturas/piedra_borgona_oscura.webp',   # media #641D2B / #FAF3EB / #420E20
                i_cuero=1.0,i_papel=1.0,velo_tarjeta=0.65,tam_cuero='500px auto',rep_cuero='no-repeat',pos_barra='right 50%',tam_papel='cover',tam_tarjeta='600px auto',tam_boton='200px auto',color_boton='#420E20'),
}
SOMBRA_AZUL_TARJETA='0 1px 3px rgba(0,0,0,0.14), 0 6px 12px -4px rgba(0,0,0,0.15)'   # negra 12-18 %, blur 3-12 px
SOMBRA_AZUL_BOTON='0 1px 3px rgba(0,0,0,0.14), 0 6px 12px -4px rgba(0,0,0,0.16)'
import math
def capas(url,k):   # k veces la opacidad del archivo: N capas apiladas + opacidad k/N (en el fondo); en tarjetas solo N=round(k)
    return ', '.join(["url('%s')"%url]*k)
TARJETA_MARFIL_ALFA=0.80 # Marfil: tarjetas de blanco translucido para que se asomen las vetas
VELO_HERO=0.85           # intensidad del velo del hero de Inicio en el borde superior (0,85 por pedido de Diego (antes 0,65))
MINIMO_ICONO=3.0         # contraste minimo de un icono de interfaz (WCAG 1.4.11, no texto)

def derivar(n):
    f,t,x,nv,a=P[n]
    d=dict(fondo=f,tarjeta=t,texto=x,nav=nv,acento=a)
    d['tarjeta_css']=t
    d['tarjeta_efectiva']=t   # color real de la tarjeta sobre el fondo (para los contrastes)
    d['icono_ajustado']=False
    if n=='marfil':
        d['tarjeta_css']='rgba(%s,%s)'%(triple(t),TARJETA_MARFIL_ALFA)
        d['tarjeta_efectiva']=mix(f,t,TARJETA_MARFIL_ALFA)
        d['sobre_nav']=x
        d['sobre_nav_suave']=mix(x,nv,0.1)
        d['acento_nav']=hasta(a,'#000000',[nv],4.6)          # texto dorado oscuro sobre barra clara
        d['icono_nav']=BRONCE_CLARO; d['icono_tipo']='bronce'
        d['oro_linea']=MARFIL_LINEA; d['oro_borde']=MARFIL_BORDE; d['oro_brillo']='rgba(255,255,255,0.85)'; d['oro_radio']='2px'; d['oro_sombra']='rgba(122,74,31,0.45)'
        d['principal']=x; d['sobre_principal']='#FFFFFF'
        d['cita']=hasta(a,'#000000',[d['tarjeta_efectiva'],f],4.6)
        d['oscuro']=x; d['sobre_oscuro']=nv
        d['sobre_acento']='#FFFFFF'; d['acento_btn']=d['cita']
        d['hero']=x
        d['btn_nav_bg']='rgba(%s,0.08)'%triple(x); d['btn_nav_borde']='rgba(%s,0.55)'%triple(a)
    elif n=='nocturna':
        d['sobre_nav']='#FFFFFF'
        d['sobre_nav_suave']=hasta(mix('#FFFFFF',nv,0.3),'#FFFFFF',[nv],4.6)
        d['acento_nav']=hasta(ORO_TEXTO,'#FFFFFF',[nv],4.6)
        d['icono_nav']=ORO_ICONO; d['icono_tipo']='vivo'
        d['oro_radio']=NOCTURNA_RADIO_BRILLO
        d['principal']=a; d['sobre_principal']=f
        d['cita']=hasta(a,'#FFFFFF',[t,f],4.6)
        d['oscuro']=nv; d['sobre_oscuro']=d['acento_nav']
        d['sobre_acento']=f
        d['hero']=nv
        d['btn_nav_bg']='rgba(255,255,255,0.10)'; d['btn_nav_borde']='rgba(%s,0.5)'%triple(a)
    else:
        d['sobre_nav']='#FFFFFF'
        d['sobre_nav_suave']=hasta(mix('#FFFFFF',nv,0.3),'#FFFFFF',[nv],4.6)
        d['acento_nav']=hasta(ORO_TEXTO,'#FFFFFF',[nv],4.6)   # texto dorado sobre la barra (4.5:1)
        d['icono_tipo']='vivo'
        if cr(ORO_ICONO,nv)>=MINIMO_ICONO: d['icono_nav']=ORO_ICONO       # icono: dorado vivo (3:1 minimo)
        else: d['icono_nav']=hasta(ORO_ICONO,'#FFFFFF',[nv],MINIMO_ICONO); d['icono_ajustado']=True
        d['principal']=nv
        d['sobre_principal']='#FFFFFF'
        d['cita']=d['principal']
        d['oscuro']=nv; d['sobre_oscuro']=d['acento_nav']
        d['sobre_acento']=x
        d['hero']=nv
        d['btn_nav_bg']='rgba(255,255,255,0.12)'; d['btn_nav_borde']='rgba(%s,0.5)'%triple(a)
    if n=='azul':
        d['cita']=x                      # referencias y titulos: #172B47
        d['sombra_rgb']='0,0,0'
    d.setdefault('acento_btn',a)
    d.setdefault('oro_linea',ORO_LINEA); d.setdefault('oro_borde',ORO_BORDE); d.setdefault('oro_brillo',ORO_BRILLO); d.setdefault('oro_radio',ORO_RADIO_BRILLO); d.setdefault('oro_sombra','rgba(0,0,0,0.35)')
    if n!='marfil':
        d['sobre_acento']=hasta(x if L(x)<0.5 else f,'#000000' if L(x)<0.5 else '#FFFFFF',[d['acento_btn']],4.6)
    return d

def css():
    o=['/* GENERADO por scripts/generar-temas.py: no editar a mano. 9 paletas; la de por defecto es Turquesa renovacion. */\n']
    def bloque(sel,n):
        d=derivar(n)
        marfil = n=='marfil'; azul = n=='azul'; turq = n in REAL
        v=[('fondo',d['fondo']),('tarjeta',d['tarjeta_css']),('tarjeta-solida',d['tarjeta']),('texto',d['texto']),('nav',d['nav']),('acento',d['acento']),
           ('sobre-nav',d['sobre_nav']),('sobre-nav-suave',d['sobre_nav_suave']),('acento-nav',d['acento_nav']),('icono-nav',d['icono_nav']),
           ('principal',d['principal']),('sobre-principal',d['sobre_principal']),('cita',d['cita']),
           ('oscuro',d['oscuro']),('sobre-oscuro',d['sobre_oscuro']),('sobre-acento',d['sobre_acento']),('acento-btn',d['acento_btn']),('oro-linea',d['oro_linea']),('oro-borde',d['oro_borde']),('oro-icono',d['icono_nav']),('oro-brillo',d['oro_brillo']),('oro-radio',d['oro_radio']),('oro-sombra',d['oro_sombra']),
           ('btn-nav-bg',d['btn_nav_bg']),('btn-nav-borde',d['btn_nav_borde']),
           ('principal-rgb',triple(d['principal'])),('texto-rgb',triple(d['texto'])),('acento-rgb',triple(d['acento'])),('hero-rgb',triple(d['hero'])),
           ('titulo-rollo','#3B2A1C' if n=='nocturna' else (d['texto'] if (marfil or azul) else d['nav'])),
           ('tarjeta-rgb',triple(d['tarjeta'])),('sombra-rgb','0,0,0' if n in ('nocturna','azul') else triple(d['texto'])),
           ('palabras-jesus','#FF9A8F' if n=='nocturna' else '#9B1024'),
           ('z-barra','40' if (marfil or azul or turq) else 'auto'),
           ('aislar-barra','isolate' if (marfil or azul or turq) else 'auto')]
        # texturas: fondo de pantalla (.phone), encabezado/barra inferior y tarjetas. 'none' = sin textura (todas salvo Marfil y Azul)
        if marfil:
            tx=dict(fondo="url('marmol_marfil_fuerte.webp')",tf='600px',of='0.5',barra="url('marmol_marfil_fuerte.webp')",tb='600px',ob='0.5',tinte='none',tarjeta='none',tt='auto')
        elif azul:
            nf=math.ceil(INTENSIDAD_PAPEL)
            tx=dict(fondo=capas(TEX_PAPEL,nf),tf=TAM_PAPEL,of='%.4g'%(INTENSIDAD_PAPEL/nf),barra="url('%s')"%TEX_CUERO,tb=TAM_CUERO,ob='%g'%INTENSIDAD_CUERO,
                    tinte='linear-gradient(180deg, rgba(255,255,255,%.2f), rgba(255,255,255,0))'%CUERO_BRILLO,
                    tarjeta=capas(TEX_ALGODON,max(1,round(INTENSIDAD_ALGODON))),tt=TAM_ALGODON)
        elif turq:
            r=REAL[n]
            tx=dict(fondo="url('%s')"%r['papel'],tf=r['tam_papel'],of='%g'%r['i_papel'],barra="url('%s')"%r['cuero'],tb=r['tam_cuero'],ob='%g'%r['i_cuero'],
                    tinte='linear-gradient(180deg, rgba(255,255,255,%.2f), rgba(255,255,255,0))'%CUERO_BRILLO,
                    tarjeta="linear-gradient(rgba(%s,%g), rgba(%s,%g)), url('%s')"%(triple(d['tarjeta']),r['velo_tarjeta'],triple(d['tarjeta']),r['velo_tarjeta'],r['papel']),tt=r['tam_tarjeta'])
        else:
            tx=dict(fondo='none',tf='auto',of='0',barra='none',tb='auto',ob='0',tinte='none',tarjeta='none',tt='auto')
        rep,posh,posn=((REAL[n]['rep_cuero'] if turq else 'no-repeat'),POS_CUERO_ENCABEZADO,(REAL[n].get('pos_barra',POS_CUERO_BARRA) if turq else POS_CUERO_BARRA)) if (azul or turq) else ('repeat','0 0','0 0')
        v+=[('repeticion-barra',rep),('posicion-encabezado',posh),('posicion-nav',posn),('textura-fondo',tx['fondo']),('tamano-fondo',tx['tf']),('intensidad-fondo',tx['of']),('fondo-display','block' if tx['fondo']!='none' else 'none'),
            ('textura-barra',tx['barra']),('tamano-barra',tx['tb']),('intensidad-barra',tx['ob']),('barra-display','block' if tx['barra']!='none' else 'none'),
            ('barra-tinte',tx['tinte']),('tinte-display','block' if tx['tinte']!='none' else 'none'),
            ('textura-tarjeta',tx['tarjeta']),('tamano-tarjeta',tx['tt']),('intensidad-papel',str(INTENSIDAD_PAPEL) if azul else '0'),('intensidad-algodon',str(INTENSIDAD_ALGODON) if azul else '0')]
        if turq: v+=[('repeticion-fondo','no-repeat'),('posicion-fondo','center top'),('nav-grad','none')]
        if azul:
            v+=[('nav-grad','none'),('sombra-tarjeta',SOMBRA_AZUL_TARJETA),('sombra-boton',SOMBRA_AZUL_BOTON)]
        o.append(sel+' {\n'+''.join('  --%s: %s;\n'%(k,x) for k,x in v)+'}\n')
        # iconos de la barra inferior (imagenes recoloreadas con el dorado de la paleta)
        o.append(''.join("%s #nav-%s { background-image: url('nav-%s-%s.png'); }\n"%(sel,i,i,n) for i in ('inicio','leer','guia','favoritos')))
    bloque(':root',PALETA_POR_DEFECTO)
    for n in P: bloque(':root[data-tema="%s"]'%n,n)
    o.append("""
/* ===== Derivados comunes (se recalculan con cada paleta) ===== */
:root {
  /* Encabezado y barra inferior: un tono algo mas claro arriba y el color exacto abajo */
  --nav-grad: linear-gradient(180deg, color-mix(in srgb, var(--nav) 90%, #fff) 0%, var(--nav) 100%);
  /* lineas finas doradas: degradado metalico horizontal */
  /* Botones: el color exacto, con un degradado MUY leve hacia mas oscuro (nunca mas claro) */
  --principal-2: color-mix(in srgb, var(--principal) 92%, #000);
  --brillo-boton: inset 0 1px 0 rgba(255,255,255,0.25);
  /* Tarjetas: borde dorado fino y sombra pequena con el color de la paleta */
  --borde: rgba(var(--principal-rgb), 0.28);
  --borde-tarjeta: var(--oro-borde);
  --oro-linea-px: @@LINEA_PX@@;
  --oro-borde-px: @@BORDE_PX@@;
  --sombra-tarjeta: 0 1px 3px rgba(var(--sombra-rgb), 0.16), 0 8px 14px -8px rgba(var(--sombra-rgb), 0.22);
  --texto-suave: color-mix(in srgb, var(--texto) 82%, var(--tarjeta-solida));
  --fondo-exterior: var(--nav);
  --sobre-hero: #FBF3E4;
  /* Velo del encabezado de Inicio: 'nubecita' del color de la paleta, mas fuerte arriba y desvanecida hacia abajo. Intensidad en el borde superior (0-1) */
  --velo-hero-intensidad: @@VELO@@;
}

/* ===== Texturas (Marfil: marmol; Azul clasico: papel/cuero/algodon): llegan al fondo, al encabezado y a la barra inferior de TODAS las pantallas =====
   (las reglas de cada pagina usan 'background' abreviado; aqui se sube la especificidad para que no la pisen) */
:root .phone { isolation: isolate; background-color: var(--fondo); }
:root header:not(.hero) { background: var(--nav-grad); background-color: var(--nav); border-bottom: var(--oro-linea-px) solid transparent; border-image: var(--oro-linea) 1; position: relative; z-index: var(--z-barra); isolation: var(--aislar-barra); }
:root nav { background: var(--nav-grad); background-color: var(--nav); border-top: var(--oro-linea-px) solid transparent; border-image: var(--oro-linea) 1; position: relative; isolation: var(--aislar-barra); }
:root .phone::before, :root header:not(.hero)::before, :root nav::before {
  content: ''; position: absolute; inset: 0; z-index: -1; pointer-events: none; background-repeat: repeat;
}
:root .phone::before { display: var(--fondo-display); background-image: var(--textura-fondo); background-size: var(--tamano-fondo); background-repeat: var(--repeticion-fondo, repeat); background-position: var(--posicion-fondo, 0 0); opacity: var(--intensidad-fondo); }
:root header:not(.hero)::before, :root nav::before { display: var(--barra-display); background-image: var(--textura-barra); background-size: var(--tamano-barra); background-repeat: var(--repeticion-barra); opacity: var(--intensidad-barra); }
:root header:not(.hero)::before { background-position: var(--posicion-encabezado); }
:root nav::before { background-position: var(--posicion-nav); }
/* tinte + degradado vertical leve ENCIMA de la textura de la barra (solo Azul clasico) */
:root header:not(.hero)::after, :root nav::after { content: ''; display: var(--tinte-display); position: absolute; inset: 0; z-index: -1; pointer-events: none; background: var(--barra-tinte); }

/* Los enlaces de la barra inferior nunca van subrayados (Favoritos salia subrayado en Inicio) */
nav a.item, nav a.item:hover, nav a.item:focus, nav a.item:active, nav a.item:visited { text-decoration: none; outline: none; }

/* Iconos de la barra inferior: imagen recoloreada (dorado metalico vivo; bronce en Marfil) con resplandor y una sombra oscura leve */
:root .icono-nav { mix-blend-mode: normal; filter: drop-shadow(0 0 var(--oro-radio) var(--oro-brillo)) drop-shadow(0 1px 1px var(--oro-sombra)); background-size: cover; background-position: center; background-repeat: no-repeat; }
:root .item.activo .icono-nav { filter: drop-shadow(0 0 calc(var(--oro-radio) + 1px) var(--oro-brillo)) drop-shadow(0 0 2px var(--oro-brillo)) drop-shadow(0 1px 1px var(--oro-sombra)); }
:root nav .item.activo { text-shadow: 0 0 8px var(--oro-brillo); }

/* ===== Selector de paleta del menu: cuadricula 3x3 (las 9 sin hacer scroll) ===== */
:root .menu-principal { min-width: 236px; }
:root .submenu-paleta.visible { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; padding: 4px 0 6px; margin: 2px 0 4px; border-left: 0; }
:root .opcion-tema { display: flex; flex-direction: column; align-items: center; justify-content: flex-start; gap: 4px; padding: 6px 3px 5px; font-size: 10.5px; line-height: 1.15; text-align: center; border-radius: 7px; border: 1.5px solid transparent; }
:root .opcion-tema.activo { font-weight: 700; border-color: var(--acento); background: rgba(var(--acento-rgb), 0.18); }
.opcion-tema .nombre-tema { display: block; width: 100%; }
.muestras { display: flex; width: 100%; height: 17px; border-radius: 5px; overflow: hidden; box-shadow: 0 0 0 1px rgba(128,128,128,0.5); }
.muestras i { display: block; flex: 1; }
""")
    o.append("""
/* ===== Azul clasico: textura de algodon en las tarjetas y sombras suaves negras en tarjetas y botones =====
   (solo esta paleta; las tarjetas con campo de texto, menus y popups siguen solidos) */
:root[data-tema="azul"] :is(.versiculo-dia, .tarjeta-oracion, .tarjeta-historia, .tarjeta-mapa, .tarjeta-favorito, .tarjeta-termino, .item-libro, .num-capitulo, .item-guardado) {
  background-image: var(--textura-tarjeta); background-size: var(--tamano-tarjeta); background-repeat: repeat;
}
:root[data-tema="azul"] #vista-detalle .texto-oracion { background-image: var(--textura-tarjeta); background-size: var(--tamano-tarjeta); background-repeat: repeat; }
:root[data-tema="azul"] :is(.pestana.activa, .tab.activo, .btn-leer-pasaje, .btn-copiar-lista, .tarjeta-oracion .simbolo, .btn-ir-verso-flotante, .pin-mapa) {
  box-shadow: var(--sombra-boton), var(--brillo-boton);
}
""")
    for nn,r in REAL.items():
        o.append("""
/* ===== %(nombre)s: papel tenue en las tarjetas (una sola imagen, sin mosaico) y textura oscura en los botones redondos ===== */
:root[data-tema="%(nn)s"] :is(.versiculo-dia, .tarjeta-oracion, .tarjeta-historia, .tarjeta-mapa, .tarjeta-favorito, .tarjeta-termino, .item-libro, .num-capitulo, .item-guardado),
:root[data-tema="%(nn)s"] #vista-detalle .texto-oracion {
  background-image: var(--textura-tarjeta); background-size: var(--tamano-tarjeta); background-repeat: no-repeat; background-position: center top;
}
:root[data-tema="%(nn)s"] :is(.btn-atras, .btn-menu, .btn-tamano, .btn-ir-verso-flotante) {
  background-color: %(color_boton)s; background-image: url('%(boton)s'); background-size: %(tam_boton)s; background-position: center; background-repeat: no-repeat;
}
""" % dict(r,nn=nn,nombre=NOMBRES[nn]))
    return ''.join(o).replace('@@VELO@@',str(VELO_HERO)).replace('@@LINEA_PX@@',ORO_LINEA_PX).replace('@@BORDE_PX@@',ORO_BORDE_PX)

def g_suave(d,te): return mix(d['texto'],te,0.18)

def tabla():
    filas=[]
    for n in P:
        d=derivar(n); te=d['tarjeta_efectiva']
        filas.append((NOMBRES[n],
            cr(d['texto'],te),cr(d['texto'],d['fondo']),cr(d['cita'],te),cr(d['cita'],d['fondo']),
            cr(g_suave(d,te),te),cr(g_suave(d,te),d['fondo']),
            cr(d['sobre_principal'],d['principal']),cr(d['sobre_nav'],d['nav']),cr(d['acento_nav'],d['nav']),cr(d['sobre_nav_suave'],d['nav']),
            cr(d['icono_nav'],d['nav']),cr(d['sobre_oscuro'],d['oscuro']),cr(d['sobre_acento'],d['acento_btn'])))
    return filas

if __name__=='__main__':
    open('temas.css','w',encoding='utf8',newline='\n').write(css())
    cab=['Paleta','texto/tarjeta','texto/fondo','cita/tarjeta','cita/fondo','texto suave/tarjeta','texto suave/fondo','boton (texto/fondo del boton)','titulo en barra','texto dorado en barra (etiqueta activa, subtitulo)','etiqueta inactiva en barra','ICONO en barra (min. 3:1)','chip','boton dorado']
    print('| '+' | '.join(cab)+' |'); print('|'+'---|'*len(cab))
    for f in tabla(): print('| '+' | '.join(str(v) for v in f)+' |')
    for n in P:
        d=derivar(n); print(n,'icono',d['icono_nav'],'(pedido %s)'%P[n][4],'ajustado' if d['icono_ajustado'] else '','cita',d['cita'],'tarjeta efectiva',d['tarjeta_efectiva'])
