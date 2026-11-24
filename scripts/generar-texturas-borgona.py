# Prepara las texturas de Borgona real (piedra noble), mismo metodo aditivo que Azul clasico y Turquesa.
# Entrada: carpeta Santa_Biblia_2026_Borgona_Real (zip extraido FUERA del repo). Las texturas se recortaron de la referencia y se
#   repitieron con efecto espejo: pueden mostrar patrones de repeticion; por eso la piedra va como UNA sola imagen (sin mosaico).
# Salida: texturas/piedra_borgona.webp, papel_borgona.webp, piedra_borgona_oscura.webp
# Uso: python scripts/generar-texturas-borgona.py <carpeta extraida>
import sys, os
from PIL import Image, ImageStat
base=sys.argv[1]
# (origen, salida, color medio objetivo, lado, calidad, ganancia de contraste alrededor de la media)
TRABAJOS=[('01_piedra_borgona/textura.png','texturas/piedra_borgona.webp',(0x64,0x1D,0x2B),1024,92,1.0),
          ('02_papel_marfil/textura.png','texturas/papel_borgona.webp',(0xFA,0xF3,0xEB),1024,92,3.0),   # el papel original es casi liso (desv. ~1): ganancia x3 para que se aprecie el grano
          ('03_piedra_borgona_oscura/textura.png','texturas/piedra_borgona_oscura.webp',(0x42,0x0E,0x20),512,92,1.0)]
for rel,salida,obj,lado,q,g in TRABAJOS:
    im=Image.open(os.path.join(base,rel)).convert('RGB')
    media=ImageStat.Stat(im).mean
    d=[round(obj[c]-media[c]) for c in range(3)]
    print(rel,im.size,'media','#%02X%02X%02X'%tuple(round(x) for x in media),'desplazamiento',d,'ganancia',g)
    lut=sum([[max(0,min(255,round(v+d[c]+(v-media[c])*(g-1)))) for v in range(256)] for c in range(3)],[])
    im=im.point(lut)
    if im.width!=lado: im=im.resize((lado,lado),Image.LANCZOS)
    im.save(salida,'WEBP',quality=q,method=6)
    fin=Image.open(salida).convert('RGB'); st=ImageStat.Stat(fin)
    print('  ->',salida,fin.size,os.path.getsize(salida),'bytes, media','#%02X%02X%02X'%tuple(round(x) for x in st.mean),'desv. tipica',[round(x,1) for x in st.stddev])
