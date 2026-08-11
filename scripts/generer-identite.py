"""
Genere toute l'identite visuelle a partir du logo PNG d'origine.

Sorties :
  src/components/logo-path.ts   chemin vectoriel unique, recolore par variable CSS
  public/favicon.svg            tuile de marque, vectorielle
  public/favicon.ico            16 / 32 / 48 / 64
  public/apple-touch-icon.png   180x180
  public/icon-192.png           PWA
  public/icon-512.png           PWA
  public/icon-maskable-512.png  PWA, zone de securite respectee

Choix de la tuile : le logo dans ses bleus d'origine, pose sur fond blanc.
C'est l'option la plus lisible des deux cotes. La barre d'onglets est sombre
chez la plupart des gens, une tuile blanche s'y detache franchement, et elle
reste nette sur un navigateur en theme clair.

Prerequis : pip install vtracer pillow svglib rlPyCairo
Relancer uniquement si le logo source change.
"""

import io
import re
import tempfile
from pathlib import Path

import vtracer
from PIL import Image, ImageDraw
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "_sources" / "logo-version-claire.png"
PUBLIC = RACINE / "public"
COMPOSANTS = RACINE / "src" / "components"

TUILE_FOND = (255, 255, 255)
MARQUE_SOMBRE = (4, 34, 95)
MARQUE_CLAIR = (10, 74, 200)

# Marge autour de la marque, en fraction du cote de la tuile.
#
# La marque est presque deux fois plus large que haute : dans un carre, sa
# hauteur ne remplit qu'un peu plus du tiers, et une marge genereuse la rendait
# minuscule sur un ecran de telephone. Les coins d'une tuile arrondie restent
# vides de toute facon, la marque n'y touche jamais.
MARGE_TUILE = 0.05

# Marge de la version maskable, celle qu'Android decoupe lui-meme.
#
# Le disque de securite garanti par Android couvre 80 % du cote. S'y tenir
# strictement imposait une marque a 70 % de la tuile, soit bien plus petite que
# les 89 % affiches sur ordinateur, et l'ecart se voyait sur un telephone.
#
# Or ce disque est un minimum garanti, pas la forme reellement appliquee : la
# plupart des lanceurs decoupent un squircle, nettement plus large sur les
# flancs. Mesure faite sur la silhouette elle-meme, et non sur son cadre :
#
#     largeur    perdu sur cercle strict    perdu sur squircle
#       70 %             0,00 %                   0,00 %
#       78 %             0,36 %                   0,00 %
#       82 %             1,14 %                   0,00 %
#       90 %             3,38 %                   0,07 %
#
# Marge alignee sur celle de la tuile ordinaire, a sa demande expresse : il veut
# la meme taille de marque sur les deux appareils, et l'ecart de huit points se
# voyait. Sur un squircle, la forme qu'emploient la plupart des lanceurs, on n'y
# perd toujours rien. Sur un lanceur au masque parfaitement circulaire, l'extreme
# pointe des volutes est rognee. C'est un choix assume, pas un oubli.
MARGE_MASQUABLE = MARGE_TUILE


# --------------------------------------------------------------------------
# Vectorisation
# --------------------------------------------------------------------------

def tracer_masque() -> tuple[str, int, int]:
    """Vectorise le canal alpha du logo en un jeu de chemins monochromes."""
    image = Image.open(SOURCE).convert("RGBA")
    alpha = image.getchannel("A")
    alpha = alpha.crop(alpha.getbbox())
    largeur, hauteur = alpha.size

    masque = alpha.point(lambda v: 0 if v > 128 else 255, mode="L").convert("RGB")

    with tempfile.TemporaryDirectory() as dossier:
        entree = Path(dossier) / "masque.png"
        sortie = Path(dossier) / "trace.svg"
        masque.save(entree)
        vtracer.convert_image_to_svg_py(
            str(entree),
            str(sortie),
            colormode="binary",
            mode="spline",
            filter_speckle=8,
            corner_threshold=70,
            length_threshold=6.0,
            splice_threshold=55,
            path_precision=1,
        )
        brut = sortie.read_text(encoding="utf-8")

    # On conserve les translations produites par le traceur : elles font partie
    # de la geometrie. Seul le remplissage est retire, il vient du groupe parent.
    chemins = re.findall(r'<path\s+d="([^"]+)"[^>]*transform="([^"]+)"', brut)
    corps = "\n".join(f'<path d="{d}" transform="{t}"/>' for d, t in chemins)
    return corps, largeur, hauteur


# --------------------------------------------------------------------------
# Composition matricielle
#
# svglib ne sait pas rasteriser un degrade SVG. On lui demande donc seulement
# la silhouette de la marque, en aplat, et le degrade est applique par dessus
# avec Pillow. Le resultat est identique a la version vectorielle.
# --------------------------------------------------------------------------

def silhouette(corps: str, largeur: int, hauteur: int, cote: int, marge: float) -> Image.Image:
    """Rend la marque seule, en niveaux de gris, prete a servir de masque."""
    utile = cote * (1 - 2 * marge)
    facteur = min(utile / largeur, utile / hauteur)
    dx = (cote - largeur * facteur) / 2
    dy = (cote - hauteur * facteur) / 2

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {cote} {cote}" '
        f'width="{cote}" height="{cote}">'
        f'<rect width="{cote}" height="{cote}" fill="#000000"/>'
        f'<g transform="translate({dx:.2f} {dy:.2f}) scale({facteur:.5f})" fill="#ffffff">'
        f"{corps}</g></svg>"
    )

    with tempfile.TemporaryDirectory() as dossier:
        fichier = Path(dossier) / "silhouette.svg"
        fichier.write_text(svg, encoding="utf-8")
        dessin = svg2rlg(str(fichier))
        echelle = cote / dessin.width
        dessin.scale(echelle, echelle)
        dessin.width = dessin.height = cote
        tampon = io.BytesIO()
        renderPM.drawToFile(dessin, tampon, fmt="PNG", bg=0x000000)

    return Image.open(tampon).convert("L")


def degrade(cote: int) -> Image.Image:
    """Degrade diagonal, sombre aux extremites et clair au centre, comme l'original."""
    image = Image.new("RGB", (cote, cote))
    pixels = image.load()
    for y in range(cote):
        for x in range(cote):
            # Position le long de la diagonale, de 0 en bas a gauche a 1 en haut a droite.
            t = (x / cote + (cote - y) / cote) / 2
            # Deux segments : sombre -> clair -> sombre.
            f = t / 0.55 if t < 0.55 else (1 - t) / 0.45
            f = max(0.0, min(1.0, f))
            pixels[x, y] = tuple(
                int(MARQUE_SOMBRE[c] + (MARQUE_CLAIR[c] - MARQUE_SOMBRE[c]) * f)
                for c in range(3)
            )
    return image


def tuile(corps: str, largeur: int, hauteur: int, cote: int, rayon: int, marge: float) -> Image.Image:
    """Assemble le fond arrondi, le degrade et la silhouette de la marque."""
    fond = Image.new("RGBA", (cote, cote), (0, 0, 0, 0))
    dessin = ImageDraw.Draw(fond)
    dessin.rounded_rectangle([0, 0, cote - 1, cote - 1], radius=rayon, fill=(*TUILE_FOND, 255))

    masque = silhouette(corps, largeur, hauteur, cote, marge)
    marque = degrade(cote).convert("RGBA")
    marque.putalpha(masque)

    fond.alpha_composite(marque)
    return fond


def aplatir(image: Image.Image) -> Image.Image:
    """
    Aplatit sur la couleur de tuile, jamais sur du noir.

    `convert("RGB")` jette le canal alpha sans rien demander et laisse le noir
    apparaitre partout ou l'image etait transparente. C'est ce qui donnait des
    coins noirs aux icones une fois le site installe.
    """
    fond = Image.new("RGBA", image.size, (*TUILE_FOND, 255))
    fond.alpha_composite(image)
    return fond.convert("RGB")


def svg_tuile(corps: str, largeur: int, hauteur: int, rayon: float, marge: float) -> str:
    """Version vectorielle de la meme tuile, pour la favicon SVG."""
    cote = 512.0
    utile = cote * (1 - 2 * marge)
    facteur = min(utile / largeur, utile / hauteur)
    dx = (cote - largeur * facteur) / 2
    dy = (cote - hauteur * facteur) / 2
    sombre = "#%02x%02x%02x" % MARQUE_SOMBRE
    clair = "#%02x%02x%02x" % MARQUE_CLAIR
    fond = "#%02x%02x%02x" % TUILE_FOND
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
<defs>
<linearGradient id="marque" x1="0" y1="1" x2="1" y2="0">
<stop offset="0%" stop-color="{sombre}"/>
<stop offset="55%" stop-color="{clair}"/>
<stop offset="100%" stop-color="{sombre}"/>
</linearGradient>
</defs>
<rect width="512" height="512" rx="{rayon}" fill="{fond}"/>
<g transform="translate({dx:.2f} {dy:.2f}) scale({facteur:.5f})" fill="url(#marque)">
{corps}
</g>
</svg>
"""


def main() -> None:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    COMPOSANTS.mkdir(parents=True, exist_ok=True)

    corps, largeur, hauteur = tracer_masque()
    print(f"trace : {len(corps)} octets, viewBox 0 0 {largeur} {hauteur}")

    # 1. Chemin reutilisable par le composant Astro.
    module = (
        "// Genere par scripts/generer-identite.py. Ne pas modifier a la main.\n"
        f"export const LOGO_VIEWBOX = '0 0 {largeur} {hauteur}';\n"
        f"export const LOGO_RATIO = {largeur / hauteur:.4f};\n"
        "export const LOGO_PATHS = `\n" + corps.replace("`", "\\`") + "\n`;\n"
    )
    (COMPOSANTS / "logo-path.ts").write_text(module, encoding="utf-8")

    # 2. Favicon vectorielle. Marge serree : a seize pixels, chaque point compte.
    (PUBLIC / "favicon.svg").write_text(
        svg_tuile(corps, largeur, hauteur, rayon=112, marge=0.06), encoding="utf-8"
    )

    # 3. Icones installables. Chaque systeme a sa regle, aucune n'est la meme.
    #
    # Windows affiche le fichier tel quel, sans lui appliquer de forme : pour
    # qu'une icone y soit arrondie, c'est au fichier de porter l'arrondi, et
    # l'exterieur doit rester transparent. Un exterieur noir, c'est le defaut
    # d'origine, et un carre plein donnerait un carre plein sur le bureau.
    base = tuile(corps, largeur, hauteur, 512, rayon=112, marge=MARGE_TUILE)
    base.save(PUBLIC / "icon-512.png", optimize=True)
    base.resize((192, 192), Image.LANCZOS).save(PUBLIC / "icon-192.png", optimize=True)

    # iOS applique lui-meme son carre arrondi, et il ignore la transparence :
    # ce qu'il trouve de transparent, il le compose sur du noir. Ce fichier est
    # donc le seul qui doit rester un carre plein et opaque.
    aplatir(tuile(corps, largeur, hauteur, 512, rayon=0, marge=MARGE_TUILE)).resize(
        (180, 180), Image.LANCZOS
    ).save(PUBLIC / "apple-touch-icon.png", optimize=True)

    # 4. Version maskable. Android y decoupe la forme de son choix, cercle,
    #    goutte ou carre arrondi, et ne garantit que le disque central de 80 %.
    #    La marque etant tres large, sa hauteur compte autant que sa largeur
    #    dans ce disque : MARGE_MASQUABLE est calculee pour que les quatre coins
    #    de son cadre y tiennent, et pas seulement ses cotes.
    aplatir(tuile(corps, largeur, hauteur, 512, rayon=0, marge=MARGE_MASQUABLE)).save(
        PUBLIC / "icon-maskable-512.png", optimize=True
    )

    # 4bis. Version monochrome, pour les icones thematiques d'Android.
    #
    # Depuis Android 13, le systeme peut jeter les couleurs d'une icone, n'en
    # garder que la silhouette, et la reteindre avec la palette tiree du fond
    # d'ecran. C'est un reglage du telephone, pas un choix du site : quand il
    # est actif, aucune couleur envoyee ici ne sera respectee.
    #
    # Sans ce fichier, Android deduit la silhouette de l'icone couleur et le
    # resultat est approximatif. En la fournissant, on garde la main sur le
    # dessin meme quand on n'a plus la main sur la couleur. Le trace est blanc
    # sur transparent : seule l'opacite est lue, la couleur est ignoree.
    #
    # Meme marge que la version maskable, puisque le systeme la decoupe pareil.
    mono = Image.new("RGBA", (512, 512), (255, 255, 255, 255))
    mono.putalpha(silhouette(corps, largeur, hauteur, 512, MARGE_MASQUABLE))
    mono.save(PUBLIC / "icon-monochrome-512.png", optimize=True)

    # 5. ICO multi-resolution pour la barre d'onglets. Meme raison que Windows :
    #    aucun navigateur n'arrondit une favicon, donc le fichier s'en charge.
    tuile(corps, largeur, hauteur, 256, rayon=52, marge=0.06).save(
        PUBLIC / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)]
    )

    for fichier in sorted(PUBLIC.glob("*")):
        if fichier.is_file():
            print(f"  {fichier.name:<26} {fichier.stat().st_size:>8} octets")


if __name__ == "__main__":
    main()
