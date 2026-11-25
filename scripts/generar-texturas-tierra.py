# Prepara las texturas de Tierra biblica a partir del zip Texturas_Tierra_Santa_Biblia_2026 (mismo metodo que Verde olivo).
# Los mosaicos del zip son REFLEJADOS y traen manchas (puntos blancos en la madera, manchas negras en el papel): se arman
# texturas nuevas con parches al azar de zonas limpias (semillas fijas), sin espejo; el papel ademas cierra sin costura.
# La barra y la zona de los botones de Android son un empedrado de arenisca dibujado por el script, a juego con el sendero del encabezado.
# Encabezado: 'fondo_reconstruido' trae bloques emborronados donde estaban el titulo y los botones, y la curva dorada abajo.
# Se arma uno nuevo: arbol (izquierda) + valle, sol y casa (derecha) para que ambos quepan en el encabezado del telefono,
# se corta la curva dorada y se repinta la parte baja: matorrales a la izquierda (parches de la misma imagen) y empedrado dibujado a la derecha.
# 'recorte_referencia' NO se usa.
# Entrada: carpeta Tierra_Santa_Biblia_2026 (zip extraido FUERA del repo)
# Salida: texturas/encabezado_tierra.webp, barra_tierra.webp, papel_tierra.webp, piedra_tierra_oscura.webp, piedra_tierra_android.webp
# Uso: python scripts/generar-texturas-tierra.py <carpeta extraida>     (imprime tamanos, colores y contraste sobre cada textura)
import sys, os, random, math
from PIL import Image, ImageDraw, ImageFilter, ImageStat

PRINCIPAL=(0x48,0x2B,0x1D); PROFUNDO=(0x24,0x12,0x08)
MARFIL=(0xFA,0xF1,0xE3)          # marfil de paleta.json (menos calido que el papel del zip, #FEEFD9)
BOTON=(0x45,0x21,0x0F)           # marron rojizo oscuro de los botones de la referencia
BARRA=(0x60,0x3C,0x26)           # piedra de la barra: marron de la paleta (#482B1D) aclarado
ANDROID=(0x8A,0x5C,0x38)         # piedra detras de los botones de Android (arenisca, mas clara que la barra)
TINTA='#392419'; ORO_TEXTO='#F0D27A'; ORO_ICONO='#F0CF72'
# el titulo y el subtitulo llevan su propio oscurecimiento en CSS (generar-temas.py); su contraste se mide sobre capturas del telefono

def rampa(x,a,b):
    t=max(0.0,min(1.0,(x-a)/(b-a))); return t*t*(3-2*t)

def contraste_de_media(im,k):
    """k<1 suaviza el grano alrededor de la media; k>1 lo realza."""
    m=ImageStat.Stat(im).mean
    return Image.merge('RGB',[c.point([max(0,min(255,round(m[i]+(v-m[i])*k))) for v in range(256)]) for i,c in enumerate(im.split())])

def a_media(im,obj):
    """Desplazamiento aditivo por canal hasta la media objetivo (varias pasadas para compensar el recorte en 0 y 255)."""
    for _ in range(3):
        media=ImageStat.Stat(im).mean; d=[round(obj[c]-media[c]) for c in range(3)]
        im=im.point(sum([[max(0,min(255,v+d[c])) for v in range(256)] for c in range(3)],[]))
    return im

def parches(donantes,tam,P,semilla,cierra=False):
    """Textura de tamano 'tam' con parches (ancho,alto)=P al azar de los 'donantes', bordes difuminados y volteo horizontal.
    cierra=True: los parches que salen por un borde entran por el opuesto (mosaico sin costura)."""
    rnd=random.Random(semilla); pw,ph=P; W,H=tam
    lienzo=donantes[0].resize(tam,Image.BICUBIC)
    m=Image.new('L',P,0); ImageDraw.Draw(m).ellipse((pw//7,ph//7,pw-pw//7,ph-ph//7),fill=255); m=m.filter(ImageFilter.GaussianBlur(min(P)/12))
    px,py=max(1,pw*35//96),max(1,ph*35//96)
    for y in range(0 if cierra else -ph//2,H,py):
        for x in range(0 if cierra else -pw//2,W,px):
            d=rnd.choice(donantes)
            if d.width<pw or d.height<ph:
                k=max(pw/d.width,ph/d.height); d=d.resize((round(d.width*k)+1,round(d.height*k)+1),Image.BICUBIC)
            sx=rnd.randint(0,d.width-pw); sy=rnd.randint(0,d.height-ph); p=d.crop((sx,sy,sx+pw,sy+ph))
            if rnd.random()<0.5: p=p.transpose(Image.FLIP_LEFT_RIGHT)
            X=x+rnd.randint(-pw//8,pw//8); Y=y+rnd.randint(-ph//8,ph//8)
            for dx in ((-W,0,W) if cierra else (0,)):
                for dy in ((-H,0,H) if cierra else (0,)):
                    lienzo.paste(p,(X+dx,Y+dy),m)
    return lienzo

def zona(tam,poligono,difuso):
    m=Image.new('L',tam,0); ImageDraw.Draw(m).polygon(poligono,fill=255); return m.filter(ImageFilter.GaussianBlur(difuso))

def abrir(base,rel): return Image.open(os.path.join(base,rel,'recurso.png')).convert('RGB')

def encabezado(base):
    f=abrir(base,'01_encabezado/fondo_reconstruido')                  # 832x235
    H=192; CORTE=320; SOLAPE=70; IZQ=150                              # alto sin la curva dorada; arbol [0,150) + resto desde x=320
    W=IZQ+(f.width-CORTE)-SOLAPE; dx=IZQ-SOLAPE-CORTE                 # x en la composicion = x original + dx
    im=Image.new('RGB',(W,H)); im.paste(f.crop((CORTE,0,f.width,H)),(CORTE+dx,0))
    mezcla=Image.new('L',(IZQ,H),255); d=ImageDraw.Draw(mezcla)
    for x in range(SOLAPE):
        t=x/(SOLAPE-1); d.line([(IZQ-SOLAPE+x,0),(IZQ-SOLAPE+x,H)],fill=round(255*(1-t*t*(3-2*t))))
    im.paste(f.crop((0,0,IZQ,H)),(0,0),mezcla)
    c=lambda *b: f.crop(b)
    # 1) bruma del valle donde quedaba el borde del bloque del titulo, entre el arbol y el valle
    bruma=parches([c(396,72,470,128)],(W,H),(44,30),3)
    im=Image.composite(bruma,im,zona((W,H),[(104,68),(150,66),(152,134),(108,132)],7))
    # 2) abajo a la izquierda: matorrales y olivos
    veg=parches([c(392,150,446,190),c(446,110,500,150),c(0,66,34,128)],(W,H),(36,28),7)
    veg=Image.blend(veg,Image.new('RGB',(W,H),(60,36,10)),0.18)
    im=Image.composite(veg,im,zona((W,H),[(0,136),(40,126),(100,122),(168,128),(176,150),(168,192),(0,192)],6))
    # 3) se amplia al doble y abajo a la derecha se dibuja el empedrado en perspectiva (losas mas grandes hacia delante)
    im=im.resize((W*2,H*2),Image.LANCZOS)
    grano=parches([c(452,198,540,224),c(404,196,470,218)],(W*2,H*2),(60,24),19)
    piso=empedrado((W*2,H*2),grano,57)
    r=lambda x,y: (2*(x+dx),2*y)
    forma=[r(468,152),r(500,138),r(545,132),r(600,130),r(660,128),r(722,129),r(792,134),r(808,148),r(808,192),r(448,192),r(447,174)]
    im=Image.composite(piso,im,zona(im.size,forma,7))
    return im.filter(ImageFilter.UnsharpMask(radius=1.4,percent=55,threshold=2))

def empedrado(tam,grano,semilla):
    """Losas tipo Voronoi en perspectiva: junta oscura, canto superior iluminado, color propio por piedra y grano de la imagen original."""
    W,H=tam; rnd=random.Random(semilla); semillas={}
    def punto(i,j):
        if (i,j) not in semillas:
            semillas[(i,j)]=(i+0.5*(j%2)+rnd.uniform(-0.32,0.32), j+rnd.uniform(-0.30,0.30), rnd.uniform(0.84,1.14), rnd.uniform(-8,8))
        return semillas[(i,j)]
    g=grano.load(); gb=grano.filter(ImageFilter.GaussianBlur(5)).load(); out=Image.new('RGB',tam,(150,100,52)); o=out.load()
    for y in range(236,H):
        v=y-196; esc=v/120.0                       # tamano aparente de las losas segun la distancia
        for x in range(W):
            X=(x-760)/(66*esc)+0.18*math.sin(y/23.0+x/61.0); Y=math.log(v/40.0)*5.2+0.15*math.sin(x/37.0)
            a=b=(9e9,None)
            for j in range(int(math.floor(Y))-1,int(math.floor(Y))+3):
                for i in range(int(math.floor(X))-2,int(math.floor(X))+3):
                    q=punto(i,j); d=(X-q[0])**2+((Y-q[1])*1.15)**2
                    if d<a[0]: a,b=(d,q),a
                    elif d<b[0]: b=(d,q)
            borde=math.sqrt(b[0])-math.sqrt(a[0]); q=a[1]
            piedra=rampa(borde,0.03,0.20)                                  # 0 en la junta, 1 dentro de la losa
            canto=(q[1]-Y)*math.exp(-((borde-0.22)/0.14)**2)               # luz arriba, sombra abajo
            t=max(0.0,min(1.0,(x-620)/520.0))                              # dorado junto al sendero, tostado hacia la esquina
            base=(214-58*t,162-52*t,98-38*t)
            sombra=1.0-0.16*rampa(y,320,H)
            col=[]
            for k in range(3):
                piel=base[k]*q[2]+(q[3] if k==0 else 0)+38*canto*(1,0.9,0.7)[k]+0.6*(g[x,y][k]-gb[x,y][k])
                junta=(92,58,30)[k]
                col.append(max(0,min(255,round((junta+(piel-junta)*piedra)*sombra))))
            o[x,y]=tuple(col)
    return out.filter(ImageFilter.GaussianBlur(0.6))

def ruido(tam,celda,rnd):
    """Ruido suave en 0..1 (rejilla al azar ampliada)."""
    w,h=tam; g=Image.new('L',(w//celda+4,h//celda+4)); g.putdata([rnd.randint(0,255) for _ in range(g.width*g.height)])
    g=g.resize((g.width*celda,g.height*celda),Image.BICUBIC).crop((celda,celda,celda+w,celda+h))
    return [v/255 for v in g.tobytes()]

def losas(L,semilla,celda,objetivo,corte=8,brillo=0.5):
    """Empedrado de arenisca como el sendero del encabezado: losas irregulares (Voronoi) con junta hundida, canto superior
    iluminado, color propio por piedra (marron, terracota, cobre), picado y grano. Sin mosaico: una sola imagen."""
    W,H=L; cw,ch=celda; rnd=random.Random(semilla); sem={}
    TONOS=[(108,72,46),(116,74,46),(114,80,50),(100,68,44),(124,86,54),(106,68,42)]
    def piedra_de(i,j):
        if (i,j) not in sem:
            sem[(i,j)]=(i+0.5*(j%2)+rnd.uniform(-0.30,0.30), j+rnd.uniform(-0.28,0.28), rnd.choice(TONOS), rnd.uniform(0.90,1.10), rnd.uniform(-0.5,0.5), rnd.uniform(-0.5,0.5))
        return sem[(i,j)]
    torcido=ruido(L,34,rnd); torcido2=ruido(L,34,rnd); quiebre=ruido(L,11,rnd); nube=ruido(L,46,rnd); medio=ruido(L,9,rnd); fino=ruido(L,3,rnd); polvo=ruido(L,1,rnd)
    im=Image.new('RGB',L); o=im.load()
    for y in range(H):
        for x in range(W):
            k=y*W+x
            X=x/cw+(torcido[k]-0.5)*0.12+(quiebre[k]-0.5)*0.035
            Y=y/ch+(torcido2[k]-0.5)*0.12+(quiebre[(k+977)%(W*H)]-0.5)*0.045
            a=b=(9e9,None)
            for j in range(int(Y)-1,int(Y)+3):
                for i in range(int(X)-2,int(X)+3):
                    q=piedra_de(i,j); d=((X-q[0])*cw/ch)**2+(Y-q[1])**2
                    if d<a[0]: a,b=(d,q),a
                    elif d<b[0]: b=(d,q)
            q=a[1]; r=b[1]
            ex=(r[0]-q[0])*cw/ch; ey=r[1]-q[1]; sep=math.hypot(ex,ey) or 1
            borde=(b[0]-a[0])/(2*sep)*ch                                   # distancia en pixeles a la junta
            dentro=rampa(borde,1.6,5.0)                                    # 0 en la junta, 1 en la losa
            hacia_arriba=-ey/sep                                           # 1 si la junta mas cercana queda arriba
            bisel=math.exp(-((borde-7.0)/5.0)**2)*hacia_arriba
            lomo=0.80+0.20*rampa(borde,3.0,17.0)                          # la losa se redondea: mas oscura junto al canto
            inclina=q[4]*(X-q[0])*0.16+q[5]*(Y-q[1])*0.16                  # cada losa algo inclinada respecto a la luz
            v=q[3]*lomo*(1.04+inclina+0.26*(nube[k]-0.5)+0.16*(medio[k]-0.5)+0.14*(fino[k]-0.5)+0.12*(polvo[k]-0.5))
            if medio[k]<0.24 and fino[k]<0.34: v*=0.90                     # picaduras
            col=[q[2][c]*v+(64,48,30)[c]*bisel*(1.0 if bisel>0 else 0.6) for c in range(3)]
            junta=[(50,30,17)[c]*(0.8+0.5*fino[k]) for c in range(3)]
            o[x,y]=tuple(max(0,min(255,round(junta[c]+(col[c]-junta[c])*dentro))) for c in range(3))
    im=im.filter(ImageFilter.GaussianBlur(0.5)).filter(ImageFilter.UnsharpMask(radius=1.6,percent=60,threshold=1))
    # recorta los brillos para que el dorado de la etiqueta activa pase 4,5:1
    med=ImageStat.Stat(im).mean
    im=Image.merge('RGB',[c.point([v if v<=med[n]+corte else round(med[n]+corte+(v-med[n]-corte)*brillo) for v in range(256)]) for n,c in enumerate(im.split())])
    return a_media(im,objetivo)

def barra(base):
    return losas((1000,280),14,(132,84),BARRA,corte=4,brillo=0.22)

def papel(base):
    p=abrir(base,'02_papel_marfil')
    donantes=[p.crop((70,40,250,250)),p.crop((262,262,442,472))]        # sin las manchas negras de las esquinas
    return a_media(parches(donantes,(512,512),(128,128),31,cierra=True),MARFIL)

def piedra(base):   # parte interior de un cuadrante: sin el rombo ni los ejes del espejo
    return abrir(base,'03_piedra_arenisca_android').crop((138,150,252,252))

def boton(base):
    im=parches([piedra(base)],(192,192),(72,72),41)
    return a_media(contraste_de_media(im,0.7),BOTON)

def android(base):
    """Zona de los botones de Android: el mismo empedrado, losas algo menores y un tono arenisca mas claro."""
    return losas((1000,160),73,(104,62),ANDROID)

TRABAJOS=[(encabezado,'texturas/encabezado_tierra.webp',86),(barra,'texturas/barra_tierra.webp',86),
          (papel,'texturas/papel_tierra.webp',80),(boton,'texturas/piedra_tierra_oscura.webp',82),
          (android,'texturas/piedra_tierra_android.webp',84)]

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
