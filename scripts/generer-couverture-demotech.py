"""
Compose la couverture du projet Y-MENI : l'affiche MineTech et le certificat.

L'affiche fournie ne fait que 392 x 512 pixels. L'agrandir seule sur toute une
couverture la rendrait floue. On la garde donc a une taille raisonnable, et on
lui adjoint le certificat, qui est en haute definition et porte le nom.

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

TAILLE = (1600, 1000)
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


def poser(toile: Image.Image, image: Image.Image, x: int, y: int, rayon: int) -> None:
    toile.alpha_composite(ombre(image.size, rayon, 24, 155), (x - 48, y - 36))
    toile.alpha_composite(coins_arrondis(image, rayon), (x, y))
    cadre = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(cadre).rounded_rectangle(
        [0, 0, image.size[0] - 1, image.size[1] - 1],
        radius=rayon,
        outline=(255, 255, 255, 46),
        width=2,
    )
    toile.alpha_composite(cadre, (x, y))


def main() -> None:
    if not AFFICHE.exists():
        raise SystemExit(f"Affiche introuvable : {AFFICHE}")
    SORTIE.mkdir(parents=True, exist_ok=True)

    toile = Image.new("RGBA", TAILLE, (*FOND, 255))
    toile.alpha_composite(halo(TAILLE, (0.28, 0.4), 0.6, ACCENT, 0.26))
    toile.alpha_composite(halo(TAILLE, (0.76, 0.72), 0.55, OR, 0.14))

    # Le certificat, en fond a droite. Il est en haute definition, il porte donc
    # la composition sans souffrir de l'agrandissement.
    cert = Image.open(CERTIFICAT).convert("RGB")
    hauteur_cert = 620
    cert = cert.resize(
        (int(cert.size[0] * hauteur_cert / cert.size[1]), hauteur_cert), Image.LANCZOS
    )
    poser(toile, cert, 690, 230, 18)

    # L'affiche, devant a gauche. Agrandissement limite a 1,3 fois : au dela,
    # le texte de l'affiche deviendrait illisible.
    affiche = Image.open(AFFICHE).convert("RGB")
    hauteur_affiche = min(760, int(affiche.size[1] * 1.3))
    affiche = affiche.resize(
        (int(affiche.size[0] * hauteur_affiche / affiche.size[1]), hauteur_affiche),
        Image.LANCZOS,
    )
    poser(toile, affiche, 150, (TAILLE[1] - hauteur_affiche) // 2, 16)

    cible = SORTIE / "demotech-9.png"
    toile.convert("RGB").save(cible, optimize=True)
    facteur = hauteur_affiche / Image.open(AFFICHE).size[1]
    print(f"  affiche agrandie {facteur:.2f} fois")
    print(f"  {cible.name:<24} {TAILLE[0]}x{TAILLE[1]}  {cible.stat().st_size:>8} o")


if __name__ == "__main__":
    main()
