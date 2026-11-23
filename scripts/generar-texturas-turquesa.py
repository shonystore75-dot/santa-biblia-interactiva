# Prepara las texturas reales de Turquesa renovacion (mismo metodo aditivo que generar-cuero-realista.py de Azul clasico).
# Entrada: carpeta Santa_Biblia_2026_Turquesa_Renovacion (zip extraido FUERA del repo). Ninguna textura es un mosaico perfecto: no se repiten
#   (cuero y papel del fondo: una sola imagen; tarjetas y botones: una sola imagen mas grande que el elemento).
# Salida: texturas/cuero_turquesa_realista.webp, papel_marfil_verdoso.webp, cuero_turquesa_oscuro.webp
# Uso: python scripts/generar-texturas-turquesa.py <carpeta extraida>
import sys, os
from PIL import Image, ImageStat
base=sys.argv[1]
# (archivo origen, salida, color medio objetivo, lado, calidad)
TRABAJOS=[('01_Cuero_Turquesa/cuero_turquesa_fino.png','texturas/cuero_turquesa_realista.webp',(0x12,0x61,0x6A),1000,55),
          ('02_Papel_Marfil_Verdoso/papel_marfil_verdoso.png','texturas/papel_marfil_verdoso.webp',(0xEF,0xF7,0xF5),1000,70),
          ('04_Cuero_Turquesa_Oscuro/cuero_turquesa_oscuro.png','texturas/cuero_turquesa_oscuro.webp',(0x18,0x4A,0x51),512,72)]
for rel,salida,obj,lado,q in TRABAJOS:
    im=Image.open(os.path.join(base,rel)).convert('RGB')
    media=ImageStat.Stat(im).mean
    d=[round(obj[c]-media[c]) for c in range(3)]
    print(rel,im.size,'media','#%02X%02X%02X'%tuple(round(x) for x in media),'desplazamiento',d)
    im=im.point(sum([[max(0,min(255,v+d[c])) for v in range(256)] for c in range(3)],[]))
    if im.width!=lado: im=im.resize((lado,lado),Image.LANCZOS)
    im.save(salida,'WEBP',quality=q,method=6)
    fin=Image.open(salida).convert('RGB'); st=ImageStat.Stat(fin)
    print('  ->',salida,fin.size,os.path.getsize(salida),'bytes, media','#%02X%02X%02X'%tuple(round(x) for x in st.mean),'desv. tipica',[round(x,1) for x in st.stddev])
