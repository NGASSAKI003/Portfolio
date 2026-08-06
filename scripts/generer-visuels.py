"""
Genere les visuels de marque : couvertures de projet et images de partage.

  src/assets/couvertures/<slug>.png   1600x1000, illustration de la fiche projet
  public/og/<slug>.png                1200x630, carte WhatsApp / LinkedIn / X

Les couvertures sont des compositions abstraites tirees du trace du logo.
Elles sont volontairement neutres : le jour ou de vraies captures d'ecran sont
disponibles, il suffit de remplacer le fichier, le code ne bouge pas.

Prerequis : pip install pillow fonttools brotli svglib rlPyCairo
"""

import io
import math
import random
import re
import tempfile
from pathlib import Path

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg

RACINE = Path(__file__).resolve().parent
RACINE = RACINE.parent
CACHE = RACINE / "scripts" / ".cache"
COUVERTURES = RACINE / "src" / "assets" / "couvertures"
OG = RACINE / "public" / "og"
CONTENU = RACINE / "src" / "content" / "projets"

FOND = (8, 9, 10)
ENCRE = (242, 242, 243)
ENCRE_2 = (168, 168, 174)
ENCRE_3 = (126, 126, 136)
ACCENT = (91, 140, 255)

POLICES_SOURCE = {
    "serif": "node_modules/@fontsource/instrument-serif/files/instrument-serif-latin-400-normal.woff2",
    "sans": "node_modules/@fontsource-variable/inter/files/inter-latin-wght-normal.woff2",
    "mono": "node_modules/@fontsource-variable/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2",
}


# --------------------------------------------------------------------------
# Polices
# --------------------------------------------------------------------------

def polices() -> dict[str, Path]:
    """Convertit les woff2 du site en ttf utilisables par Pillow."""
    CACHE.mkdir(parents=True, exist_ok=True)
    resultat = {}
    for nom, relatif in POLICES_SOURCE.items():
        cible = CACHE / f"{nom}.ttf"
        if not cible.exists():
            police = TTFont(RACINE / relatif)
            police.flavor = None
            police.save(cible)
        resultat[nom] = cible
    return resultat


POLICES = polices()


def fonte(nom: str, taille: int, graisse: float | None = None) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(str(POLICES[nom]), taille)
    if graisse is not None:
        try:
            f.set_variation_by_axes([graisse])
        except OSError:
            pass
    return f


# --------------------------------------------------------------------------
# Marque
# --------------------------------------------------------------------------

def marque(largeur: int) -> Image.Image:
    """Rasterise le trace du logo en blanc sur fond transparent."""
    cle = CACHE / f"marque-{largeur}.png"
    if cle.exists():
        return Image.open(cle).convert("RGBA")

    # Le trace vit dans le module genere pour Astro : une seule source.
    module = (RACINE / "src" / "components" / "logo-path.ts").read_text(encoding="utf-8")
    boite = re.search(r"LOGO_VIEWBOX = '0 0 (\d+) (\d+)'", module)
    chemins = re.search(r"LOGO_PATHS = `(.*?)`;", module, re.S)
    if not boite or not chemins:
        raise SystemExit("logo-path.ts introuvable ou illisible, lancer generer-identite.py")
    lw, lh = int(boite.group(1)), int(boite.group(2))

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {lw} {lh}" '
        f'width="{lw}" height="{lh}">'
        f'<g fill="#ffffff">{chemins.group(1)}</g></svg>'
    )
    with tempfile.TemporaryDirectory() as dossier:
        fichier = Path(dossier) / "marque.svg"
        fichier.write_text(svg, encoding="utf-8")
        dessin = svg2rlg(str(fichier))
        facteur = largeur / dessin.width
        hauteur = int(round(dessin.height * facteur))
        dessin.scale(facteur, facteur)
        dessin.width, dessin.height = largeur, hauteur
        tampon = io.BytesIO()
        # Rendu blanc sur noir, puis le canal de luminance devient le canal alpha.
        renderPM.drawToFile(dessin, tampon, fmt="PNG", bg=0x000000)

    plat = Image.open(tampon).convert("L")
    resultat = Image.new("RGBA", plat.size, (255, 255, 255, 0))
    resultat.putalpha(plat)
    CACHE.mkdir(parents=True, exist_ok=True)
    resultat.save(cle)
    return resultat


# --------------------------------------------------------------------------
# Composition
# --------------------------------------------------------------------------

def halo(taille: tuple[int, int], centre: tuple[float, float], rayon: float,
         couleur: tuple[int, int, int], intensite: float) -> Image.Image:
    """Lueur radiale douce, additionnee au fond."""
    largeur, hauteur = taille
    petit = (max(1, largeur // 8), max(1, hauteur // 8))
    calque = Image.new("L", petit, 0)
    dessin = ImageDraw.Draw(calque)
    cx, cy = centre[0] * petit[0], centre[1] * petit[1]
    r = rayon * petit[0]
    etapes = 42
    for i in range(etapes, 0, -1):
        f = i / etapes
        valeur = int(255 * intensite * (1 - f) ** 2.2)
        dessin.ellipse([cx - r * f, cy - r * f, cx + r * f, cy + r * f], fill=valeur)
    calque = calque.filter(ImageFilter.GaussianBlur(petit[0] * 0.05))
    calque = calque.resize(taille, Image.BICUBIC)
    teinte = Image.new("RGB", taille, couleur)
    resultat = Image.new("RGBA", taille)
    resultat.paste(teinte, (0, 0))
    resultat.putalpha(calque)
    return resultat


def grille(taille: tuple[int, int], pas: int, opacite: int) -> Image.Image:
    largeur, hauteur = taille
    calque = Image.new("RGBA", taille, (0, 0, 0, 0))
    dessin = ImageDraw.Draw(calque)
    for x in range(0, largeur, pas):
        dessin.line([(x, 0), (x, hauteur)], fill=(255, 255, 255, opacite))
    for y in range(0, hauteur, pas):
        dessin.line([(0, y), (largeur, y)], fill=(255, 255, 255, opacite))
    return calque


def toile(taille: tuple[int, int], graine: int) -> Image.Image:
    """Fond commun a toutes les compositions : noir, lueurs, grille fine."""
    alea = random.Random(graine)
    image = Image.new("RGBA", taille, (*FOND, 255))

    cx = 0.18 + alea.random() * 0.64
    cy = 0.15 + alea.random() * 0.5
    image.alpha_composite(halo(taille, (cx, cy), 0.85, ACCENT, 0.42))
    image.alpha_composite(
        halo(taille, (1 - cx * 0.8, 0.95), 0.7, (120, 90, 255), 0.2)
    )
    image.alpha_composite(grille(taille, max(taille) // 28, 7))
    return image


def poser_marque(image: Image.Image, graine: int, echelle: float, opacite: int) -> None:
    """Pose le trace du logo, tourne et deborde du cadre, comme un element graphique."""
    alea = random.Random(graine * 7 + 3)
    largeur, hauteur = image.size
    m = marque(int(largeur * echelle))
    angle = alea.uniform(-16, 16)
    m = m.rotate(angle, resample=Image.BICUBIC, expand=True)

    teinte = Image.new("RGBA", m.size, (*ACCENT, 0))
    teinte.putalpha(m.getchannel("A").point(lambda v: int(v * opacite / 255)))

    x = int(largeur * alea.uniform(0.02, 0.3))
    y = int(hauteur * alea.uniform(0.1, 0.42))
    image.alpha_composite(teinte, (x, y))


def cadre(image: Image.Image) -> None:
    dessin = ImageDraw.Draw(image)
    largeur, hauteur = image.size
    dessin.rectangle([0, 0, largeur - 1, hauteur - 1], outline=(255, 255, 255, 26), width=1)


def couper(texte: str, police: ImageFont.FreeTypeFont, largeur_max: int) -> list[str]:
    mots, lignes, courante = texte.split(), [], ""
    for mot in mots:
        essai = f"{courante} {mot}".strip()
        if police.getlength(essai) <= largeur_max or not courante:
            courante = essai
        else:
            lignes.append(courante)
            courante = mot
    if courante:
        lignes.append(courante)
    return lignes


# --------------------------------------------------------------------------
# Sorties
# --------------------------------------------------------------------------

def couverture(slug: str, graine: int) -> Path:
    taille = (1600, 1000)
    image = toile(taille, graine)
    poser_marque(image, graine, echelle=0.85, opacite=54)
    image.alpha_composite(halo(taille, (0.5, 1.15), 0.9, FOND, 0.85))
    cadre(image)

    COUVERTURES.mkdir(parents=True, exist_ok=True)
    chemin = COUVERTURES / f"{slug}.png"
    image.convert("RGB").save(chemin, optimize=True)
    return chemin


def carte_partage(slug: str, titre: str, sous_titre: str, meta: str, graine: int) -> Path:
    taille = (1200, 630)
    image = toile(taille, graine)
    poser_marque(image, graine, echelle=0.62, opacite=34)
    image.alpha_composite(halo(taille, (0.35, 0.75), 1.0, FOND, 0.8))
    cadre(image)

    dessin = ImageDraw.Draw(image)
    marge = 72

    f_mono = fonte("mono", 21, 500)
    f_titre = fonte("serif", 76)
    f_sous = fonte("sans", 28, 400)
    f_pied = fonte("mono", 20, 500)

    dessin.text((marge, marge), meta.upper(), font=f_mono, fill=(*ACCENT, 255))

    y = marge + 92
    for ligne in couper(titre, f_titre, taille[0] - marge * 2)[:2]:
        dessin.text((marge, y), ligne, font=f_titre, fill=(*ENCRE, 255))
        y += 84

    y += 12
    for ligne in couper(sous_titre, f_sous, taille[0] - marge * 2 - 120)[:2]:
        dessin.text((marge, y), ligne, font=f_sous, fill=(*ENCRE_2, 255))
        y += 40

    dessin.line(
        [(marge, taille[1] - marge - 44), (taille[0] - marge, taille[1] - marge - 44)],
        fill=(255, 255, 255, 30),
        width=1,
    )
    dessin.text(
        (marge, taille[1] - marge - 26),
        "NGASSAKI-NDZA ANACLET JULIEN",
        font=f_pied,
        fill=(*ENCRE_3, 255),
    )
    droite = "DÉVELOPPEUR FULL STACK"
    dessin.text(
        (taille[0] - marge - f_pied.getlength(droite), taille[1] - marge - 26),
        droite,
        font=f_pied,
        fill=(*ENCRE_3, 255),
    )

    OG.mkdir(parents=True, exist_ok=True)
    chemin = OG / f"{slug}.png"
    image.convert("RGB").save(chemin, optimize=True)
    return chemin


def lire_frontmatter(fichier: Path) -> dict[str, str]:
    texte = fichier.read_text(encoding="utf-8")
    bloc = re.match(r"^---\r?\n(.*?)\r?\n---", texte, re.S)
    if not bloc:
        return {}
    champs = {}
    for ligne in bloc.group(1).splitlines():
        paire = re.match(r"^([a-zA-Zé]+):\s*(.+?)\s*$", ligne)
        if paire:
            champs[paire.group(1)] = paire.group(2).strip().strip("'\"")
    return champs


PAGES = [
    ("defaut", "NGASSAKI-NDZA Anaclet Julien", "Développeur full stack. Web, mobile, API et IA. Pointe-Noire, Congo.", "Portfolio", 11),
    ("projets", "Projets", "Ce que j'ai construit, comment, et ce que ça a donné.", "Sélection", 23),
    ("a-propos", "Parcours", "Génie informatique à l'ESTAM, Pointe-Noire. Ce que je sais faire et comment je travaille.", "À propos", 37),
    ("contact", "Travaillons ensemble", "Disponible immédiatement, sur site à Pointe-Noire ou à distance.", "Contact", 53),
]

COUVERTURES_PROJETS = [
    ("one-zone", 101),
    ("y-meni-sentinel", 211),
    ("portfolio-referencement", 307),
]


def main() -> None:
    for slug, graine in COUVERTURES_PROJETS:
        chemin = couverture(slug, graine)
        print(f"couverture  {chemin.name:<32} {chemin.stat().st_size:>8} o")

    for slug, titre, sous, meta, graine in PAGES:
        chemin = carte_partage(slug, titre, sous, meta, graine)
        print(f"partage     {chemin.name:<32} {chemin.stat().st_size:>8} o")

    if CONTENU.exists():
        for fichier in sorted(CONTENU.glob("*.mdx")) + sorted(CONTENU.glob("*.md")):
            champs = lire_frontmatter(fichier)
            if not champs:
                continue
            slug = fichier.stem
            graine = dict(COUVERTURES_PROJETS).get(slug, sum(map(ord, slug)))
            chemin = carte_partage(
                slug,
                champs.get("titre", slug),
                champs.get("sousTitre", ""),
                f"Projet · {champs.get('annee', '')}",
                graine,
            )
            print(f"partage     {chemin.name:<32} {chemin.stat().st_size:>8} o")


if __name__ == "__main__":
    main()
