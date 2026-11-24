# Genera las texturas de Borgona real (piedra noble con vetas) con PIL, sin depender del zip: las del zip eran un recorte
# repetido en espejo (rombos simetricos muy visibles). Aqui cada textura es UNA imagen irregular, sin simetria ni mosaico,
# que imita la piedra de la referencia: base #641D2B, nubes oscuras y claras, grano fino y vetas finas de rojo mas claro.
# Salida: texturas/piedra_borgona.webp, papel_borgona.webp, piedra_borgona_oscura.webp
# Uso: python scripts/generar-texturas-borgona.py        (determinista: semillas fijas)
import random, math, os
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageStat

def nubes(lado, escalas, pesos, semilla):
    """Ruido de varias octavas, normalizado a media 128."""
    rnd=random.Random(semilla); acc=None
    for esc,peso in zip(escalas,pesos):
        n=max(2,lado//esc)
        im=Image.new('L',(n,n)); im.putdata([rnd.randint(0,255) for _ in range(n*n)])
        im=im.resize((lado,lado),Image.BICUBIC)
        im=im.point([int(128+(v-128)*peso) for v in range(256)])
        acc=im if acc is None else ImageChops.add(acc,im,scale=1.0,offset=-128)
    return acc

def grano(lado, sigma, semilla):
    rnd=random.Random(semilla)
    im=Image.new('L',(lado,lado)); im.putdata([max(0,min(255,int(rnd.gauss(128,sigma)))) for _ in range(lado*lado)])
    return im

def vetas(lado, n, semilla, ancho=1.4):
    """Mascara de vetas: caminatas aleatorias con ramas, trazadas al doble de tamano y suavizadas."""
    rnd=random.Random(semilla); S=2; L=lado*S
    m=Image.new('L',(L,L),0); d=ImageDraw.Draw(m)
    def camina(x,y,ang,pasos,grosor,prof):
        pts=[(x,y)]
        for i in range(pasos):
            ang+=rnd.gauss(0,0.12)
            x+=math.cos(ang)*7*S; y+=math.sin(ang)*7*S
            pts.append((x,y))
            if prof<2 and rnd.random()<0.02:
                camina(x,y,ang+rnd.choice((-1,1))*rnd.uniform(0.5,1.1),rnd.randint(15,60),max(1,grosor-1),prof+1)
        d.line(pts,fill=255 if prof==0 else 190,width=max(1,int(grosor*S*ancho/1.4)))
    for _ in range(n):
        lado_ini=rnd.choice('tblr')
        if lado_ini=='t': x,y,a=rnd.uniform(0,L),0,rnd.uniform(0.3,2.8)
        elif lado_ini=='b': x,y,a=rnd.uniform(0,L),L,rnd.uniform(-2.8,-0.3)
        elif lado_ini=='l': x,y,a=0,rnd.uniform(0,L),rnd.uniform(-1.1,1.1)
        else: x,y,a=L,rnd.uniform(0,L),rnd.uniform(2.0,4.2)
        camina(x,y,a,rnd.randint(80,200),2,0)
    m=m.filter(ImageFilter.GaussianBlur(1.0*S)).resize((lado,lado),Image.LANCZOS)
    return m

def tono(base,sombra,extra=None):
    """Multiplica el color base por el mapa de sombras (128 = sin cambio) canal a canal."""
    canales=[sombra.point([max(0,min(255,round(base[c]*v/128))) for v in range(256)]) for c in range(3)]
    return Image.merge('RGB',canales)

def a_media(im,obj):
    """Desplazamiento aditivo por canal hasta la media objetivo (metodo de Azul clasico y Turquesa)."""
    media=ImageStat.Stat(im).mean; d=[round(obj[c]-media[c]) for c in range(3)]
    return im.point(sum([[max(0,min(255,v+d[c])) for v in range(256)] for c in range(3)],[])),d

def piedra(lado,obj,semilla,vena,intensidad_vena,amp):
    sombra=nubes(lado,[330,150,70,34],[amp*1.0,amp*0.8,amp*0.5,amp*0.3],semilla)
    g=grano(lado,16,semilla+1).filter(ImageFilter.GaussianBlur(0.6))
    sombra=ImageChops.add(sombra,g,scale=1.0,offset=-128)
    im=tono(obj,sombra)
    mask=vetas(lado,6,semilla+2).point([int(v*intensidad_vena) for v in range(256)])
    im=Image.composite(Image.new('RGB',(lado,lado),vena),im,mask)
    return a_media(im,obj)

def papel(lado,obj,semilla):
    sombra=nubes(lado,[300,140,60,28],[0.035,0.03,0.022,0.014],semilla)
    sombra=ImageChops.add(sombra,grano(lado,2.2,semilla+1).filter(ImageFilter.GaussianBlur(0.5)),scale=1.0,offset=-128)
    # manchas calidas: los canales verde y azul varian algo mas que el rojo (tono durazno suave como en la referencia)
    r=sombra.point([max(0,min(255,round(obj[0]*(1+(v-128)/128*0.6)))) for v in range(256)])
    g=sombra.point([max(0,min(255,round(obj[1]*(1+(v-128)/128*1.0)))) for v in range(256)])
    b=sombra.point([max(0,min(255,round(obj[2]*(1+(v-128)/128*1.1)))) for v in range(256)])
    return a_media(Image.merge('RGB',[r,g,b]),obj)

JOBS=[('piedra',   'texturas/piedra_borgona.webp',        1000,(0x64,0x1D,0x2B),dict(semilla=11,vena=(0xC4,0x3A,0x52),intensidad_vena=0.9,amp=0.11),90),
      ('papel',    'texturas/papel_borgona.webp',         1000,(0xFA,0xF3,0xEB),dict(semilla=23),78),
      ('oscura',   'texturas/piedra_borgona_oscura.webp',  512,(0x56,0x15,0x22),dict(semilla=37,vena=(0xA8,0x30,0x48),intensidad_vena=0.7,amp=0.11),90)]
if __name__=='__main__':
    for tipo,salida,lado,obj,kw,q in JOBS:
        im,d=(papel(lado,obj,**kw) if tipo=='papel' else piedra(lado,obj,**kw))
        im.save(salida,'WEBP',quality=q,method=6)
        fin=Image.open(salida).convert('RGB'); st=ImageStat.Stat(fin)
        print(salida,fin.size,os.path.getsize(salida),'bytes, media','#%02X%02X%02X'%tuple(round(x) for x in st.mean),'desv. tipica',[round(x,1) for x in st.stddev])
