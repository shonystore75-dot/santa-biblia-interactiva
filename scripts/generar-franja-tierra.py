# Piedra de la franja inferior de Tierra biblica (barra de la app + zona de los botones de Android), a partir del zip
# Actualizacion_Tierra_Biblica_Franja_Inferior. Se usa UNA sola imagen para las dos zonas. Solo se recorta la banda que
# se llega a ver (la pantalla la dibuja a lo ancho, centrada), para que decodificarla no retrase el cambio de pantalla.
# Uso: python scripts/generar-franja-tierra.py <carpeta extraida del zip>   -> texturas/piedra_tierra_franja.webp
import sys, os, math
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageStat

BANDA = (0, 384, 1535, 896)   # franja central-baja de la foto: piedras del tamano del diseno aprobado
SALIDA = 'texturas/piedra_tierra_franja.webp'
COLOR, CONTRASTE, BRILLO = 1.18, 1.06, 0.95   # hacia el tono mas calido y con juntas mas marcadas del diseno aprobado

# La piedra grande que queda bajo la pestana Leer venia con vetas blancas y media cara gris: se le cambia SOLO la superficie
# (misma silueta y tamano) por la de una piedra vecina sin vetas, deformada para que su contorno coincida con el original.
VETEADA = [(520, 692), (545, 681), (580, 679), (615, 678), (655, 685), (680, 692), (705, 707), (722, 727), (742, 745), (755, 765), (760, 785),
           (759, 800), (764, 820), (757, 835), (735, 850), (710, 857), (680, 861), (640, 864), (602, 866), (570, 864), (550, 856), (535, 842),
           (520, 820), (513, 795), (511, 770), (506, 750), (502, 730), (508, 712)]
DONANTE = [(1029, 700), (1039, 679), (1061, 665), (1093, 660), (1120, 662), (1142, 673), (1166, 695), (1193, 719), (1215, 735), (1231, 754),
           (1235, 768), (1223, 778), (1201, 787), (1174, 800), (1147, 808), (1120, 810), (1093, 803), (1061, 797), (1034, 784), (1019, 765),
           (1016, 743), (1023, 719)]
GAMMA, LUZ = 0.82, 1.05   # la donante es mas oscura que las vecinas de la piedra sustituida: se aclaran sombras y brillo

def centro(p):
    xs, ys = [x for x, y in p], [y for x, y in p]
    return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2

def radio(p, c, dx, dy):
    """distancia del centro al contorno en la direccion (dx, dy), unitaria"""
    mejor = 0.0
    for (ax, ay), (bx, by) in zip(p, p[1:] + p[:1]):
        ex, ey = bx - ax, by - ay
        det = ex * dy - ey * dx
        if abs(det) < 1e-9: continue
        t = (ex * (ay - c[1]) - ey * (ax - c[0])) / det
        u = (dx * (ay - c[1]) - dy * (ax - c[0])) / det
        if t > 0 and -1e-6 <= u <= 1 + 1e-6: mejor = max(mejor, t)
    return mejor

def repintar(im):
    x0, y0 = min(x for x, y in VETEADA) - 8, min(y for x, y in VETEADA) - 8
    x1, y1 = max(x for x, y in VETEADA) + 8, max(y for x, y in VETEADA) + 8
    W, H = x1 - x0, y1 - y0
    forma = Image.new('L', (W * 4, H * 4), 0)
    ImageDraw.Draw(forma).polygon([((x - x0) * 4, (y - y0) * 4) for x, y in VETEADA], fill=255)
    forma = forma.resize((W, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.6))
    ca, cd = centro(VETEADA), centro(DONANTE)
    orig = im.load(); nueva = Image.new('RGB', (W, H)); o = nueva.load()
    for y in range(H):
        for x in range(W):
            dx, dy = x0 + x - ca[0], y0 + y - ca[1]
            r = math.hypot(dx, dy)
            if r < 1e-6: sx, sy = cd
            else:
                ux, uy = dx / r, dy / r
                k = radio(DONANTE, cd, ux, uy) / radio(VETEADA, ca, ux, uy)
                sx, sy = cd[0] + dx * k, cd[1] + dy * k
            ix, iy = int(sx), int(sy); fx, fy = sx - ix, sy - iy
            q = [orig[ix, iy], orig[ix + 1, iy], orig[ix, iy + 1], orig[ix + 1, iy + 1]]
            w = [(1 - fx) * (1 - fy), fx * (1 - fy), (1 - fx) * fy, fx * fy]
            o[x, y] = tuple(min(255, round(LUZ * 255 * (sum(q[j][c] * w[j] for j in range(4)) / 255) ** GAMMA)) for c in range(3))
    nueva = nueva.filter(ImageFilter.UnsharpMask(radius=1.2, percent=50, threshold=1))   # recupera el grano tras ampliar
    zona = im.crop((x0, y0, x1, y1))
    im = im.copy(); im.paste(Image.composite(nueva, zona, forma), (x0, y0))
    return im

if __name__ == '__main__':
    im = Image.open(os.path.join(sys.argv[1], '01_Texturas', 'piedra_tierra_original.webp')).convert('RGB')
    im = repintar(im).crop(BANDA)
    for mejora, k in ((ImageEnhance.Color, COLOR), (ImageEnhance.Contrast, CONTRASTE), (ImageEnhance.Brightness, BRILLO)):
        im = mejora(im).enhance(k)
    im.save(SALIDA, 'WEBP', quality=80, method=6)
    print(SALIDA, im.size, os.path.getsize(SALIDA), 'bytes, media #%02X%02X%02X' % tuple(round(x) for x in ImageStat.Stat(im).mean))
