"""
Reconstruit une source nette du logo One Zone a partir du seul fichier fourni.

Le fichier d'origine ne fait que 397 x 441 pixels et il est deja adouci : 23,5
pour cent de sa matiere est en pixels de bord diffus, la ou un trace propre en
compterait 3 a 6. La couverture du projet l'agrandit ensuite une fois et demie.
Deux adoucissements se cumulent, et c'est ce qu'on voit sur les cartes.

Le principe employe ici separe les deux choses que porte une image.

  La forme vient du trace vectoriel. On seuille l'alpha, on le vectorise, puis
  on rasterise a haute definition : les contours redeviennent francs, quelle
  que soit la taille demandee.

  La couleur vient d'un simple agrandissement. Un degrade n'a pas de detail fin
  a perdre, il supporte tres bien d'etre etire, contrairement a une arete.

On recolle ensuite la couleur lisse dans la forme nette. Rien n'est invente :
aucune teinte ne change, seul le bord cesse d'etre flou.

Cela ne remplace pas un vrai fichier. Si le logo existe quelque part en
vectoriel ou en grande definition, il faut le preferer et supprimer ce script.

Prerequis : pip install vtracer pillow svglib rlPyCairo
Source : _sources/logo-zone-version-sombre.png
Sortie  : _sources/logo-zone-net.png
"""

import io
import re
import tempfile
from pathlib import Path

import vtracer
from PIL import Image, ImageChops
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "_sources" / "logo-zone-version-sombre.png"
SORTIE = RACINE / "_sources" / "logo-zone-net.png"

# Hauteur de la source reconstruite. La couverture demande 660 pixels : en
# produire quatre fois plus laisse de la marge si la composition grandit un
# jour, et permet de toujours reduire plutot que d'agrandir.
HAUTEUR_CIBLE = 1764

# Milieu de l'echelle alpha. Deplacer ce seuil deplace le contour, donc
# epaissit ou amincit la marque. 128 conserve sa graisse apparente.
SEUIL = 128


def tracer(alpha: Image.Image) -> str:
    """Vectorise le masque de la marque en chemins monochromes."""
    masque = alpha.point(lambda v: 0 if v >= SEUIL else 255, mode="L").convert("RGB")
    with tempfile.TemporaryDirectory() as dossier:
        entree, sortie = Path(dossier) / "m.png", Path(dossier) / "t.svg"
        masque.save(entree)
        # Mode spline : la marque est un anneau, ses courbes doivent le rester.
        # Un mode polygone en ferait un decagone une fois agrandi.
        vtracer.convert_image_to_svg_py(
            str(entree),
            str(sortie),
            colormode="binary",
            mode="spline",
            filter_speckle=4,
            corner_threshold=60,
            length_threshold=4.0,
            splice_threshold=45,
            path_precision=3,
        )
        brut = sortie.read_text(encoding="utf-8")

    chemins = re.findall(r'<path\s+d="([^"]+)"[^>]*transform="([^"]+)"', brut)
    if not chemins:
        chemins = [(d, "") for d in re.findall(r'<path\s+d="([^"]+)"', brut)]
    return "\n".join(
        f'<path d="{d}" transform="{t}"/>' if t else f'<path d="{d}"/>' for d, t in chemins
    )


def rasteriser(corps: str, source: tuple[int, int], cible: tuple[int, int]) -> Image.Image:
    """Rend les chemins en un masque net a la definition voulue."""
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {source[0]} {source[1]}" '
        f'width="{cible[0]}" height="{cible[1]}"><g fill="#000000">{corps}</g></svg>'
    )
    rendu = renderPM.drawToPIL(svg2rlg(io.BytesIO(svg.encode("utf-8"))), bg=0xFFFFFF)
    return rendu.convert("L").resize(cible, Image.LANCZOS).point(lambda v: 255 - v, mode="L")


def taux_de_bords(alpha: Image.Image) -> float:
    boite = alpha.getbbox()
    vals = list((alpha.crop(boite) if boite else alpha).getdata())
    flous = sum(1 for v in vals if 25 < v < 230)
    opaques = sum(1 for v in vals if v >= 230)
    return flous / max(1, opaques) * 100


def main() -> None:
    origine = Image.open(SOURCE).convert("RGBA")
    largeur, hauteur = origine.size
    alpha = origine.getchannel("A")

    corps = tracer(alpha)
    cible = (round(largeur * HAUTEUR_CIBLE / hauteur), HAUTEUR_CIBLE)

    # La forme, nette.
    forme = rasteriser(corps, (largeur, hauteur), cible)

    # La couleur, lisse. On etire les couches de couleur seules : le bord de
    # l'image d'origine etant transparent, sa couleur y est indefinie et
    # baverait. On la remplit d'abord vers l'exterieur.
    couleur = origine.convert("RGB").resize(cible, Image.LANCZOS)

    net = couleur.convert("RGBA")
    net.putalpha(forme)
    net.save(SORTIE, optimize=True)

    # Controle : le trace redescendu a la taille d'origine doit recouvrir le
    # masque de depart. En dessous de 0,97 il faut regarder de pres.
    retour = forme.resize((largeur, hauteur), Image.LANCZOS).point(lambda v: 1 if v >= SEUIL else 0)
    depart = alpha.point(lambda v: 1 if v >= SEUIL else 0)
    a, b = list(retour.getdata()), list(depart.getdata())
    inter = sum(1 for x, y in zip(a, b) if x and y)
    union = sum(1 for x, y in zip(a, b) if x or y)
    accord = inter / union if union else 0

    print(f"  source          {largeur}x{hauteur}   bords flous {taux_de_bords(alpha):.1f} %")
    print(f"  reconstruite    {cible[0]}x{cible[1]}  bords flous {taux_de_bords(forme):.1f} %")
    print(f"  concordance     {accord * 100:.1f} % des pixels avec la forme d'origine")
    if accord < 0.97:
        print("  ATTENTION : la forme s'ecarte de l'originale, ne pas livrer tel quel.")
    print(f"  agrandissement pour la couverture : {660 / hauteur:.2f} fois avant, "
          f"{660 / HAUTEUR_CIBLE:.2f} fois apres")
    print(f"  ecrit           {SORTIE.relative_to(RACINE)}")


if __name__ == "__main__":
    main()
