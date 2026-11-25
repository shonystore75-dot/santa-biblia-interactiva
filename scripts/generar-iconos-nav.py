# Genera la textura fuerte del marmol (marmol_marfil_fuerte.webp).
# Los iconos de la barra inferior se generan con scripts/generar-iconos-barra.py.
import os
from PIL import Image
RAIZ=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')

# Textura fuerte: el original tiene alfa maximo 110/255 (promedio ~4 %); se multiplica x4 (la intensidad se ajusta con --intensidad-marmol)
m=Image.open(os.path.join(RAIZ,'marmol_marfil_2026-11-22_2110.webp')).convert('RGBA')
a=m.getchannel('A').point(lambda v:min(255,int(v*4.0)))
m.putalpha(a); m.save(os.path.join(RAIZ,'marmol_marfil_fuerte.webp'),quality=88,method=6)
print('ok')
