"""
Compose la couverture du projet « Ce portfolio » : le logo, en couleur, sur le
fond de marque.

Le trace vient du meme module que le reste du site, donc la forme est
rigoureusement identique a celle de l'en-tete et de la constellation.

Sortie : src/assets/couvertures/portfolio-logo.png
"""

import io
import re
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "src" / "assets" / "couvertures"

TAILLE = (1600, 1000)
FOND = (8, 9, 10)
ACCENT = (91, 140, 255)
# Les deux bleus du logo, du plus sombre au plus clair.
LOGO_SOMBRE = (11, 63, 168)
LOGO_CLAIR = (109, 168, 255)


def trace_logo() -> tuple[str, int, int]:
    module = (RACINE / "src" / "components" / "logo-path.ts").read_text(encoding="utf-8")
    boite = re.search(r"LOGO_VIEWBOX = '0 0 (\d+) (\d+)'", module)
    chemins = re.search(r"LOGO_PATHS = `(.*?)`;", module, re.S)
    if not boite or not chemins:
        raise SystemExit("logo-path.ts introuvable, lancer generer-identite.py")
    return chemins.group(1), int(boite.group(1)), int(boite.group(2))


def silhouette(corps: str, lw: int, lh: int, largeur: int) -> Image.Image:
    """Rasterise la marque en niveaux de gris, pour servir de masque."""
    hauteur = int(round(largeur * lh / lw))
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {lw} {lh}" '
        f'width="{lw}" height="{lh}">'
        f'<rect width="{lw}" height="{lh}" fill="#000000"/>'
        f'<g fill="#ffffff">{corps}</g></svg>'
    )
    with tempfile.TemporaryDirectory() as dossier:
        fichier = Path(dossier) / "marque.svg"
        fichier.write_text(svg, encoding="utf-8")
        dessin = svg2rlg(str(fichier))
        echelle = largeur / dessin.width
        dessin.scale(echelle, echelle)
        dessin.width, dessin.height = largeur, hauteur
        tampon = io.BytesIO()
        renderPM.drawToFile(dessin, tampon, fmt="PNG", bg=0x000000)
    return Image.open(tampon).convert("L")


def degrade(taille: tuple[int, int]) -> Image.Image:
    """Degrade diagonal reprenant les bleus du logo d'origine."""
    largeur, hauteur = taille
    image = Image.new("RGB", taille)
    pixels = image.load()
    for y in range(hauteur):
        for x in range(largeur):
            t = (x / largeur + (hauteur - y) / hauteur) / 2
            f = t / 0.55 if t < 0.55 else (1 - t) / 0.45
            f = max(0.0, min(1.0, f))
            pixels[x, y] = tuple(
                int(LOGO_SOMBRE[c] + (LOGO_CLAIR[c] - LOGO_SOMBRE[c]) * f) for c in range(3)
            )
    return image


def halo(taille: tuple[int, int], centre: tuple[float, float], rayon: float,
         couleur: tuple[int, int, int], intensite: float) -> Image.Image:
    largeur, hauteur = taille
    petit = (max(1, largeur // 8), max(1, hauteur // 8))
    calque = Image.new("L", petit, 0)
    dessin = ImageDraw.Draw(calque)
    cx, cy = centre[0] * petit[0], centre[1] * petit[1]
    r = rayon * petit[0]
    for i in range(40, 0, -1):
        f = i / 40
        dessin.ellipse(
            [cx - r * f, cy - r * f, cx + r * f, cy + r * f],
            fill=int(255 * intensite * (1 - f) ** 2.2),
        )
    calque = calque.filter(ImageFilter.GaussianBlur(petit[0] * 0.05)).resize(taille, Image.BICUBIC)
    teinte = Image.new("RGBA", taille, (*couleur, 0))
    teinte.putalpha(calque)
    return teinte


def grille(taille: tuple[int, int], pas: int, opacite: int) -> Image.Image:
    calque = Image.new("RGBA", taille, (0, 0, 0, 0))
    dessin = ImageDraw.Draw(calque)
    for x in range(0, taille[0], pas):
        dessin.line([(x, 0), (x, taille[1])], fill=(255, 255, 255, opacite))
    for y in range(0, taille[1], pas):
        dessin.line([(0, y), (taille[0], y)], fill=(255, 255, 255, opacite))
    return calque


def main() -> None:
    SORTIE.mkdir(parents=True, exist_ok=True)
    corps, lw, lh = trace_logo()

    toile = Image.new("RGBA", TAILLE, (*FOND, 255))
    toile.alpha_composite(halo(TAILLE, (0.5, 0.44), 0.72, ACCENT, 0.3))
    toile.alpha_composite(grille(TAILLE, TAILLE[0] // 26, 7))

    # La marque occupe 62 % de la largeur, centree.
    largeur_marque = int(TAILLE[0] * 0.62)
    masque = silhouette(corps, lw, lh, largeur_marque)
    marque = degrade(masque.size).convert("RGBA")
    marque.putalpha(masque)

    # Halo diffus derriere la marque, pour la decoller du fond.
    #
    # Le masque est d'abord pose sur une toile plus grande : sans cette marge,
    # le flou serait coupe net au bord du cadre et laisserait un rectangle
    # visible autour du logo.
    marge = 90
    grand = Image.new("L", (masque.size[0] + marge * 2, masque.size[1] + marge * 2), 0)
    grand.paste(masque, (marge, marge))
    voile = grand.filter(ImageFilter.GaussianBlur(30)).point(lambda v: int(v * 0.42))

    lueur = Image.new("RGBA", grand.size, (*ACCENT, 0))
    lueur.putalpha(voile)

    x = (TAILLE[0] - masque.size[0]) // 2
    y = (TAILLE[1] - masque.size[1]) // 2
    toile.alpha_composite(lueur, (x - marge, y - marge))
    toile.alpha_composite(marque, (x, y))

    cible = SORTIE / "portfolio-logo.png"
    toile.convert("RGB").save(cible, optimize=True)
    print(f"  {cible.name:<28} {TAILLE[0]}x{TAILLE[1]}  {cible.stat().st_size:>8} o")


if __name__ == "__main__":
    main()
