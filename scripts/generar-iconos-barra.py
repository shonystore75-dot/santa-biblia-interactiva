# Recorta los iconos de la barra inferior de la imagen de 5 iconos dorados sobre verde oscuro liso,
# quita el fondo y los recolorea: dorado metalico (barras oscuras) y bronce (Marfil). El amarillo original no se usa:
# solo su luminancia, para conservar el relieve.
# Uso: python scripts/generar-iconos-barra.py [imagen]   (por defecto resources/iconos/iconos-dorados-fuente.png)
# Salidas: nav-<icono>-oro.webp y nav-<icono>-bronce.webp (raiz), resources/iconos/engranaje-*.webp (no va en la app)
import importlib.util, os, sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
spec = importlib.util.spec_from_file_location('g', os.path.join(RAIZ, 'scripts', 'generar-temas.py'))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

RAMPAS = {
    # dorado metalico: sombra ambar profunda -> dorado aprobado (#F0CF72) -> brillo casi blanco
    'oro':    [(0.0, '#9A6612'), (0.30, '#C48E24'), (0.55, '#E2B440'), (0.75, '#F2CF6A'), (0.90, '#FCE79C'), (1.0, '#FFFBE6')],
    # bronce para la barra clara de Marfil: el cuerpo queda por debajo de #A8722E (3:1); solo los brillos son mas claros
    'bronce': [(0.0, '#2E1804'), (0.35, '#55300A'), (0.65, '#7C4C16'), (0.85, '#9C6726'), (0.95, '#B9843C'), (1.0, '#E4B770')],
}
LADO = 512          # lienzo cuadrado de cada icono
MARGEN_MIN = 16     # margen lateral del icono mas ancho (el libro); fija el alto comun de los cuatro
NITIDEZ = ImageFilter.UnsharpMask(radius=3, percent=70, threshold=1)   # realza los biseles, que a ~1/4 de tamano se pierden
# columnas de cada icono en la imagen original (2172 px de ancho)
ZONAS = {'inicio': (0, 460), 'leer': (460, 1008), 'guia': (1008, 1385), 'favoritos': (1385, 1780), 'engranaje': (1780, 2172)}
# huecos oscuros con un brillo que el umbral no distingue del dorado: se vacian con su poligono exacto
HUECOS = [
    [(251.2, 188.8), (370.8, 255.0), (127.3, 255.0)],                                             # triangulo del templo
    [(1581.7, 210), (1616, 296.7), (1712, 300.7), (1642.7, 361.7), (1663.5, 454), (1582.3, 403.3),
     (1498.8, 454), (1521.5, 361.7), (1452.8, 300.7), (1548, 296.7)],                             # centro de la estrella
]
ALFA_R0, ALFA_R1 = 60, 175     # canal rojo: <=R0 fondo (R~2), >=R1 dorado (tambien el naranja de las sombras), en medio borde suave


def mascara_huecos(tam, k=4):
    m = Image.new('L', (tam[0] * k, tam[1] * k), 0)
    d = ImageDraw.Draw(m)
    for p in HUECOS:
        d.polygon([(x * k, y * k) for x, y in p], fill=255)
    return m.resize(tam, Image.LANCZOS)


def color_rampa(rampa, t):
    for (t0, c0), (t1, c1) in zip(rampa, rampa[1:]):
        if t <= t1:
            u = (t - t0) / (t1 - t0)
            a, b = g.rgb(c0), g.rgb(c1)
            return [a[k] + (b[k] - a[k]) * u for k in range(3)]
    return g.rgb(rampa[-1][1])


def main(origen):
    im = Image.open(origen).convert('RGB')
    assert im.size == (2172, 724), 'las zonas y los huecos estan medidos sobre la imagen de 2172x724'
    alfa = im.getchannel('R').point(lambda v: max(0, min(255, round((v - ALFA_R0) * 255 / (ALFA_R1 - ALFA_R0)))))
    alfa = ImageChops.multiply(alfa, ImageChops.invert(mascara_huecos(im.size)))
    lum = im.convert('L')
    solido = alfa.point(lambda v: 255 if v >= 245 else 0)
    # en el borde la luminancia esta mezclada con el fondo: se toma la del dorado vecino (sin halo)
    interior = ImageChops.multiply(lum, solido)
    vecino = interior
    for _ in range(3):
        vecino = vecino.filter(ImageFilter.MaxFilter(3))
    lum = Image.composite(lum, vecino, solido)
    # percentiles comunes a los cinco, para que todos tengan el mismo reparto de luces y sombras
    h = interior.histogram(); h[0] = 0
    total = sum(h); ac = 0; p = []
    for v, n in enumerate(h):
        ac += n
        while len(p) < 2 and ac >= total * (0.02, 0.98)[len(p)]:
            p.append(v)
    bajo, alto = p
    t = lum.point(lambda v: max(0, min(255, round((v - bajo) * 255 / (alto - bajo)))))

    recortes = {}
    for n, (x0, x1) in ZONAS.items():
        a = alfa.crop((x0, 0, x1, im.size[1]))
        caja = a.point(lambda v: 255 if v > 24 else 0).getbbox()
        recortes[n] = (a.crop(caja), t.crop((x0, 0, x1, im.size[1])).crop(caja))
    barra = ('inicio', 'leer', 'guia', 'favoritos')
    aspecto = max(recortes[n][0].width / recortes[n][0].height for n in barra)
    alto_comun = int((LADO - 2 * MARGEN_MIN) / aspecto)
    destino_extra = os.path.join(RAIZ, 'resources', 'iconos')
    os.makedirs(destino_extra, exist_ok=True)
    for nombre, rampa in RAMPAS.items():
        lut = [color_rampa(rampa, v / 255) for v in range(256)]
        canales = [[round(c[k]) for c in lut] for k in range(3)]
        for n, (a, tt) in recortes.items():
            rgba = Image.merge('RGBA', [tt.point(c) for c in canales] + [a])
            ancho = round(a.width * alto_comun / a.height)
            rgba = rgba.convert('RGBa').resize((ancho, alto_comun), Image.LANCZOS).convert('RGBA')
            nitido = rgba.convert('RGB').filter(NITIDEZ); nitido.putalpha(rgba.getchannel('A')); rgba = nitido
            lienzo = Image.new('RGBA', (LADO, LADO), tuple(g.rgb(rampa[2][1])) + (0,))
            lienzo.paste(rgba, ((LADO - ancho) // 2, (LADO - alto_comun) // 2))
            ruta = (os.path.join(destino_extra, 'engranaje-%s.webp' % nombre) if n == 'engranaje'
                    else os.path.join(RAIZ, 'nav-%s-%s.webp' % (n, nombre)))
            lienzo.save(ruta, quality=95, alpha_quality=100, method=6)
            print(os.path.relpath(ruta, RAIZ), 'contenido %dx%d' % (ancho, alto_comun), os.path.getsize(ruta), 'bytes')


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(RAIZ, 'resources', 'iconos', 'iconos-dorados-fuente.png'))
