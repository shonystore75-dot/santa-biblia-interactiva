# Prepara las texturas de Verde olivo a partir del zip Texturas_Verde_Olivo_Santa_Biblia_2026 (mismo metodo aditivo que Turquesa).
# Los mosaicos del zip son REFLEJADOS: para la barra y los botones se usa UN SOLO cuadrante (sin espejo ni mosaico);
# la barra y la piedra de la zona Android se arman con parches al azar de un cuadrante (semilla fija).
# Al encabezado se le dibuja una pradera iluminada en la parte baja (el fondo reconstruido del zip es casi negro ahi).
# Entrada: carpeta Verde_Olivo_Santa_Biblia_2026 (zip extraido FUERA del repo)
# Salida: texturas/encabezado_olivo.webp, barra_olivo.webp, papel_olivo.webp, piedra_olivo_oscura.webp, piedra_olivo_android.webp
# Uso: python scripts/generar-texturas-olivo.py <carpeta extraida>     (imprime tamanos, colores y contraste sobre cada textura)
import sys, os, random, math
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageStat

PRINCIPAL=(0x35,0x46,0x09); PROFUNDO=(0x18,0x26,0x05)
MARFIL=(0xFE,0xF1,0xD6)          # un poco menos amarillo que paleta.json (#FFF0C9), igual al centro de lectura de la referencia
BOTON=(0x21,0x30,0x04)           # como los botones de la referencia
ANDROID=(0x36,0x45,0x04)         # piedra verde detras de los botones de Android
TINTA='#202815'; ORO_TEXTO='#F0D27A'; ORO_ICONO='#F0CF72'
# el titulo y el subtitulo llevan su propio oscurecimiento en CSS (generar-temas.py); su contraste se mide sobre capturas del telefono

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

def rampa(x,a,b):
    t=max(0.0,min(1.0,(x-a)/(b-a))); return t*t*(3-2*t)

def mascara(tam,f):
    m=Image.new('L',tam); w,h=tam; m.putdata([round(255*max(0,min(1,f(x,y)))) for y in range(h) for x in range(w)]); return m

def pradera(im,base):
    """Aclara la franja baja: pradera con tres lomas de cresta iluminada y grano de hierba. La luz se concentra bajo el sol y el olivo."""
    w,h=im.size
    lado=lambda x: 0.35+0.65*rampa(x,260,620)                      # mas suave detras del texto
    sol=lambda x: math.exp(-((x-850)/330.0)**2)
    # color de la pradera: mas calido cerca del horizonte y bajo el sol
    col=Image.new('RGB',im.size)
    col.putdata([(round(66+34*sol(x)-18*rampa(y,170,300)), round(84+30*sol(x)-18*rampa(y,170,300)), 6) for y in range(h) for x in range(w)])
    alfa=mascara(im.size,lambda x,y: 0.92*rampa(y,142,192)*lado(x))
    im=Image.composite(col,im,alfa)
    # lomas: sombra bajo cada cresta y filo de luz sobre ella
    for y0,amp,fase,luz in ((174,7,0.6,0.24),(202,11,2.4,0.22),(236,12,4.1,0.17)):
        cresta=[y0+amp*math.sin(x/97.0+fase)+0.45*amp*math.sin(x/41.0+2*fase) for x in range(w)]
        sombra=mascara(im.size,lambda x,y: 0.40*rampa(y-cresta[x],-2,9)*(1-rampa(y-cresta[x],12,40))*lado(x))
        im=Image.composite(Image.new('RGB',im.size,(30,42,3)),im,sombra)
        filo=mascara(im.size,lambda x,y: luz*math.exp(-((y-cresta[x]+5)/(7.0 if y<cresta[x]-5 else 4.5))**2)*(0.35+0.65*sol(x))*lado(x))
        im=Image.composite(Image.new('RGB',im.size,(176,170,40)),im,filo)
    # grano de hierba (luminancia del recurso 03), solo en la pradera
    g=Image.open(os.path.join(base,'03_piedra_olivo_android/recurso.png')).convert('L').crop((24,24,232,150))
    g=parches(g.convert('RGB'),(w,h),96,11).convert('L'); media=ImageStat.Stat(g).mean[0]
    delta=g.point([max(0,min(255,round(128+(v-media)*0.75))) for v in range(256)])
    con=ImageChops.add(im,Image.merge('RGB',[delta,delta,delta.point([128+(v-128)//4 for v in range(256)])]),1.0,-128)
    return Image.composite(con,im,mascara(im.size,lambda x,y: rampa(y,160,200)))

def parches(im,tam,P,semilla):
    """Arma una textura de tamano 'tam' con parches al azar (bordes difuminados, volteados): sin mosaico ni espejo."""
    rnd=random.Random(semilla); lienzo=im.resize(tam,Image.BICUBIC); paso=P*35//96
    m=Image.new('L',(P,P),0); ImageDraw.Draw(m).ellipse((P*14//96,P*14//96,P-P*14//96,P-P*14//96),fill=255); m=m.filter(ImageFilter.GaussianBlur(P/12))
    for y in range(-P//2,tam[1],paso):
        for x in range(-P//2,tam[0],paso):
            sx=rnd.randint(0,im.width-P); sy=rnd.randint(0,im.height-P); parche=im.crop((sx,sy,sx+P,sy+P))
            if rnd.random()<0.5: parche=parche.transpose(Image.FLIP_LEFT_RIGHT)
            if rnd.random()<0.5: parche=parche.transpose(Image.FLIP_TOP_BOTTOM)
            lienzo.paste(parche,(x+rnd.randint(-P//8,P//8),y+rnd.randint(-P//8,P//8)),m)
    return lienzo

def encabezado(base):
    return pradera(Image.open(os.path.join(base,'01_encabezado/fondo_reconstruido/recurso.png')).convert('RGB'),base)

def barra(base):
    L=(1000,280)
    piedra=Image.open(os.path.join(base,'03_piedra_olivo_android/recurso.png')).convert('RGB').crop((24,24,232,232))
    piedra=piedra.resize((312,312),Image.LANCZOS)                       # relieve algo mas grande que en la zona Android
    im=parches(piedra,L,128,23)
    # variacion amplia y calida del recurso 04 (medio ancho: sin espejo)
    luz=Image.open(os.path.join(base,'04_verde_barra/recurso.png')).convert('RGB').crop((0,96,256,416)).resize(L,Image.BICUBIC)
    im=Image.blend(im,luz,0.18).filter(ImageFilter.UnsharpMask(radius=2,percent=70,threshold=0))
    im=contraste_de_media(im,0.82)
    # degradado leve hacia olivo profundo (nada arriba, 25 % abajo)
    r=Image.new('L',(1,L[1])); r.putdata([round(255*0.25*(y/(L[1]-1))**1.3) for y in range(L[1])])
    im=Image.composite(Image.new('RGB',L,PROFUNDO),im,r.resize(L))
    # recorta los brillos (70 % por encima de la media) para que el dorado de la etiqueta activa pase 4,5:1; las sombras se conservan
    m=ImageStat.Stat(im).mean
    im=Image.merge('RGB',[x.point([v if v<=m[i] else round(m[i]+(v-m[i])*0.7) for v in range(256)]) for i,x in enumerate(im.split())])
    return a_media(im,PRINCIPAL)

def papel(base):
    im=Image.open(os.path.join(base,'02_papel_marfil/recurso.png')).convert('RGB')     # 512, tamano nativo
    return a_media(im,MARFIL)

def boton(base):
    im=Image.open(os.path.join(base,'03_piedra_olivo_android/recurso.png')).convert('RGB')
    im=im.crop((30,30,222,222))                                        # un cuadrante, sin el rombo central ni el borde oscuro
    return a_media(contraste_de_media(im,0.65),BOTON)

def android(base):
    im=Image.open(os.path.join(base,'03_piedra_olivo_android/recurso.png')).convert('RGB').crop((24,24,232,150))   # parte pareja de un cuadrante
    return a_media(contraste_de_media(parches(im,(1000,160),96,5),0.8),ANDROID)

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

if __name__=='__main__':
    base=sys.argv[1]; fin={}
    for f,salida,q in TRABAJOS:
        f(base).save(salida,'WEBP',quality=q,method=6)
        im=Image.open(salida).convert('RGB'); st=ImageStat.Stat(im); fin[f.__name__]=im
        print(salida,im.size,os.path.getsize(salida),'bytes, media','#%02X%02X%02X'%tuple(round(x) for x in st.mean),'desv. tipica',[round(x,1) for x in st.stddev])
    filas=[('texto (tinta) sobre papel',TINTA,fin['papel'],4.5),
           ('etiqueta (blanco) sobre barra','#FFFFFF',fin['barra'],4.5),
           ('etiqueta activa (dorado) sobre barra',ORO_TEXTO,fin['barra'],4.5),
           ('icono (dorado) sobre barra',ORO_ICONO,fin['barra'],3.0),
           ('icono (dorado) sobre boton redondo',ORO_TEXTO,fin['boton'].crop((64,64,128,128)),3.0),
           ('botones de Android (blanco) sobre piedra','#FFFFFF',fin['android'],3.0)]
    print('\n| elemento sobre textura | peor 1 % | mediana | minimo | ok |\n|---|---|---|---|---|')
    for n,c,im,m in filas:
        p,med=peor(c,im); print('|',n,'|',p,'|',med,'|',m,'|','si' if p>=m else 'NO','|')
