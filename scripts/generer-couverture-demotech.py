"""
Compose la couverture du projet Y-MENI : l'affiche MineTech et le certificat.

Deux contraintes opposees gouvernent cette image.

Le certificat porte le nom en toutes lettres : c'est la piece qui prouve le
projet, elle doit etre lisible. Il arrive dans une maquette de 1800 x 1336 dont
le certificat n'occupe que 10 pour cent de la surface, le reste etant un cadre
sombre decoratif. On recadre donc la maquette pour ne garder que le document,
ce qui rend au certificat toute sa definition au lieu de l'agrandir a vide.

L'affiche, elle, ne fait que 396 x 505 pixels. C'est la piece faible : sa taille
dans la composition est calculee a rebours depuis l'agrandissement maximal
tolerable, jamais choisie a l'oeil.

Source : _sources/affiche-demotech-9.jpg
         src/assets/certificats/demotech-9-mockup.jpg
Sortie  : src/assets/couvertures/demotech-9.png
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

RACINE = Path(__file__).resolve().parent.parent
AFFICHE = RACINE / "_sources" / "affiche-demotech-9.jpg"
CERTIFICAT = RACINE / "src" / "assets" / "certificats" / "demotech-9-mockup.jpg"
SORTIE = RACINE / "src" / "assets" / "couvertures"

# La couverture est rendue en 2400 pixels de large et non en 1600.
#
# Sur un ecran a densite double, la fiche projet l'affiche jusqu'a environ
# 2300 pixels reels : une toile de 1600 y etait agrandie de moitie avant meme
# qu'on parle du contenu. Deux agrandissements se cumulaient.
TAILLE = (2400, 1500)

# Rapport entre un pixel de la toile et un pixel reel a l'ecran, dans le pire
# cas d'affichage. Il sert a dimensionner l'affiche : ce qui compte n'est pas
# son agrandissement sur la toile, c'est son agrandissement une fois affichee.
ECHELLE_AFFICHAGE = 2300 / TAILLE[0]

# Au dela, le texte de l'affiche se delite. Mesure a l'oeil sur la source.
PLAFOND_AGRANDISSEMENT = 1.35

# Part de la toile que laisse voir la banniere de la fiche projet, relevee sur
# le site construit : elle est plus large que la toile et rogne par le bas.
FRACTION_VISIBLE_BANNIERE = 0.847

FOND = (8, 9, 10)
ACCENT = (91, 140, 255)
OR = (217, 164, 65)


def coins_arrondis(image: Image.Image, rayon: int) -> Image.Image:
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


def halo(taille, centre, rayon, couleur, intensite) -> Image.Image:
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


def lueur_bord(taille, rayon_coins, flou, couleur, force):
    """
    Nappe de couleur derriere une piece, qui la decolle du fond noir.

    Le masque est dessine sur une toile plus grande que la piece, sinon le flou
    serait coupe net au bord et laisserait voir un rectangle.
    """
    marge = flou * 3
    calque = Image.new("L", (taille[0] + marge * 2, taille[1] + marge * 2), 0)
    ImageDraw.Draw(calque).rounded_rectangle(
        [marge, marge, marge + taille[0], marge + taille[1]], radius=rayon_coins, fill=255
    )
    calque = calque.filter(ImageFilter.GaussianBlur(flou)).point(lambda v: int(v * force))
    teinte = Image.new("RGBA", calque.size, (*couleur, 0))
    teinte.putalpha(calque)
    return teinte, marge


def renetteter(image: Image.Image, rayon: float, pourcent: int) -> Image.Image:
    """
    Rend leurs aretes aux images redimensionnees.

    Lanczos adoucit toujours un peu ; un masque flou rend au texte sa franchise.
    Sans cela, une affiche agrandie parait delavee meme a la bonne taille.
    """
    return image.filter(ImageFilter.UnsharpMask(radius=rayon, percent=pourcent, threshold=2))


def recadrer_maquette(chemin: Path) -> Image.Image:
    """
    Extrait le document de son cadre de maquette.

    Le cadre est d'une seule couleur, relevee dans un coin. On garde la boite
    englobante des pixels qui s'en ecartent. Le calcul est refait a chaque
    execution : si la maquette change, le recadrage suit sans retouche.
    """
    image = Image.open(chemin).convert("RGB")
    largeur, hauteur = image.size
    px = image.load()
    cadre = px[8, 8]

    def etranger(x: int, y: int) -> bool:
        c = px[x, y]
        return max(abs(c[i] - cadre[i]) for i in range(3)) > 40

    # Une ligne appartient au document si la moitie de ses pixels s'ecartent du
    # cadre. Le seuil evite qu'un reflet isole n'elargisse le recadrage.
    lignes = [y for y in range(hauteur)
              if sum(etranger(x, y) for x in range(0, largeur, 4)) > largeur / 8]
    colonnes = [x for x in range(largeur)
                if sum(etranger(x, y) for y in range(0, hauteur, 4)) > hauteur / 8]
    if not lignes or not colonnes:
        return image
    return image.crop((colonnes[0], lignes[0], colonnes[-1] + 1, lignes[-1] + 1))


def poser(toile, image, x, y, rayon, teinte, force) -> None:
    nappe, marge = lueur_bord(image.size, rayon, 90, teinte, force)
    toile.alpha_composite(nappe, (x - marge, y - marge))
    toile.alpha_composite(ombre(image.size, rayon, 34, 155), (x - 68, y - 52))
    toile.alpha_composite(coins_arrondis(image, rayon), (x, y))
    cadre = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(cadre).rounded_rectangle(
        [0, 0, image.size[0] - 1, image.size[1] - 1],
        radius=rayon,
        outline=(255, 255, 255, 46),
        width=3,
    )
    toile.alpha_composite(cadre, (x, y))


def ajuster(image: Image.Image, hauteur: int) -> Image.Image:
    largeur = round(image.size[0] * hauteur / image.size[1])
    return image.resize((largeur, hauteur), Image.LANCZOS)


def main() -> None:
    if not AFFICHE.exists():
        raise SystemExit(f"Affiche introuvable : {AFFICHE}")
    SORTIE.mkdir(parents=True, exist_ok=True)

    toile = Image.new("RGBA", TAILLE, (*FOND, 255))
    toile.alpha_composite(halo(TAILLE, (0.18, 0.5), 0.52, ACCENT, 0.26))
    toile.alpha_composite(halo(TAILLE, (0.68, 0.46), 0.62, OR, 0.17))

    # ---- Le certificat, piece principale ----
    #
    # Il est desormais assez grand pour que le nom se lise sur la vignette
    # elle-meme, sans ouvrir la fiche. C'est la seule image du site qui porte
    # une preuve exterieure : autant qu'elle se donne a lire.
    source_cert = recadrer_maquette(CERTIFICAT)
    hauteur_cert = 980
    cert = renetteter(ajuster(source_cert, hauteur_cert), 1.4, 85)

    # ---- L'affiche, piece secondaire ----
    #
    # Sa hauteur decoule du plafond d'agrandissement, elle n'est pas choisie.
    # Une affiche plus grande serait une affiche floue.
    source_affiche = Image.open(AFFICHE).convert("RGB")
    hauteur_affiche = round(
        source_affiche.size[1] * PLAFOND_AGRANDISSEMENT / ECHELLE_AFFICHAGE
    )
    affiche = renetteter(ajuster(source_affiche, hauteur_affiche), 1.9, 120)

    # Les deux pieces cote a cote, gouttiere au milieu, l'ensemble centre.
    gouttiere = 120
    total = affiche.size[0] + gouttiere + cert.size[0]
    x = (TAILLE[0] - total) // 2

    # La composition est remontee.
    #
    # La couverture sert a deux cadrages differents. La carte de la liste est
    # en 16/10, soit exactement la toile : tout est visible. La banniere de la
    # fiche projet est plus large que haute et rogne par le bas ; mesuree, elle
    # ne laisse voir que les 85 premiers pour cent. Centrer sur la toile
    # tronquait le bas du certificat, centrer sur la bande visible creusait un
    # vide sous la carte. Le centre retenu est a mi-chemin des deux.
    centre = round(TAILLE[1] * (1 + FRACTION_VISIBLE_BANNIERE) / 4)

    poser(toile, affiche, x, centre - hauteur_affiche // 2, 18, ACCENT, 0.30)
    poser(toile, cert, x + affiche.size[0] + gouttiere,
          centre - hauteur_cert // 2, 20, OR, 0.34)

    cible = SORTIE / "demotech-9.png"
    toile.convert("RGB").save(cible, optimize=True)

    print(f"  maquette      {Image.open(CERTIFICAT).size[0]}x{Image.open(CERTIFICAT).size[1]}"
          f"  recadree en {source_cert.size[0]}x{source_cert.size[1]}")
    print(f"  certificat    {cert.size[0]}x{cert.size[1]}"
          f"   affiche a {hauteur_cert * ECHELLE_AFFICHAGE / source_cert.size[1]:.2f} fois sa taille")
    print(f"  affiche       {affiche.size[0]}x{affiche.size[1]}"
          f"   affichee a {PLAFOND_AGRANDISSEMENT:.2f} fois sa taille")
    print(f"  {cible.name:<24} {TAILLE[0]}x{TAILLE[1]}  {cible.stat().st_size:>9} o")


if __name__ == "__main__":
    main()
