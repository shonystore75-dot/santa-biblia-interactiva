# Prepara las texturas de Verde olivo a partir del zip Texturas_Verde_Olivo_Santa_Biblia_2026 (mismo metodo aditivo que Turquesa).
# Los mosaicos del zip son REFLEJADOS: para la barra y los botones se usa UN SOLO cuadrante (sin espejo ni mosaico);
# la piedra de la zona Android se arma con parches al azar de un cuadrante (semilla fija).
# Entrada: carpeta Verde_Olivo_Santa_Biblia_2026 (zip extraido FUERA del repo)
# Salida: texturas/encabezado_olivo.webp, barra_olivo.webp, papel_olivo.webp, piedra_olivo_oscura.webp, piedra_olivo_android.webp
# Uso: python scripts/generar-texturas-olivo.py <carpeta extraida>     (imprime tamanos, colores y contraste sobre cada textura)
import sys, os, random
from PIL import Image, ImageDraw, ImageFilter, ImageStat

PRINCIPAL=(0x35,0x46,0x09); PROFUNDO=(0x18,0x26,0x05)
MARFIL=(0xFE,0xF1,0xD6)          # un poco menos amarillo que paleta.json (#FFF0C9), igual al centro de lectura de la referencia
BOTON=(0x21,0x30,0x04)           # como los botones de la referencia
BARRA=(0x2C,0x3C,0x05)           # centro de la barra en la referencia (algo mas oscuro que #354609)
ANDROID=(0x36,0x45,0x04)         # piedra verde detras de los botones de Android
TINTA='#202815'; ORO_TEXTO='#F0D27A'; ORO_ICONO='#F0CF72'
# degradado oscuro del encabezado (debe coincidir con el de generar-temas.py): (posicion 0-1, opacidad de #182605)
VELO_ENCABEZADO=[(0,0.55),(0.44,0.52),(0.68,0.0),(1,0.0)]

def contraste_de_media(im,k):
    """k<1 suaviza el grano alrededor de la media."""
    m=ImageStat.Stat(im).mean
    return Image.merge('RGB',[c.point([max(0,min(255,round(m[i]+(v-m[i])*k))) for v in range(256)]) for i,c in enumerate(im.split())])

def a_media(im,obj):
    """Desplazamiento aditivo por canal hasta la media objetivo (dos pasadas para compensar el recorte en 0)."""
    for _ in range(3):
        media=ImageStat.Stat(im).mean; d=[round(obj[c]-media[c]) for c in range(3)]
        im=im.point(sum([[max(0,min(255,v+d[c])) for v in range(256)] for c in range(3)],[]))
    return im

def encabezado(base):
    return Image.open(os.path.join(base,'01_encabezado/fondo_reconstruido/recurso.png')).convert('RGB')

def barra(base):
    im=Image.open(os.path.join(base,'04_verde_barra/recurso.png')).convert('RGB')
    im=im.crop((0,96,256,416)).resize((1000,240),Image.BICUBIC)        # medio ancho: sin espejo
    im=contraste_de_media(im,0.6)
    # degradado vertical hacia olivo profundo (nada arriba, 60 % abajo)
    rampa=Image.new('L',(1,240)); rampa.putdata([round(255*0.60*(y/239)**1.2) for y in range(240)])
    im=Image.composite(Image.new('RGB',im.size,PROFUNDO),im,rampa.resize(im.size))
    return a_media(im,BARRA)

def papel(base):
    im=Image.open(os.path.join(base,'02_papel_marfil/recurso.png')).convert('RGB')     # 512, tamano nativo
    return a_media(im,MARFIL)

def boton(base):
    im=Image.open(os.path.join(base,'03_piedra_olivo_android/recurso.png')).convert('RGB')
    im=im.crop((30,30,222,222))                                        # un cuadrante, sin el rombo central ni el borde oscuro
    return a_media(contraste_de_media(im,0.65),BOTON)

def android(base):
    im=Image.open(os.path.join(base,'03_piedra_olivo_android/recurso.png')).convert('RGB').crop((24,24,232,150))   # parte pareja de un cuadrante
    rnd=random.Random(5); L=(1000,160); P=96
    lienzo=im.resize(L,Image.BICUBIC)
    mascara=Image.new('L',(P,P),0); ImageDraw.Draw(mascara).ellipse((14,14,P-14,P-14),fill=255); mascara=mascara.filter(ImageFilter.GaussianBlur(8))
    for y in range(-40,L[1],34):
        for x in range(-40,L[0],34):
            sx=rnd.randint(0,im.width-P); sy=rnd.randint(0,im.height-P); parche=im.crop((sx,sy,sx+P,sy+P))
            if rnd.random()<0.5: parche=parche.transpose(Image.FLIP_LEFT_RIGHT)
            if rnd.random()<0.5: parche=parche.transpose(Image.FLIP_TOP_BOTTOM)
            lienzo.paste(parche,(x+rnd.randint(-12,12),y+rnd.randint(-12,12)),mascara)
    return a_media(contraste_de_media(lienzo,0.8),ANDROID)

TRABAJOS=[(encabezado,'texturas/encabezado_olivo.webp',90),(barra,'texturas/barra_olivo.webp',82),
          (papel,'texturas/papel_olivo.webp',82),(boton,'texturas/piedra_olivo_oscura.webp',82),
          (android,'texturas/piedra_olivo_android.webp',80)]

# ---- contraste sobre las texturas ----
def lum(c):
    c=[v/255 for v in c]
    c=[x/12.92 if x<=.03928 else ((x+.055)/1.055)**2.4 for x in c]
    return .2126*c[0]+.7152*c[1]+.0722*c[2]
def rgb(h): return tuple(int(h[i:i+2],16) for i in (1,3,5))
def peor(texto,im):
    """contraste contra el 1 % de pixeles menos favorable, y contra la mediana"""
    t=lum(rgb(texto)); L=sorted(lum(p) for p in im.getdata())
    cr=lambda a,b:(max(a,b)+.05)/(min(a,b)+.05)
    mala=L[int(len(L)*0.99)] if t>L[len(L)//2] else L[int(len(L)*0.01)]
    return round(cr(t,mala),2), round(cr(t,L[len(L)//2]),2)

def vista_encabezado(im,ancho=393,alto=133,pos=0.85):
    """simula background-size: auto 140%; position: pos 0 (como en temas.css) con el degradado oscuro"""
    k=alto*1.4/im.height; s=im.resize((round(im.width*k),round(im.height*k)),Image.LANCZOS)
    x=round((s.width-ancho)*pos); v=s.crop((x,0,x+ancho,alto))
    def alfa(p):
        for (a,va),(b,vb) in zip(VELO_ENCABEZADO,VELO_ENCABEZADO[1:]):
            if p<=b: return va+(vb-va)*(p-a)/(b-a)
        return 0
    m=Image.new('L',(ancho,1)); m.putdata([round(255*alfa(i/(ancho-1))) for i in range(ancho)])
    return Image.composite(Image.new('RGB',v.size,PROFUNDO),v,m.resize(v.size))

if __name__=='__main__':
    base=sys.argv[1]; fin={}
    for f,salida,q in TRABAJOS:
        f(base).save(salida,'WEBP',quality=q,method=6)
        im=Image.open(salida).convert('RGB'); st=ImageStat.Stat(im); fin[f.__name__]=im
        print(salida,im.size,os.path.getsize(salida),'bytes, media','#%02X%02X%02X'%tuple(round(x) for x in st.mean),'desv. tipica',[round(x,1) for x in st.stddev])
    v=vista_encabezado(fin['encabezado'])
    filas=[('titulo (blanco) sobre encabezado, zona del texto','#FFFFFF',v.crop((58,50,170,75)),4.5),
           ('subtitulo (dorado) sobre encabezado, zona del texto',ORO_TEXTO,v.crop((58,75,180,96)),4.5),
           ('subtitulo largo (dorado) hasta el 70 % del ancho',ORO_TEXTO,v.crop((20,75,275,96)),4.5),
           ('texto (tinta) sobre papel',TINTA,fin['papel'],4.5),
           ('etiqueta (blanco) sobre barra','#FFFFFF',fin['barra'],4.5),
           ('etiqueta activa (dorado) sobre barra',ORO_TEXTO,fin['barra'],4.5),
           ('icono (dorado) sobre barra',ORO_ICONO,fin['barra'],3.0),
           ('icono (dorado) sobre boton redondo',ORO_TEXTO,fin['boton'].crop((64,64,128,128)),3.0),
           ('botones de Android (blanco) sobre piedra','#FFFFFF',fin['android'],3.0)]
    print('\n| elemento sobre textura | peor 1 % | mediana | minimo | ok |\n|---|---|---|---|---|')
    for n,c,im,m in filas:
        p,med=peor(c,im); print('|',n,'|',p,'|',med,'|',m,'|','si' if p>=m else 'NO','|')
