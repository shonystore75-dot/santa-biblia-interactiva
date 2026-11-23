# Prepara el cuero fotografico del encabezado y la barra inferior de Azul clasico.
# Entrada: cuero_azul_marino_realista.png (1254x1254, no repite bien en mosaico; NO se repite en la app).
# Salida: texturas/cuero_azul_realista.webp, con el color medio desplazado (suma por canal) hasta #102F50 y el contraste del grano intacto.
# Uso: python scripts/generar-cuero-realista.py <ruta al png original>
import sys
from PIL import Image, ImageStat
OBJETIVO=(0x10,0x2F,0x50); LADO=1000; CALIDAD=78
src=sys.argv[1]
im=Image.open(src).convert('RGB')
media=ImageStat.Stat(im).mean
d=[round(OBJETIVO[c]-media[c]) for c in range(3)]
print('original',im.size,'media',[round(x,1) for x in media],'desplazamiento',d)
im=im.point([max(0,min(255,v+d[0])) for v in range(256)]+[max(0,min(255,v+d[1])) for v in range(256)]+[max(0,min(255,v+d[2])) for v in range(256)])
if im.width!=LADO: im=im.resize((LADO,LADO),Image.LANCZOS)
im.save('texturas/cuero_azul_realista.webp','WEBP',quality=CALIDAD)
fin=Image.open('texturas/cuero_azul_realista.webp').convert('RGB'); st=ImageStat.Stat(fin)
print('final',fin.size,'media','#%02X%02X%02X'%tuple(round(x) for x in st.mean),'desv. tipica',[round(x,1) for x in st.stddev])
