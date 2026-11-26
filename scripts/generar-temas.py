# Genera temas.css a partir de las 9 paletas (y calcula los colores derivados).
# Uso: python scripts/generar-temas.py  -> escribe temas.css, imprime la tabla de contraste
# Los iconos de la barra inferior (nav-<icono>-oro|bronce.webp) se generan con scripts/generar-iconos-barra.py
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
'olivo':('#FEF1D6','#FFFDF2','#202815','#354609','#D9A62C'),   # paleta.json del zip (fondo algo menos amarillo que #FFF0C9)
'tierra':('#FAF1E3','#FFFAF0','#392419','#482B1D','#D4A650'),   # paleta.json del zip
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
TEX_PAPEL='texturas/papel_azul_fondo.webp'   # opaco, media exacta #F7F5F0 y grano x3 del papel original (scripts/generar-papel-azul.py)
TEX_ALGODON='texturas/03_papel_blanco_marfil.webp'  # overlay, alfa fijo 7/255
INTENSIDAD_ALGODON=2.5    # idem para las tarjetas
CUERO_BRILLO=0.03        # degradado vertical blanco leve sobre el cuero (arriba)
TAM_PAPEL='256px'; TAM_ALGODON='256px'
# ---- Texturas reales de Turquesa, Borgona, Verde olivo y Tierra (scripts/generar-texturas-<paleta>.py) ----
# cuero: encabezado y barra | papel: fondo (una sola imagen que cubre el telefono) y tarjetas (velo del color de la tarjeta encima) | boton: botones redondos del encabezado y boton flotante de Leer
REAL={
'turquesa':dict(cuero='texturas/cuero_turquesa_realista.webp',papel='texturas/papel_marfil_verdoso.webp',boton='texturas/cuero_turquesa_oscuro.webp',   # media #12616A / #EFF7F5 / #184A51
                i_cuero=1.0,i_papel=1.0,velo_tarjeta=0.65,tam_cuero='500px auto',rep_cuero='no-repeat',tam_papel='cover',tam_tarjeta='600px auto',tam_boton='200px auto',color_boton='#184A51'),
'borgona':dict(cuero='texturas/piedra_borgona.webp',papel='texturas/papel_borgona.webp',boton='texturas/piedra_borgona_oscura.webp',   # media #641D2B / #FAF3EB / #420E20
                i_cuero=1.0,i_papel=1.0,velo_tarjeta=0.65,tam_cuero='500px auto',rep_cuero='no-repeat',pos_barra='right 50%',tam_papel='cover',tam_tarjeta='600px auto',tam_boton='200px auto',color_boton='#420E20'),
# Verde olivo: el encabezado tiene su propia imagen (paisaje, anclado a la derecha) con un degradado oscuro a la izquierda; la barra es una imagen estirada (sin mosaico)
'olivo':dict(cuero='texturas/barra_olivo.webp',papel='texturas/papel_olivo.webp',boton='texturas/piedra_olivo_oscura.webp',   # media #354609 / #FEF1D6 / #213004
             i_cuero=1.0,i_papel=0.7,velo_tarjeta=0.65,tam_cuero='100% 100%',rep_cuero='no-repeat',pos_barra='center',tam_papel='512px auto',rep_fondo='repeat',tam_tarjeta='512px auto',rep_tarjeta='repeat',
             tam_boton='160px auto',color_boton='#213004',tinte='none',encabezado='texturas/encabezado_olivo.webp',pos_imagen_encabezado='85% 0',tam_imagen_encabezado='auto 140%',
             velo_texto='radial-gradient(closest-side, rgba(24,38,5,0.74) 0%, rgba(24,38,5,0.66) 66%, rgba(24,38,5,0) 100%)',
             android='texturas/piedra_olivo_android.webp',
             borde_fondo='linear-gradient(90deg, rgba(236,190,84,0.30) 0%, rgba(236,190,84,0) 16%, rgba(236,190,84,0) 84%, rgba(236,190,84,0.30) 100%)'),
# Tierra biblica: igual que Verde olivo (paisaje en el encabezado, halo solo tras el titulo, barra y piedra arenisca tras los botones de Android)
'tierra':dict(cuero='texturas/piedra_tierra_franja.webp',papel='texturas/papel_tierra.webp',boton='texturas/piedra_tierra_oscura.webp',   # piedra de la franja: scripts/generar-franja-tierra.py
             i_cuero=1.0,i_papel=0.7,velo_tarjeta=0.65,tam_cuero='max(104%, 390px) auto',rep_cuero='no-repeat',pos_barra='center',franja=True,tam_papel='512px auto',rep_fondo='repeat',tam_tarjeta='512px auto',rep_tarjeta='repeat',
             tam_boton='160px auto',color_boton='#45210F',tinte='none',encabezado='texturas/encabezado_tierra.webp',pos_imagen_encabezado='50% 0',tam_imagen_encabezado='cover',
             velo_texto='radial-gradient(closest-side, rgba(43,20,6,0.79) 0%, rgba(43,20,6,0.71) 66%, rgba(43,20,6,0) 100%)',
             inset_velo='-20px -58px -34px',   # arriba mas corto: no apaga el sol
             borde_fondo='linear-gradient(90deg, rgba(222,168,92,0.24) 0%, rgba(222,168,92,0) 16%, rgba(222,168,92,0) 84%, rgba(222,168,92,0.24) 100%)'),
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
    if n in ('olivo','tierra'):
        d['sobre_nav_suave']='#FFFFFF'    # etiquetas blancas como en la referencia
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
            tx=dict(fondo="url('%s')"%TEX_PAPEL,tf=TAM_PAPEL,of='1',barra="url('%s')"%TEX_CUERO,tb=TAM_CUERO,ob='%g'%INTENSIDAD_CUERO,
                    tinte='linear-gradient(180deg, rgba(255,255,255,%.2f), rgba(255,255,255,0))'%CUERO_BRILLO,
                    tarjeta=capas(TEX_ALGODON,max(1,round(INTENSIDAD_ALGODON))),tt=TAM_ALGODON)
        elif turq:
            r=REAL[n]
            tx=dict(fondo="url('%s')"%r['papel'],tf=r['tam_papel'],of='%g'%r['i_papel'],barra="url('%s')"%r['cuero'],tb=r['tam_cuero'],ob='%g'%r['i_cuero'],
                    tinte=r.get('tinte','linear-gradient(180deg, rgba(255,255,255,%.2f), rgba(255,255,255,0))'%CUERO_BRILLO),
                    tarjeta="linear-gradient(rgba(%s,%g), rgba(%s,%g)), url('%s')"%(triple(d['tarjeta']),r['velo_tarjeta'],triple(d['tarjeta']),r['velo_tarjeta'],r['papel']),tt=r['tam_tarjeta'])
            if 'borde_fondo' in r:      # bordes calidos sobre el papel, como en la referencia
                tx['fondo']=r['borde_fondo']+', '+tx['fondo']; tx['tf']='100% 100%, '+tx['tf']
        else:
            tx=dict(fondo='none',tf='auto',of='0',barra='none',tb='auto',ob='0',tinte='none',tarjeta='none',tt='auto')
        rep,posh,posn=((REAL[n]['rep_cuero'] if turq else 'no-repeat'),POS_CUERO_ENCABEZADO,(REAL[n].get('pos_barra',POS_CUERO_BARRA) if turq else POS_CUERO_BARRA)) if (azul or turq) else ('repeat','0 0','0 0')
        v+=[('repeticion-barra',rep),('posicion-encabezado',posh),('posicion-nav',posn),('textura-fondo',tx['fondo']),('tamano-fondo',tx['tf']),('intensidad-fondo',tx['of']),('fondo-display','block' if tx['fondo']!='none' else 'none'),
            ('textura-barra',tx['barra']),('tamano-barra',tx['tb']),('intensidad-barra',tx['ob']),('barra-display','block' if tx['barra']!='none' else 'none'),
            ('barra-tinte',tx['tinte']),('tinte-display','block' if tx['tinte']!='none' else 'none'),
            ('textura-tarjeta',tx['tarjeta']),('tamano-tarjeta',tx['tt']),('intensidad-algodon',str(INTENSIDAD_ALGODON) if azul else '0')]
        # TODAS las paletas fijan la repeticion y la posicion del fondo: si falta, se hereda la de la paleta por defecto (:root),
        # y un papel en mosaico queda dibujado una sola vez (un rectangulo en medio de la pantalla)
        v+=[('repeticion-fondo',(('no-repeat, ' if 'borde_fondo' in REAL[n] else '')+REAL[n].get('rep_fondo','no-repeat')) if turq else 'repeat'),
            ('posicion-fondo','center top' if turq else '0 0')]
        if turq: v+=[('nav-grad','none')]
        if azul:
            v+=[('nav-grad','none'),('sombra-tarjeta',SOMBRA_AZUL_TARJETA),('sombra-boton',SOMBRA_AZUL_BOTON)]
        # fondo de la placa de los iconos de la barra (variante con marco): el de los botones redondos del encabezado; en Marfil, claro (el bronce necesita 3:1)
        if marfil: marco='linear-gradient(180deg, #FFFDF8, #FBF3E2)'
        elif n in REAL: marco="url('%s') center / 160px auto no-repeat %s"%(REAL[n]['boton'],REAL[n]['color_boton'])
        else: marco='linear-gradient(180deg, %s, %s)'%(mix(d['nav'],'#000000',0.28),mix(d['nav'],'#000000',0.42))
        v.append(('marco-fondo',marco))
        # bordes y luz de la placa: la pestana activa se distingue SOLO por el marco (y la etiqueta), nunca por filtros sobre el dibujo
        if marfil:   # barra clara: bordes de bronce; el activo, dorado vivo y grueso
            v+=[('marco-velo','rgba(122,74,31,0.07)'),('marco-borde','rgba(150,98,34,0.78)'),('marco-borde-activo','#B57A0C'),
                ('marco-halo','rgba(226,160,24,0.80)'),('marco-luz','rgba(240,184,60,0.42)')]
        else:
            v+=[('marco-velo','rgba(0,0,0,0.20)'),('marco-borde','rgba(226,185,79,0.74)'),('marco-borde-activo','#FFE9A0'),
                ('marco-halo','rgba(255,214,100,0.85)'),('marco-luz','rgba(255,214,110,0.30)')]
        o.append(sel+' {\n'+''.join('  --%s: %s;\n'%(k,x) for k,x in v)+'}\n')
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
nav .item { -webkit-tap-highlight-color: transparent; }   /* sin el recuadro azul al tocar: quedaba a la vista durante el cambio de pantalla */

/* Iconos de la barra inferior: dibujo recoloreado (dorado metalico; bronce en Marfil) en ::after, sobre una placa redondeada en ::before.
   El dibujo va SIEMPRE nitido (solo una sombra oscura corta, igual en todas las pestanas): la activa se distingue por la placa y la etiqueta.
   --icono-caja es el alto que ocupa en la barra (la barra mide lo mismo: relleno superior + caja + margen = 42px) y --icono-lienzo el lado
   del archivo de 192px, cuyo dibujo ocupa 119/192 del alto. La placa se activa con html[data-marco="si"] (variable MARCO_BARRA en temas.js). */
:root { --icono-caja: 33px; --icono-ancho: 48px; --icono-hueco: 2px; --icono-lienzo: 46.7px; }          /* sin placa: dibujo de 29px de alto */
:root[data-marco="si"] { --icono-caja: 36px; --icono-ancho: 54px; --icono-lienzo: 45.2px; }                /* placa de 54x36, dibujo de 28px, a 4px de la linea */
:root nav { padding-top: calc(42px - var(--icono-caja) - var(--icono-hueco)); }
:root .icono-nav { position: relative; width: var(--icono-ancho); height: var(--icono-caja); margin: 0 auto var(--icono-hueco); }
:root .icono-nav::after { content: ''; position: absolute; left: 50%; top: 50%; width: var(--icono-lienzo); height: var(--icono-lienzo); transform: translate(-50%, -50%); background: center / 100% 100% no-repeat; pointer-events: none; filter: drop-shadow(0 1px 1px var(--oro-sombra)); }
/* placa: como los botones redondos del encabezado; las inactivas con borde tenue y fondo algo apagado */
:root[data-marco="si"] .icono-nav::before { content: ''; position: absolute; inset: 0; box-sizing: border-box; border-radius: 12px; background: linear-gradient(var(--marco-velo), var(--marco-velo)), var(--marco-fondo); border: 1px solid var(--marco-borde); box-shadow: 0 1px 3px var(--oro-sombra); }
/* activa: borde luminoso y grueso, halo detras de la placa y brillo interior leve */
:root[data-marco="si"] .item.activo .icono-nav::before { background: var(--marco-fondo); border: 2px solid var(--marco-borde-activo); box-shadow: 0 0 8px 1px var(--marco-halo), inset 0 0 7px var(--marco-luz); }
:root #nav-inicio::after { background-image: url('nav-inicio-oro.webp'); }
:root #nav-leer::after { background-image: url('nav-leer-oro.webp'); }
:root #nav-guia::after { background-image: url('nav-guia-oro.webp'); }
:root #nav-favoritos::after { background-image: url('nav-favoritos-oro.webp'); }
:root[data-tema="marfil"] #nav-inicio::after { background-image: url('nav-inicio-bronce.webp'); }
:root[data-tema="marfil"] #nav-leer::after { background-image: url('nav-leer-bronce.webp'); }
:root[data-tema="marfil"] #nav-guia::after { background-image: url('nav-guia-bronce.webp'); }
:root[data-tema="marfil"] #nav-favoritos::after { background-image: url('nav-favoritos-bronce.webp'); }
:root nav .item.activo { text-shadow: 0 0 8px var(--oro-brillo); }

/* Mientras llega una lista (si la pantalla se muestra antes que su contenido): siluetas de tarjetas bajo el aviso */
:root .phone .cargando::after { content: ''; display: block; width: 100%; height: 430px; margin-top: 14px; border-radius: 14px;
  background: repeating-linear-gradient(180deg, rgba(var(--principal-rgb), 0.09) 0 74px, transparent 74px 86px); }

/* ===== Pulsacion de botones (todas las pantallas y paletas) =====
   Sin el rectangulo azulado con que Android resalta el toque, ni contorno de foco al tocar con el dedo (con teclado,
   :focus-visible conserva su contorno). El efecto propio sigue la forma de cada boton y no cambia su fondo ni su textura. */
:root, :root * { -webkit-tap-highlight-color: transparent; }
:root :focus:not(:focus-visible) { outline: none; }
:root :is(.btn-atras, .btn-menu, .btn-tamano, .btn-ir-verso-flotante, .flecha-carrusel, .visor-cerrar, .pin-mapa, .estrella-fav, .compartir-verso, .nota-btn,
  .btn-buscar, .btn-nav-cap, .btn-overlay, .btn-confirmar, .btn-copiar-lista, .btn-leer-pasaje, .btn-suscribirse, .btn-cerrar-overlay, .btn-quitar, .btn-escala-fila,
  .tab, .pestana, .tab-legal, .num-capitulo, .item-libro, .tarjeta-oracion, .tarjeta-historia, .tarjeta-mapa, .tarjeta-favorito, .item-guardado) {
  -webkit-user-select: none; user-select: none; -webkit-touch-callout: none;   /* mantener el dedo no selecciona la letra del boton */
}
/* redondos: se encogen, se oscurecen un poco y muestran un halo dorado (el contorno sigue el border-radius) */
:root :is(.btn-atras, .btn-menu, .btn-tamano, .btn-ir-verso-flotante, .flecha-carrusel, .visor-cerrar, .pin-mapa, .estrella-fav, .compartir-verso, .nota-btn):active {
  scale: 0.95; filter: brightness(0.9); outline: 3px solid rgba(231, 188, 84, 0.55); outline-offset: 0;
}
/* demas botones: se encogen y oscurecen levemente */
:root :is(.btn-buscar, .btn-nav-cap, .btn-overlay, .btn-confirmar, .btn-copiar-lista, .btn-leer-pasaje, .btn-suscribirse, .tab, .pestana, .tab-legal, .num-capitulo):active {
  scale: 0.97; filter: brightness(0.92);
}
/* tarjetas y filas: solo oscurecimiento leve */
:root :is(.item-libro, .tarjeta-oracion, .tarjeta-historia, .tarjeta-mapa, .tarjeta-favorito, .item-guardado, .libro-busqueda, .resultado-verso, .fila-enlace, .btn-cerrar-overlay):active {
  filter: brightness(0.94);
}

/* ===== Mantener el dedo sobre la navegacion: sin el aviso con la direccion del enlace ni menu del sistema =====
   (el aviso es la sombra de arrastre de un <a href>; temas.js ademas anula 'dragstart' y 'contextmenu') */
:root a, :root img { -webkit-user-drag: none; -webkit-touch-callout: none; }
:root :is(a, header, nav, .tarjeta-termino) { -webkit-user-select: none; user-select: none; -webkit-touch-callout: none; }

/* ===== Glosario: buscador y contador fijos, sin que el texto pase por detras =====
   La lista tiene su propio desplazamiento DEBAJO del bloque: nada queda tras el buscador, el contador ni el hueco bajo el encabezado,
   y el fondo del bloque es el mismo de la pantalla (color y textura de papel de cada paleta), sin capas encima. */
:root main:has(.caja-busqueda-glosario) { display: flex; flex-direction: column; overflow: hidden; padding-bottom: 0; }
:root .caja-busqueda-glosario { position: static; flex: 0 0 auto; background: transparent; margin-bottom: 0; }
:root #lista-glosario { flex: 1 1 auto; min-height: 0; overflow-y: auto; margin: 0 -5vw; padding: 0.4vh 5vw 3vh;
  scrollbar-width: thin; scrollbar-color: rgba(var(--principal-rgb),0.65) rgba(var(--principal-rgb),0.08); }
:root .contador-glosario { font-family: 'Source Serif 4', serif; }

/* ===== Recuadro de publicidad: igual en todas las pantallas (como en Leer) ===== */
:root .contenido-ads { width: 100%; }
:root .contenido-ads .marcador { font-family: 'Cinzel', serif; font-weight: 600; font-size: 10.5px; letter-spacing: 0.3px; }
/* la etiqueta va montada sobre el borde superior y el texto queda debajo, separado */
:root .phone .espacio-publicidad { margin-top: 7px; padding-top: 13px; padding-bottom: 3px; min-height: 50px; overflow: visible; z-index: 4; }
:root .phone .etiqueta-ads { top: -8px; left: 14px; font-size: 7.5px; line-height: 10px; padding: 2px 8px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
:root .contenido-ads .marcador { line-height: 1.35; }
:root .contenido-ads .marcador-sub { font-size: 9px; line-height: 1.3; }

/* ===== Titulo del encabezado: en Tierra va 12px mas arriba (con su subtitulo). Los titulos que no caben en su columna
   (temas.js les pone .titulo-ancho) se quedan en una linea y pasan POR ENCIMA de los botones de buscar y A-/A+ ===== */
:root[data-tema="tierra"] header:not(.hero) > div:has(> #titulo-header) { top: -12px; }
:root header:not(.hero) > div:has(> #titulo-header) { min-width: 0; }
:root header:not(.hero) #titulo-header.titulo-ancho { white-space: nowrap; width: max-content; position: relative; }

/* ===== Numeros de versiculo (todas las paletas): letra serif de la app en negrita, sobre la linea, con subrayado dorado fino ===== */
:root .phone .verso .num { display: inline-block; font-family: 'Source Serif 4', serif; font-weight: 700; font-size: 0.86em; line-height: 1.1;
  vertical-align: baseline; color: var(--cita); padding: 0 1px 1px; margin-right: 6px; border-bottom: 1.5px solid var(--oro-borde); }

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
  background-image: var(--textura-tarjeta); background-size: var(--tamano-tarjeta); background-repeat: %(rep_tarjeta)s; background-position: center top;
}
:root[data-tema="%(nn)s"] :is(.btn-atras, .btn-menu, .btn-tamano, .btn-ir-verso-flotante) {
  background-color: %(color_boton)s; background-image: url('%(boton)s'); background-size: %(tam_boton)s; background-position: center; background-repeat: no-repeat;
}
""" % dict(dict(rep_tarjeta='no-repeat'),**dict(r,nn=nn,nombre=NOMBRES[nn])))
        if 'encabezado' in r:
            o.append("""/* %(nombre)s: imagen propia en el encabezado (cover, anclada a la derecha), sin velo sobre el paisaje */
:root[data-tema="%(nn)s"] header:not(.hero)::before {
  background-image: url('%(encabezado)s'); background-size: %(tam_imagen_encabezado)s; background-position: %(pos_imagen_encabezado)s; background-repeat: no-repeat;
}
/* %(nombre)s: oscurecimiento suave SOLO detras del titulo y el subtitulo (sigue el tamano de su caja) */
:root[data-tema="%(nn)s"] header:not(.hero) > div:has(> #titulo-header) { position: relative; }
:root[data-tema="%(nn)s"] header:not(.hero) > div:has(> #titulo-header)::before {
  content: ''; position: absolute; inset: %(inset_velo)s; clip-path: inset(0 0 calc(34px - 1.4vh) 0); z-index: -1; pointer-events: none; background: %(velo_texto)s;
}
/* %(nombre)s: botones con borde dorado vivo */
:root[data-tema="%(nn)s"] :is(.btn-atras, .btn-menu, .btn-tamano, .btn-ir-verso-flotante) { border: var(--oro-borde-px) solid var(--oro-borde); }
""" % dict(dict(inset_velo='-34px -58px'),**dict(r,nn=nn,nombre=NOMBRES[nn])))
        if 'android' in r:
            o.append("""/* %(nombre)s: %(material_android)s en la zona de los botones de Android (debajo de la barra inferior), separada por una linea dorada */
:root[data-tema="%(nn)s"] nav::after {
  display: block; top: auto; height: max(0px, calc(env(safe-area-inset-bottom) - 6px));
  background: var(--oro-linea) top / 100%% 2px no-repeat, linear-gradient(180deg, rgba(%(sombra_android)s,0.55) 0%%, rgba(%(sombra_android)s,0) 40%%), url('%(android)s') center / cover no-repeat;
}
""" % dict(dict(material_android='piedra verde',sombra_android='24,38,5'),**dict(r,nn=nn,nombre=NOMBRES[nn])))
        if r.get('franja'):
            o.append(FRANJA % dict(nn=nn,nombre=NOMBRES[nn]))
    return ''.join(o).replace('@@VELO@@',str(VELO_HERO)).replace('@@LINEA_PX@@',ORO_LINEA_PX).replace('@@BORDE_PX@@',ORO_BORDE_PX)

# Franja inferior de una sola superficie de piedra (barra de la app + zona de Android) con la barra enmarcada en oro.
# Capas dentro de nav: ::before piedra (-3), ::after marco (-2), separadores y luz de la pestana activa (-1).
FRANJA="""/* ===== %(nombre)s: franja inferior: una sola piedra hasta el borde de la pantalla y marco dorado alrededor de la barra ===== */
:root[data-tema="%(nn)s"] nav { background: transparent; border: 0; padding-top: 7px; padding-left: 8px; padding-right: 8px; isolation: isolate; }
:root[data-tema="%(nn)s"] nav::before { top: 1px; z-index: -3; border-radius: 26px 26px 0 0; background-color: var(--nav);
  /* un velo calido hacia abajo para que los botones blancos de Android se lean sobre las piedras claras */
  background-image: linear-gradient(180deg, rgba(36,18,7,0) 45%%, rgba(36,18,7,0.42) 100%%), var(--textura-barra); background-size: 100%% 100%%, var(--tamano-barra); background-position: center, center; }
:root[data-tema="%(nn)s"] nav::after { content: ''; display: block; position: absolute; z-index: -2; box-sizing: border-box; pointer-events: none;
  top: 1px; left: 3px; right: 3px; bottom: max(3px, calc(env(safe-area-inset-bottom) - 6px)); height: auto; border-radius: 24px;
  border: 3px solid; border-color: #FFE08A #EDB83F #F7C443;
  background: linear-gradient(180deg, rgba(36,18,7,0.22), rgba(36,18,7,0.36));
  box-shadow: 0 0 0 1px #8A6420, inset 0 0 0 1px rgba(138,100,32,0.9), inset 0 0 6px rgba(245,214,139,0.35), 0 3px 6px rgba(36,18,7,0.6); }
:root[data-tema="%(nn)s"] nav .item { position: relative; flex: 1 1 0; min-width: 0; min-height: 48px; color: #FFFDF2;
  text-shadow: 0 1px 2px rgba(24,10,2,1), 0 0 5px rgba(24,10,2,0.95); }
:root[data-tema="%(nn)s"] nav .item + .item::before { content: ''; position: absolute; z-index: -1; left: 0; top: 5px; bottom: 3px; width: 1px;
  background: linear-gradient(180deg, transparent, #E8C46A 30%%, #E8C46A 70%%, transparent); }
/* solo la seccion activa: fondo calido y luz dorada abajo */
:root[data-tema="%(nn)s"] nav .item.activo::after { content: ''; position: absolute; z-index: -1; left: 3px; right: 3px; top: -1px; bottom: -3px; border-radius: 12px; pointer-events: none;
  background: radial-gradient(closest-side, #FFFFFF 0%%, rgba(255,226,130,0.9) 35%%, rgba(255,190,60,0) 100%%) bottom center / 34px 9px no-repeat,
    linear-gradient(90deg, transparent, #FFD560 25%%, #FFF6C8 50%%, #FFD560 75%%, transparent) bottom 3px center / 90%% 2px no-repeat,
    radial-gradient(75%% 60%% at 50%% 100%%, rgba(255,182,45,0.80), rgba(255,150,30,0) 100%%),
    linear-gradient(180deg, rgba(70,28,2,0.45), rgba(170,82,8,0.62)); }
@media (max-width: 340px) { :root[data-tema="%(nn)s"] nav .item { font-size: 9.5px; letter-spacing: 0.1px; } }   /* telefonos muy angostos: FAVORITOS no toca el marco */
/* iconos dorados directamente sobre la piedra (sin placa), un poco mayores */
:root[data-tema="%(nn)s"] nav .item .icono-nav::before { display: none; }
:root[data-tema="%(nn)s"] nav .item .icono-nav::after { width: 50px; height: 50px; filter: drop-shadow(0 1px 1px rgba(24,10,2,1)) drop-shadow(0 0 3px rgba(24,10,2,0.8)); }
"""

def critico():
    """colores de fondo y de barra en linea en el <head> de cada pantalla: se aplican aunque temas.css o las imagenes tarden"""
    c = lambda n: '--critico-fondo:%s;--critico-barra:%s' % (P[n][0], P[n][3])
    reglas = ['html{%s;background:var(--critico-barra)}' % c(PALETA_POR_DEFECTO)] + ['html[data-tema="%s"]{%s}' % (n, c(n)) for n in P]
    reglas.append('.phone{background:var(--critico-fondo)}:where(header:not(.hero)),nav{background:var(--critico-barra)}')
    return '<style id="critico">/* generado por scripts/generar-temas.py */\n' + '\n'.join(reglas) + '\n</style>'

def escribir_critico():
    import glob, re
    for p in sorted(glob.glob('*.html')):
        s = open(p, encoding='utf8', newline='').read()
        nl = '\r\n' if '\r\n' in s else '\n'
        bloque = critico().replace('\n', nl)
        if '<style id="critico">' in s: n = re.sub(r'<style id="critico">.*?</style>', lambda m: bloque, s, flags=re.S)
        else: n = s.replace('<head>' + nl, '<head>' + nl + bloque + nl, 1)
        assert '<style id="critico">' in n, p
        if n != s: open(p, 'w', encoding='utf8', newline='').write(n)

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
    escribir_critico()
    cab=['Paleta','texto/tarjeta','texto/fondo','cita/tarjeta','cita/fondo','texto suave/tarjeta','texto suave/fondo','boton (texto/fondo del boton)','titulo en barra','texto dorado en barra (etiqueta activa, subtitulo)','etiqueta inactiva en barra','ICONO en barra (min. 3:1)','chip','boton dorado']
    print('| '+' | '.join(cab)+' |'); print('|'+'---|'*len(cab))
    for f in tabla(): print('| '+' | '.join(str(v) for v in f)+' |')
    for n in P:
        d=derivar(n); print(n,'icono',d['icono_nav'],'(pedido %s)'%P[n][4],'ajustado' if d['icono_ajustado'] else '','cita',d['cita'],'tarjeta efectiva',d['tarjeta_efectiva'])
