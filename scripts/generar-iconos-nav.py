# Genera los iconos de la barra inferior de cada paleta (nav-<icono>-<paleta>.png) y la textura fuerte del marmol
# a partir de los originales nav-<icono>.png (dorado sobre negro) y marmol_marfil_2026-11-22_2110.webp.
# Uso: python scripts/generar-iconos-nav.py   (despues de cambiar colores en generar-temas.py)
import importlib.util, os
from PIL import Image
RAIZ=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')
spec=importlib.util.spec_from_file_location('g',os.path.join(RAIZ,'scripts','generar-temas.py')); g=importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

def recolorear(origen, color_hex, salida, tam=120):
    """Conserva el dibujo y su brillo original; el trazo luminoso toma el color EXACTO de la paleta
    (las luces mas fuertes se aclaran un poco) y lo oscuro pasa a transparente."""
    im=Image.open(origen).convert('RGB').resize((tam,tam),Image.LANCZOS)
    c=g.rgb(color_hex)
    px=im.load(); out=Image.new('RGBA',(tam,tam)); po=out.load()
    for y in range(tam):
        for x in range(tam):
            r,gg,b=px[x,y]
            t=(0.299*r+0.587*gg+0.114*b)/255.0
            alfa=min(1.0,t/0.5)**0.85
            luz=max(0.0,(t-0.72)/0.28)*0.30          # solo las luces mas fuertes se aclaran
            col=[ci+(255-ci)*luz for ci in c]
            po[x,y]=(int(col[0]),int(col[1]),int(col[2]),int(alfa*255))
    out.save(salida,optimize=True)

for n in g.P:
    d=g.derivar(n)
    for i in ('inicio','leer','guia','favoritos'):
        recolorear(os.path.join(RAIZ,'nav-%s.png'%i), d['icono_nav'], os.path.join(RAIZ,'nav-%s-%s.png'%(i,n)))

# Textura fuerte: el original tiene alfa maximo 110/255 (promedio ~4 %); se multiplica x4 (la intensidad se ajusta con --intensidad-marmol)
m=Image.open(os.path.join(RAIZ,'marmol_marfil_2026-11-22_2110.webp')).convert('RGBA')
a=m.getchannel('A').point(lambda v:min(255,int(v*4.0)))
m.putalpha(a); m.save(os.path.join(RAIZ,'marmol_marfil_fuerte.webp'),quality=88,method=6)
print('ok')
