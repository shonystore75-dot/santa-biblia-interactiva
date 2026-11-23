# Genera versiones con mas contraste de la textura de cuero (01) para el encabezado y la barra de Azul clasico.
# Estira cada canal alrededor de su media (x2, x3...), sin tocar el original. Uso: python scripts/generar-cuero.py
from PIL import Image, ImageStat
ORIG='texturas/01_cuero_azul_marino.webp'
im=Image.open(ORIG).convert('RGB')
media=ImageStat.Stat(im).mean
for k in (2,3):
    lut=[]
    for c in range(3):
        lut+= [max(0,min(255,round(media[c]+(v-media[c])*k))) for v in range(256)]
    out=im.point(lut)
    out.save('texturas/01_cuero_azul_marino_x%d.webp'%k,'WEBP',quality=88)
    print(k,[round(x,1) for x in ImageStat.Stat(out).mean],ImageStat.Stat(out).extrema)
