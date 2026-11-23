# Genera temas.css a partir de las 9 paletas (y calcula los colores derivados).
# Uso: python scripts/generar-temas.py  -> escribe temas.css e imprime la tabla de contraste
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

NOMBRES={'azul':'Azul clásico','borgona':'Borgoña real','olivo':'Verde olivo','tierra':'Tierra bíblica','purpura':'Púrpura espiritual','turquesa':'Turquesa renovación','nocturna':'Nocturna','marfil':'Marfil clásico','ambar':'Ámbar inspirador'}
P={ # fondo, tarjeta, texto, nav, acento
'azul':('#F3F5F8','#FFFFFF','#24354B','#18365B','#D6A84E'),
'borgona':('#FAF3EB','#FFFDF7','#56202B','#641D2B','#D5A348'),
'olivo':('#F4F3E7','#FFFDF5','#2E4129','#344C2B','#C9A34E'),
'tierra':('#F8F0E5','#FFF9EF','#543526','#78452D','#D9A54D'),
'purpura':('#F6F2F8','#FFFFFF','#49325F','#49325F','#D7AD58'),
'turquesa':('#EFF7F5','#FFFFFF','#184A51','#12616A','#D6AC55'),
'nocturna':('#18212D','#293545','#F5F0E5','#202A38','#D5AC60'),
'marfil':('#FCF8EF','#FFFFFF','#59392D','#F2E7D1','#A96835'),
'ambar':('#FFF3E5','#FFFCF6','#71391F','#93421D','#D7A044')}

def derivar(n):
    f,t,x,nv,a=P[n]
    d=dict(fondo=f,tarjeta=t,texto=x,nav=nv,acento=a)
    if n=='marfil':
        d['sobre_nav']=x
        d['sobre_nav_suave']=mix(x,nv,0.1)
        d['acento_nav']=hasta(a,'#000000',[nv],4.6)
        d['icono_nav']=d['acento_nav']
        d['principal']=x; d['sobre_principal']='#FFFFFF'
        d['cita']=hasta(a,'#000000',[t,f],4.6)
        d['oscuro']=x; d['sobre_oscuro']=nv
        d['sobre_acento']='#FFFFFF'; d['acento_btn']=d['cita']
        d['hero']=x
        d['btn_nav_bg']='rgba(%s,0.08)'%triple(x); d['btn_nav_borde']='rgba(%s,0.55)'%triple(a)
    elif n=='nocturna':
        d['sobre_nav']='#FFFFFF'
        d['sobre_nav_suave']=hasta(mix('#FFFFFF',nv,0.3),'#FFFFFF',[nv],4.6)
        d['acento_nav']=hasta(a,'#FFFFFF',[nv],4.6); d['icono_nav']=d['acento_nav']
        d['principal']=a; d['sobre_principal']=f
        d['cita']=hasta(a,'#FFFFFF',[t,f],4.6)
        d['oscuro']=nv; d['sobre_oscuro']=d['acento_nav']
        d['sobre_acento']=f
        d['hero']=nv
        d['btn_nav_bg']='rgba(255,255,255,0.10)'; d['btn_nav_borde']='rgba(%s,0.5)'%triple(a)
    else:
        d['sobre_nav']='#FFFFFF'
        d['sobre_nav_suave']=hasta(mix('#FFFFFF',nv,0.3),'#FFFFFF',[nv],4.6)
        d['acento_nav']=hasta(a,'#FFFFFF',[nv],4.6)
        d['icono_nav']=d['acento_nav']
        d['principal']=nv
        d['sobre_principal']='#FFFFFF'
        d['cita']=d['principal']
        d['oscuro']=nv; d['sobre_oscuro']=d['acento_nav']
        d['sobre_acento']=x
        d['hero']=nv
        d['btn_nav_bg']='rgba(255,255,255,0.12)'; d['btn_nav_borde']='rgba(%s,0.5)'%triple(a)
    d.setdefault('acento_btn',a)
    if n!='marfil': d['sobre_acento']=hasta(x if L(x)<0.5 else f,'#000000' if L(x)<0.5 else '#FFFFFF',[d['acento_btn']],4.6)
    return d

def css():
    o=['/* GENERADO por scripts/generar-temas.py: no editar a mano. 9 paletas; la de por defecto es Purpura espiritual. */\n']
    def bloque(sel,n):
        d=derivar(n)
        v=[('fondo',d['fondo']),('tarjeta',d['tarjeta']),('texto',d['texto']),('nav',d['nav']),('acento',d['acento']),
           ('sobre-nav',d['sobre_nav']),('sobre-nav-suave',d['sobre_nav_suave']),('acento-nav',d['acento_nav']),('icono-nav',d['icono_nav']),
           ('principal',d['principal']),('sobre-principal',d['sobre_principal']),('cita',d['cita']),
           ('oscuro',d['oscuro']),('sobre-oscuro',d['sobre_oscuro']),('sobre-acento',d['sobre_acento']),('acento-btn',d['acento_btn']),
           ('btn-nav-bg',d['btn_nav_bg']),('btn-nav-borde',d['btn_nav_borde']),
           ('principal-rgb',triple(d['principal'])),('texto-rgb',triple(d['texto'])),('acento-rgb',triple(d['acento'])),('hero-rgb',triple(d['hero'])),('titulo-rollo','#3B2A1C' if n=='nocturna' else (d['texto'] if n=='marfil' else d['nav'])),('tarjeta-rgb',triple(d['tarjeta'])),('sombra-rgb','0,0,0' if n=='nocturna' else triple(d['texto'])),('palabras-jesus','#FF9A8F' if n=='nocturna' else '#9B1024'),
           ('textura',"url('marmol_marfil_2026-11-22_2110.webp')" if n=='marfil' else 'none')]
        o.append(sel+' {\n'+''.join('  --%s: %s;\n'%(k,x) for k,x in v)+'}\n')
    bloque(':root','purpura')
    for n in P: bloque(':root[data-tema="%s"]'%n,n)
    o.append("""
/* Derivados comunes (se recalculan con cada paleta) */
:root {
  --nav-grad: linear-gradient(135deg, var(--nav) 0%, color-mix(in srgb, var(--nav) 92%, #000) 100%);
  --principal-2: color-mix(in srgb, var(--principal) 84%, #fff);
  --texto-suave: color-mix(in srgb, var(--texto) 82%, var(--tarjeta));
  --borde: rgba(var(--principal-rgb), 0.28);
  --fondo-exterior: var(--nav);
  --sobre-hero: #FBF3E4;
  --tamano-textura: 600px;
}
/* Textura (solo Marfil: en las demas paletas --textura vale none) */
.phone { background-color: var(--fondo); background-image: var(--textura); background-size: var(--tamano-textura); background-repeat: repeat; }
header:not(.hero), nav { background-image: var(--textura), var(--nav-grad); background-size: var(--tamano-textura), auto; background-color: var(--nav); }

/* Los enlaces de la barra inferior nunca van subrayados (Favoritos salia subrayado en Inicio) */
nav a.item, nav a.item:hover, nav a.item:focus, nav a.item:active, nav a.item:visited { text-decoration: none; outline: none; }

/* Iconos de la barra inferior: silueta (mascara) pintada con el color de icono de cada paleta */
.icono-nav { background: var(--icono-nav) !important; mix-blend-mode: normal !important; filter: none !important;
  -webkit-mask-size: cover; mask-size: cover; -webkit-mask-repeat: no-repeat; mask-repeat: no-repeat; -webkit-mask-position: center; mask-position: center; }
.item.activo .icono-nav { filter: drop-shadow(0 0 4px rgba(var(--acento-rgb), 0.55)) !important; }
#nav-inicio { -webkit-mask-image: url('nav-inicio-mascara.png'); mask-image: url('nav-inicio-mascara.png'); background-image: none !important; }
#nav-leer { -webkit-mask-image: url('nav-leer-mascara.png'); mask-image: url('nav-leer-mascara.png'); background-image: none !important; }
#nav-guia { -webkit-mask-image: url('nav-guia-mascara.png'); mask-image: url('nav-guia-mascara.png'); background-image: none !important; }
#nav-favoritos { -webkit-mask-image: url('nav-favoritos-mascara.png'); mask-image: url('nav-favoritos-mascara.png'); background-image: none !important; }

/* Selector de paleta del menu */
.opcion-tema .nombre-tema { flex: 1; min-width: 0; }
.muestras { display: flex; flex-shrink: 0; border-radius: 5px; overflow: hidden; box-shadow: 0 0 0 1px rgba(128,128,128,0.45); }
.muestras i { display: block; width: 14px; height: 18px; }
""")
    return ''.join(o)

def tabla():
    filas=[]
    for n in P:
        d=derivar(n)
        filas.append((NOMBRES[n],
            cr(d['texto'],d['tarjeta']),cr(d['texto'],d['fondo']),cr(d['cita'],d['tarjeta']),cr(d['cita'],d['fondo']),
            cr(d['sobre_principal'],d['principal']),cr(d['sobre_nav'],d['nav']),cr(d['icono_nav'],d['nav']),cr(d['sobre_nav_suave'],d['nav']),cr(d['sobre_oscuro'],d['oscuro']),cr(d['sobre_acento'],d['acento_btn'])))
    return filas

if __name__=='__main__':
    open('temas.css','w',encoding='utf8',newline='\n').write(css())
    print('| Paleta | texto/tarjeta | texto/fondo | cita/tarjeta | cita/fondo | boton | titulo nav | icono nav | etiqueta inactiva nav | chip | boton dorado |')
    for f in tabla(): print('| '+' | '.join(str(v) for v in f)+' |')
    for n in P:
        d=derivar(n); print(n,{k:d[k] for k in ['acento_nav','icono_nav','sobre_nav_suave','cita','principal']})
