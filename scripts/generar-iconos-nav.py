# OBSOLETO para los iconos: la barra usa scripts/generar-iconos-barra.py (los nav-<icono>-<paleta>.png ya no se referencian).
# Sigue sirviendo para generar marmol_marfil_fuerte.webp.
# Genera los iconos de la barra inferior de cada paleta (nav-<icono>-<paleta>.png) y la textura fuerte del marmol
# a partir de los originales nav-<icono>.png (dorado sobre negro) y marmol_marfil_2026-11-22_2110.webp.
# Uso: python scripts/generar-iconos-nav.py   (despues de cambiar colores en generar-temas.py)
import importlib.util, os
from PIL import Image
RAIZ=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
spec=importlib.util.spec_from_file_location('g',os.path.join(RAIZ,'scripts','generar-temas.py')); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

RAMPA_VIVO=[(0.0,'#7A5A18'),(0.35,'#E2B94F'),(0.62,'#F0CF72'),(1.0,'#FFF1B8')]   # dorado metalico: sombra, cuerpo, luz
RAMPA_BRONCE=[(0.0,'#5E3612'),(0.5,'#7A4A1F'),(0.85,'#9C6628'),(1.0,'#B07A33')]       # bronce: nunca mas claro que #B07A33 (3:1 sobre la barra de Marfil)

def color_rampa(rampa,t):
    for (t0,c0),(t1,c1) in zip(rampa,rampa[1:]):
        if t<=t1:
            u=(t-t0)/(t1-t0) if t1>t0 else 0
            a,b=g.rgb(c0),g.rgb(c1)
            return [a[k]+(b[k]-a[k])*u for k in range(3)]
    return g.rgb(rampa[-1][1])

def recolorear(origen, rampa, salida, tam=120):
    """Parte del dibujo original con su brillo: la luminancia original (sombras, cuerpo, luces) recorre la rampa de color
    y lo oscuro pasa a transparente. No son siluetas planas."""
    im=Image.open(origen).convert('RGB').resize((tam,tam),Image.LANCZOS)
    px=im.load(); out=Image.new('RGBA',(tam,tam)); po=out.load()
    for y in range(tam):
        for x in range(tam):
            r,gg,b=px[x,y]
            t=(0.299*r+0.587*gg+0.114*b)/255.0
            alfa=min(1.0,t/0.45)**0.8
            c=color_rampa(rampa,t)
            po[x,y]=(int(c[0]),int(c[1]),int(c[2]),int(alfa*255))
    out.save(salida,optimize=True)

for n in g.P:
    d=g.derivar(n)
    for i in ('inicio','leer','guia','favoritos'):
        recolorear(os.path.join(RAIZ,'nav-%s.png'%i), RAMPA_BRONCE if d['icono_tipo']=='bronce' else RAMPA_VIVO, os.path.join(RAIZ,'nav-%s-%s.png'%(i,n)))

# Textura fuerte: el original tiene alfa maximo 110/255 (promedio ~4 %); se multiplica x4 (la intensidad se ajusta con --intensidad-marmol)
m=Image.open(os.path.join(RAIZ,'marmol_marfil_2026-11-22_2110.webp')).convert('RGBA')
a=m.getchannel('A').point(lambda v:min(255,int(v*4.0)))
m.putalpha(a); m.save(os.path.join(RAIZ,'marmol_marfil_fuerte.webp'),quality=88,method=6)
print('ok')
