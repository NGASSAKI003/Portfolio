"""
Vectorise le sigle NNAJ, les quatre initiales, pour la barre haute.

Le fichier fourni est un JPEG noir sur blanc de 1024 x 1024 dans lequel le
sigle n'occupe que 469 x 89 pixels. Ce qui ressemble a des hachures dans les
diagonales est du bruit de compression, pas un parti pris de dessin : le trace
est fait de polygones pleins, et c'est cette silhouette que l'on garde. Elle
reste nette a n'importe quelle taille, prend la couleur du texte, et pese
quelques centaines d'octets la ou une image en aurait pese des milliers.

Prerequis : pip install vtracer pillow svglib rlPyCairo
Relancer uniquement si le sigle source change.

Source : _sources/sigle-nnaj.jpg
Sortie  : src/components/sigle-path.ts
"""

import io
import re
import tempfile
from pathlib import Path

import vtracer
from PIL import Image, ImageDraw, ImageFilter
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "_sources" / "sigle-nnaj.jpg"
COMPOSANTS = RACINE / "src" / "components"

# En dessous, le pixel est de l'encre. Le JPEG delave les bords, un seuil trop
# haut epaissirait le trace, un seuil trop bas le grignoterait.
SEUIL = 150


def masque_encre() -> Image.Image:
    """
    Reduit le JPEG a un noir et blanc franc, cadre sur le sigle.

    L'encre ressort en blanc pendant le nettoyage, ce qui rend les operations
    de morphologie lisibles : dilater agrandit la matiere, eroder la reduit.
    """
    gris = Image.open(SOURCE).convert("L")
    encre = gris.point(lambda v: 255 if v < SEUIL else 0, mode="L")

    boite = encre.getbbox()
    if boite is None:
        raise SystemExit("Aucune encre trouvee dans la source.")
    encre = encre.crop(boite)

    # Fermeture : dilatation puis erosion. Elle recolle les bords ronges par la
    # compression sans deplacer les contours, qui reviennent a leur place apres
    # l'erosion. Un noyau plus large emousserait les pointes du sigle.
    encre = encre.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.MinFilter(3))
    return boucher_trous(encre)


def boucher_trous(encre: Image.Image) -> Image.Image:
    """
    Comble les eclats blancs enfermes dans la matiere.

    La compression en a laisse un dans la barre du J. Une fermeture plus large
    en viendrait a bout mais arrondirait les angles vifs du dessin. On repere
    donc les trous par ce qu'ils sont vraiment : du fond qui ne communique pas
    avec l'exterieur. Une inondation partie du bord marque tout le fond
    exterieur, ce qui reste intact est un trou.
    """
    largeur, hauteur = encre.size
    fond = Image.new("L", (largeur + 2, hauteur + 2), 255)
    fond.paste(encre.point(lambda v: 0 if v > 127 else 255), (1, 1))

    ImageDraw.floodfill(fond, (0, 0), 128)

    trous = fond.crop((1, 1, largeur + 1, hauteur + 1)).point(
        lambda v: 255 if v == 255 else 0, mode="L"
    )
    resultat = encre.copy()
    resultat.paste(255, (0, 0), trous)
    return resultat


def vectoriser(encre: Image.Image) -> str:
    """
    Trace la silhouette en polygones.

    Le sigle n'a que des aretes droites et des angles vifs. Le mode spline,
    utilise pour le logo qui est tout en courbes, arrondirait ici les pointes.
    """
    # vtracer suit le noir : on rend donc l'encre noire et le fond blanc.
    pour_trace = encre.point(lambda v: 0 if v > 127 else 255, mode="L").convert("RGB")

    with tempfile.TemporaryDirectory() as dossier:
        entree = Path(dossier) / "masque.png"
        sortie = Path(dossier) / "trace.svg"
        pour_trace.save(entree)
        vtracer.convert_image_to_svg_py(
            str(entree),
            str(sortie),
            colormode="binary",
            mode="polygon",
            filter_speckle=6,
            path_precision=2,
        )
        brut = sortie.read_text(encoding="utf-8")

    chemins = re.findall(r'<path\s+d="([^"]+)"[^>]*transform="([^"]+)"', brut)
    if not chemins:
        chemins = [(d, "") for d in re.findall(r'<path\s+d="([^"]+)"', brut)]
    return "\n".join(
        f'<path d="{d}" transform="{t}"/>' if t else f'<path d="{d}"/>' for d, t in chemins
    )


def controler(corps: str, encre: Image.Image) -> float:
    """
    Compare le trace au masque d'origine, pixel par pixel.

    Une vectorisation qui se contenterait d'etre jolie a l'ecran peut avoir
    perdu une pointe ou ferme un creux. On rasterise donc le resultat et on
    mesure l'intersection sur l'union. En dessous de 0,97 il faut regarder.
    """
    largeur, hauteur = encre.size
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {largeur} {hauteur}" '
        f'width="{largeur}" height="{hauteur}">'
        f'<g fill="#000000">{corps}</g></svg>'
    )
    dessin = svg2rlg(io.BytesIO(svg.encode("utf-8")))
    rendu = renderPM.drawToPIL(dessin, bg=0xFFFFFF).convert("L").resize(
        (largeur, hauteur), Image.LANCZOS
    )
    retrace = rendu.point(lambda v: 255 if v < 128 else 0, mode="L")

    a = encre.point(lambda v: 1 if v > 127 else 0)
    b = retrace.point(lambda v: 1 if v > 127 else 0)
    pa, pb = list(a.getdata()), list(b.getdata())
    inter = sum(1 for x, y in zip(pa, pb) if x and y)
    union = sum(1 for x, y in zip(pa, pb) if x or y)
    return inter / union if union else 0.0


def main() -> None:
    encre = masque_encre()
    largeur, hauteur = encre.size
    corps = vectoriser(encre)

    accord = controler(corps, encre)
    print(f"  sigle         {largeur}x{hauteur}, rapport {largeur / hauteur:.2f}")
    print(f"  trace         {len(corps)} octets")
    print(f"  concordance   {accord * 100:.1f} % des pixels")
    if accord < 0.97:
        print("  ATTENTION : le trace s'ecarte du dessin d'origine, ne pas livrer tel quel.")

    module = (
        "// Genere par scripts/generer-sigle.py. Ne pas modifier a la main.\n"
        f"export const SIGLE_VIEWBOX = '0 0 {largeur} {hauteur}';\n"
        f"export const SIGLE_RATIO = {largeur / hauteur:.4f};\n"
        "export const SIGLE_PATHS = `\n" + corps.replace("`", "\\`") + "\n`;\n"
    )
    (COMPOSANTS / "sigle-path.ts").write_text(module, encoding="utf-8")
    print(f"  ecrit         src/components/sigle-path.ts")


if __name__ == "__main__":
    main()
