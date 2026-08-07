"""
Prepare les visuels de One Zone a partir des captures de telephone.

One Zone est une application mobile : ce sont donc de vraies captures Android
qui servent, et non des recadrages d'une fenetre de bureau.

Sorties :
  src/assets/captures/one-zone-*.png   ecrans, statusbar retiree
  src/assets/captures/one-zone-cle.png couverture composee, trois ecrans

Source : _sources/captures-one-zone/
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "_sources" / "captures-one-zone"
SORTIE = RACINE / "src" / "assets" / "captures"

# Barre d'etat Android : heure, reseau, batterie. Rien d'utile, et cela date
# la capture inutilement.
STATUSBAR = 62

# Les captures retenues, dans l'ordre du recit de l'etude de cas.
ECRANS = [
    ("09-15-06-514", "accueil"),
    ("09-15-22-078", "publier"),
    ("09-15-30-462", "messagerie"),
    ("09-16-48-493", "badge-confiance"),
    ("09-18-20-336", "langues"),
    ("09-16-38-323", "equipe"),
    ("09-16-55-213", "portefeuille"),
    ("09-18-56-990", "one-view"),
]

# Les deux ecrans qui accompagnent la marque sur la couverture.
COUVERTURE_ECRANS = ["accueil", "publier"]

# Logo de l'application, variante destinee aux fonds sombres.
#
# On prefere la source reconstruite par vectoriser-logo-one-zone.py. Le fichier
# fourni ne fait que 397 x 441 pixels et ses bords sont deja adoucis : la
# composition l'agrandissait une fois et demie, et deux adoucissements se
# cumulaient. La version reconstruite fait 1764 pixels de haut, donc on reduit
# au lieu d'agrandir. L'original reste le repli et la source de verite.
LOGO_OZ_NET = RACINE / "_sources" / "logo-zone-net.png"
LOGO_OZ_ORIGINE = RACINE / "_sources" / "logo-zone-version-sombre.png"
LOGO_OZ = LOGO_OZ_NET if LOGO_OZ_NET.exists() else LOGO_OZ_ORIGINE
# Hauteur voulue pour la marque sur la couverture. La largeur suit le rapport
# d'origine : le logo n'est pas carre, le forcer dans un carre le deformerait.
LOGO_OZ_HAUTEUR = 660

# Les deux teintes dominantes du logo, relevees dans le fichier source. Le halo
# les reprend plutot que d'employer le bleu du site : une marque doit rayonner
# de sa propre couleur.
LOGO_OZ_CYAN = (24, 168, 240)
LOGO_OZ_VIOLET = (96, 48, 240)

FOND = (8, 9, 10)
ACCENT = (91, 140, 255)


def trouver(motif: str) -> Path | None:
    for fichier in SOURCE.glob("*.jpg"):
        if motif in fichier.name:
            return fichier
    return None


def coins_arrondis(image: Image.Image, rayon: int) -> Image.Image:
    """Applique des coins arrondis, comme un ecran de telephone."""
    masque = Image.new("L", image.size, 0)
    ImageDraw.Draw(masque).rounded_rectangle(
        [0, 0, image.size[0] - 1, image.size[1] - 1], radius=rayon, fill=255
    )
    resultat = image.convert("RGBA")
    resultat.putalpha(masque)
    return resultat


def ombre(taille: tuple[int, int], rayon: int, flou: int, opacite: int) -> Image.Image:
    calque = Image.new("RGBA", (taille[0] + flou * 4, taille[1] + flou * 4), (0, 0, 0, 0))
    ImageDraw.Draw(calque).rounded_rectangle(
        [flou * 2, flou * 2, flou * 2 + taille[0], flou * 2 + taille[1]],
        radius=rayon,
        fill=(0, 0, 0, opacite),
    )
    return calque.filter(ImageFilter.GaussianBlur(flou))


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


def preparer_ecran(chemin: Path) -> Image.Image:
    image = Image.open(chemin).convert("RGB")
    largeur, hauteur = image.size
    return image.crop((0, STATUSBAR, largeur, hauteur))


def composer_couverture(ecrans: dict[str, Image.Image]) -> Image.Image:
    """
    Visuel cle du projet : la marque One Zone a gauche, deux ecrans a droite.

    C'est la composition classique d'une fiche produit : on reconnait d'abord la
    marque, puis on voit ce qu'elle fait. Les telephones debordent par le bas,
    ce qui evite l'effet de vignette posee au milieu d'un cadre.
    """
    # La couverture est rendue en 2400 pixels de large et non en 1600.
    #
    # Sur un ecran a densite double, la fiche projet l'affiche jusqu'a environ
    # 2300 pixels reels : une toile de 1600 y etait agrandie de moitie avant
    # meme qu'on parle du logo. Deux agrandissements se cumulaient donc, et
    # c'est ce qui rendait la marque floue.
    taille = (2400, 1500)
    toile = Image.new("RGBA", taille, (*FOND, 255))
    toile.alpha_composite(halo(taille, (0.22, 0.42), 0.62, ACCENT, 0.3))
    toile.alpha_composite(halo(taille, (0.78, 0.16), 0.6, (126, 88, 255), 0.14))

    # ---- Les ecrans, a droite ----
    hauteur_tel = 1350
    espace = 60
    choisis = [ecrans[nom] for nom in COUVERTURE_ECRANS if nom in ecrans]

    vignettes = []
    for ecran in choisis:
        ratio = hauteur_tel / ecran.size[1]
        v = ecran.resize((int(ecran.size[0] * ratio), hauteur_tel), Image.LANCZOS)
        vignettes.append(coins_arrondis(v, 34))

    total = sum(v.size[0] for v in vignettes) + espace * (len(vignettes) - 1)
    x = taille[0] - total - 70
    positions = []
    for i, v in enumerate(vignettes):
        y = 74 if i == 0 else 122
        positions.append((x, y, v))
        x += v.size[0] + espace

    for px, py, v in positions:
        toile.alpha_composite(ombre(v.size, 34, 26, 150), (px - 52, py - 40))

    for px, py, v in positions:
        toile.alpha_composite(v, (px, py))
        cadre = Image.new("RGBA", v.size, (0, 0, 0, 0))
        ImageDraw.Draw(cadre).rounded_rectangle(
            [0, 0, v.size[0] - 1, v.size[1] - 1], radius=34, outline=(255, 255, 255, 40), width=2
        )
        toile.alpha_composite(cadre, (px, py))

    # ---- La marque, a gauche ----
    if LOGO_OZ.exists():
        source = Image.open(LOGO_OZ).convert("RGBA")
        facteur = LOGO_OZ_HAUTEUR / source.size[1]
        dimensions = (round(source.size[0] * facteur), LOGO_OZ_HAUTEUR)
        marque = source.resize(dimensions, Image.LANCZOS)

        # Renettoyage apres redimensionnement.
        #
        # Le lissage de Lanczos adoucit les aretes ; un masque flou leur rend
        # leur franchise. Il n'est applique qu'aux couches de couleur : le
        # canal alpha doit rester progressif, sinon le contour se crenelerait.
        # Reglage doux, parce qu'on reduit desormais au lieu d'agrandir : plus
        # fort, le trait prendrait un lisere clair.
        couleur = marque.convert("RGB").filter(
            ImageFilter.UnsharpMask(radius=1.1, percent=70, threshold=2)
        )
        marque = couleur.convert("RGBA")
        marque.putalpha(source.resize(dimensions, Image.LANCZOS).getchannel("A"))

        # Halo derriere la marque, en deux couches.
        #
        # Une couche large et sourde donne l'ambiance, une couche serree et vive
        # donne l'eclat. Une seule couche produirait soit une brume, soit un
        # cerne. Le masque est pose sur une toile plus grande, sinon le flou
        # serait coupe net au bord et laisserait un rectangle visible.
        alpha = marque.getchannel("A")
        marge = 150
        grand = Image.new("L", (dimensions[0] + marge * 2, dimensions[1] + marge * 2), 0)
        grand.paste(alpha, (marge, marge))

        lueur = Image.new("RGBA", grand.size, (0, 0, 0, 0))
        for rayon, force, teinte in (
            (72, 0.34, LOGO_OZ_VIOLET),
            (26, 0.46, LOGO_OZ_CYAN),
        ):
            voile = grand.filter(ImageFilter.GaussianBlur(rayon)).point(
                lambda v, f=force: int(v * f)
            )
            couche = Image.new("RGBA", grand.size, (*teinte, 0))
            couche.putalpha(voile)
            lueur.alpha_composite(couche)

        # Centre dans l'espace laisse libre a gauche des telephones.
        libre = positions[0][0] if positions else taille[0]
        mx = max(90, (libre - dimensions[0]) // 2)
        my = (taille[1] - dimensions[1]) // 2 - 30
        toile.alpha_composite(lueur, (mx - marge, my - marge))
        toile.alpha_composite(marque, (mx, my))

    return toile


def main() -> None:
    SORTIE.mkdir(parents=True, exist_ok=True)
    for ancien in SORTIE.glob("one-zone-*.png"):
        ancien.unlink()

    prepares: dict[str, Image.Image] = {}

    for motif, nom in ECRANS:
        chemin = trouver(motif)
        if not chemin:
            print(f"  MANQUANT {motif}")
            continue
        ecran = preparer_ecran(chemin)
        prepares[nom] = ecran
        cible = SORTIE / f"one-zone-{nom}.png"
        ecran.save(cible, optimize=True)
        print(f"  {cible.name:<32} {ecran.size[0]}x{ecran.size[1]}  {cible.stat().st_size:>8} o")

    if all(nom in prepares for nom in COUVERTURE_ECRANS):
        couverture = composer_couverture(prepares)
        cible = SORTIE / "one-zone-cle.png"
        couverture.convert("RGB").save(cible, optimize=True)
        print(f"  {cible.name:<32} {couverture.size[0]}x{couverture.size[1]}  {cible.stat().st_size:>8} o")


if __name__ == "__main__":
    main()
