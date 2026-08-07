"""
Exporte le logo One Zone en SVG, a partir du seul fichier raster disponible.

Aucune source vectorielle n'existe : ni dans le projet One Zone, ni dans ses
documents de vision, ni parmi les fichiers servis par le site en ligne, qui
plafonnent a 512 pixels. Ce script fabrique donc le vectoriel manquant.

Le mode couleur de vtracer ne convient pas ici : il decoupe le degrade en
tranches et produit 265 chemins pour 190 Ko. On procede autrement, en separant
ce que l'oeil separe deja.

  Le « 1 » est blanc : on l'isole a la saturation et on le trace a part.
  L'anneau et le « Z » portent le degrade : on les trace ensemble, et le
  degrade est reconstruit comme un vrai `linearGradient`, dont l'axe et les
  deux extremites sont ajustes sur les pixels d'origine par moindres carres.

Le resultat est independant de la resolution et tient en quelques kilooctets.
Il sert au portfolio, et il peut servir a One Zone lui-meme, dont les icones
souffrent du meme plafond de definition.

Prerequis : pip install vtracer pillow svglib rlPyCairo
Source : _sources/logo-zone-version-sombre.png
Sortie  : _sources/logo-one-zone.svg
"""

import colorsys
import io
import re
import tempfile
from pathlib import Path

import vtracer
from PIL import Image
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "_sources" / "logo-zone-version-sombre.png"
SORTIE = RACINE / "_sources" / "logo-one-zone.svg"

SEUIL_ALPHA = 128
# Au dela de cette valeur et en dessous de cette saturation, le pixel est du
# blanc du « 1 » et non une extremite claire du degrade.
SAT_MAX_BLANC = 0.22
VAL_MIN_BLANC = 0.72


def masques(image: Image.Image) -> tuple[Image.Image, Image.Image, list]:
    """Separe le « 1 » blanc du reste, et releve les pixels teintes."""
    largeur, hauteur = image.size
    px = image.load()
    blanc = Image.new("L", image.size, 0)
    teinte = Image.new("L", image.size, 0)
    pb, pt = blanc.load(), teinte.load()
    echantillons = []

    for y in range(hauteur):
        for x in range(largeur):
            r, g, b, a = px[x, y]
            if a < SEUIL_ALPHA:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if s < SAT_MAX_BLANC and v > VAL_MIN_BLANC:
                pb[x, y] = 255
            else:
                pt[x, y] = 255
                echantillons.append((x, y, r, g, b))
    return blanc, teinte, echantillons


def tracer(masque: Image.Image) -> str:
    """Vectorise un masque binaire en chemins."""
    if not masque.getbbox():
        return ""
    pour_trace = masque.point(lambda v: 0 if v > 127 else 255, mode="L").convert("RGB")
    with tempfile.TemporaryDirectory() as dossier:
        entree, sortie = Path(dossier) / "m.png", Path(dossier) / "t.svg"
        pour_trace.save(entree)
        vtracer.convert_image_to_svg_py(
            str(entree), str(sortie), colormode="binary", mode="spline",
            filter_speckle=4, corner_threshold=60, length_threshold=4.0,
            splice_threshold=45, path_precision=3,
        )
        brut = sortie.read_text(encoding="utf-8")

    chemins = re.findall(r'<path\s+d="([^"]+)"[^>]*transform="([^"]+)"', brut)
    if not chemins:
        chemins = [(d, "") for d in re.findall(r'<path\s+d="([^"]+)"', brut)]
    return "".join(
        f'<path d="{d}" transform="{t}"/>' if t else f'<path d="{d}"/>' for d, t in chemins
    )


def rasteriser(chemins: str, taille: tuple[int, int]) -> Image.Image:
    """
    Rend un jeu de chemins en masque, en aplat.

    Le degrade n'est volontairement pas demande ici : svglib ne sait pas le
    rendre. On recupere donc la seule geometrie, et la couleur est appliquee
    ensuite, ce qui reproduit exactement ce que dessinera un navigateur.
    """
    if not chemins:
        return Image.new("L", taille, 0)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {taille[0]} {taille[1]}" '
        f'width="{taille[0]}" height="{taille[1]}"><g fill="#000000">{chemins}</g></svg>'
    )
    rendu = renderPM.drawToPIL(svg2rlg(io.BytesIO(svg.encode("utf-8"))), bg=0xFFFFFF)
    return rendu.convert("L").resize(taille, Image.LANCZOS).point(lambda v: 255 - v, mode="L")


def nappe_degrade(taille, depart, arrivee, axe) -> Image.Image:
    """Reproduit en pixels le degrade que le SVG decrit, pour pouvoir le mesurer."""
    largeur, hauteur = taille
    dx, dy, pmin, pmax = axe
    etendue = (pmax - pmin) or 1e-6
    nappe = Image.new("RGB", taille)
    p = nappe.load()
    for y in range(hauteur):
        for x in range(largeur):
            t = (((x / largeur) * dx + (y / hauteur) * dy) - pmin) / etendue
            t = max(0.0, min(1.0, t))
            p[x, y] = tuple(round(depart[c] + (arrivee[c] - depart[c]) * t) for c in range(3))
    return nappe


def ajuster_degrade(echantillons: list, taille: tuple[int, int]) -> tuple:
    """
    Trouve l'axe du degrade et ses deux couleurs d'extremite.

    On projette chaque pixel sur un axe candidat, puis on ajuste une droite
    couleur = a + b * projection, canal par canal, par moindres carres. L'axe
    retenu est celui qui explique le mieux les couleurs observees.
    """
    largeur, hauteur = taille
    meilleur = None

    for angle_deg in range(0, 180, 5):
        rad = angle_deg * 3.141592653589793 / 180
        dx, dy = __import__("math").cos(rad), __import__("math").sin(rad)
        proj = [((x / largeur) * dx + (y / hauteur) * dy) for x, y, *_ in echantillons]
        pmin, pmax = min(proj), max(proj)
        if pmax - pmin < 1e-6:
            continue
        norm = [(p - pmin) / (pmax - pmin) for p in proj]

        residu = 0.0
        coeffs = []
        for canal in range(3):
            vals = [e[2 + canal] for e in echantillons]
            n = len(vals)
            sx = sum(norm); sy = sum(vals)
            sxx = sum(p * p for p in norm); sxy = sum(p * v for p, v in zip(norm, vals))
            det = n * sxx - sx * sx
            if abs(det) < 1e-9:
                b, a = 0.0, sy / n
            else:
                b = (n * sxy - sx * sy) / det
                a = (sy - b * sx) / n
            coeffs.append((a, b))
            residu += sum((a + b * p - v) ** 2 for p, v in zip(norm, vals))

        if meilleur is None or residu < meilleur[0]:
            meilleur = (residu, angle_deg, dx, dy, pmin, pmax, coeffs)

    residu, angle_deg, dx, dy, pmin, pmax, coeffs = meilleur
    borne = lambda v: max(0, min(255, round(v)))
    depart = tuple(borne(a) for a, b in coeffs)
    arrivee = tuple(borne(a + b) for a, b in coeffs)
    ecart = (residu / (3 * len(echantillons))) ** 0.5
    return depart, arrivee, (dx, dy, pmin, pmax), ecart, angle_deg


def main() -> None:
    image = Image.open(SOURCE).convert("RGBA")
    largeur, hauteur = image.size

    blanc, teinte, echantillons = masques(image)
    depart, arrivee, axe, ecart, angle = ajuster_degrade(echantillons, (largeur, hauteur))
    dx, dy, pmin, pmax = axe

    # Extremites de l'axe, ramenees dans le repere du dessin.
    x1, y1 = pmin * dx * largeur, pmin * dy * hauteur
    x2, y2 = pmax * dx * largeur, pmax * dy * hauteur

    chemins_teinte, chemins_blanc = tracer(teinte), tracer(blanc)
    hexa = lambda c: "#%02x%02x%02x" % c
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur} {hauteur}" width="{largeur}" height="{hauteur}">
<defs>
<linearGradient id="oz" gradientUnits="userSpaceOnUse" x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}">
<stop offset="0" stop-color="{hexa(depart)}"/>
<stop offset="1" stop-color="{hexa(arrivee)}"/>
</linearGradient>
</defs>
<g fill="url(#oz)">{chemins_teinte}</g>
<g fill="#f7f8fa">{chemins_blanc}</g>
</svg>
"""
    SORTIE.write_text(svg, encoding="utf-8")

    # Controle : on recompose le rendu attendu, puis on le compare a l'original
    # pose sur le meme fond. Un ecart moyen faible ne prouve pas que la forme
    # est juste, seulement que la couleur l'est : la forme, elle, a deja ete
    # verifiee par vectoriser-logo-one-zone.py, a 98,1 pour cent.
    m_teinte = rasteriser(chemins_teinte, (largeur, hauteur))
    m_blanc = rasteriser(chemins_blanc, (largeur, hauteur))
    rendu = Image.new("RGB", (largeur, hauteur), (8, 9, 10))
    rendu.paste(nappe_degrade((largeur, hauteur), depart, arrivee, (dx, dy, pmin, pmax)),
                (0, 0), m_teinte)
    rendu.paste(Image.new("RGB", (largeur, hauteur), (247, 248, 250)), (0, 0), m_blanc)

    ref = Image.new("RGBA", image.size, (8, 9, 10, 255))
    ref.alpha_composite(image)
    ref = ref.convert("RGB")
    a, b = list(rendu.getdata()), list(ref.getdata())
    diff = sum(sum(abs(u - v) for u, v in zip(p, q)) / 3 for p, q in zip(a, b)) / len(a)
    rendu.save(SORTIE.with_name("logo-one-zone-controle.png"))

    print(f"  axe du degrade      {angle} degres")
    print(f"  couleurs            {hexa(depart)} vers {hexa(arrivee)}")
    print(f"  ecart de l'ajustement {ecart:.1f} niveaux sur 255")
    print(f"  ecart au rendu       {diff:.1f} niveaux sur 255")
    print(f"  poids               {len(svg) / 1024:.1f} ko")
    print(f"  ecrit               {SORTIE.relative_to(RACINE)}")


if __name__ == "__main__":
    main()
