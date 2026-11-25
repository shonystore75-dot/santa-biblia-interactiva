"""Papel del fondo de Azul clasico: mismo grano que 02_papel_marfil_grisaceo.webp (con la intensidad x3 aprobada),
pero opaco y con el color medio exacto del fondo (#F7F5F0), para que la textura no lo vuelva gris."""
import os
from PIL import Image, ImageStat

RAIZ = os.path.join(os.path.dirname(__file__), '..', 'texturas')
FONDO = (0xF7, 0xF5, 0xF0)
INTENSIDAD = 3                                   # veces la opacidad del archivo original

origen = Image.open(os.path.join(RAIZ, '02_papel_marfil_grisaceo.webp')).convert('RGBA')
alfa = origen.getchannel('A').getextrema()[1] / 255
efectiva = 1 - (1 - alfa) ** INTENSIDAD          # la de apilar INTENSIDAD capas
rgb = origen.convert('RGB')
medias = ImageStat.Stat(rgb).mean
canales = [c.point([max(0, min(255, round(FONDO[i] + efectiva * (v - medias[i])))) for v in range(256)])
           for i, c in enumerate(rgb.split())]
salida = Image.merge('RGB', canales)
ruta = os.path.join(RAIZ, 'papel_azul_fondo.webp')
salida.save(ruta, lossless=True, method=6)
s = ImageStat.Stat(salida)
print('media', [round(v, 1) for v in s.mean], 'desviacion', [round(v, 1) for v in s.stddev], os.path.getsize(ruta), 'bytes')
