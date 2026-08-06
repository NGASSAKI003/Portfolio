"""
Reduit les polices aux caracteres reellement necessaires au site.

Les paquets fontsource livrent le cyrillique, le grec, le vietnamien et tout
l'axe de graisse d'une variable. Sur un site en francais, c'est du poids paye
pour rien. On ne garde que le jeu latin francais, avec de la marge.

Sortie :
  src/styles/polices/*.woff2   polices reduites
  src/styles/polices.css       declarations @font-face correspondantes

Prerequis : pip install fonttools brotli
Relancer si la liste des caracteres doit s'elargir.
"""

import io
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

RACINE = Path(__file__).resolve().parent.parent
SORTIE = RACINE / "src" / "styles" / "polices"

# Jeu de caracteres : ASCII imprimable, plus tout ce dont le francais a besoin,
# plus la ponctuation typographique employee sur le site. Volontairement large,
# pour qu'un futur texte ne fasse pas apparaitre de carre vide.
CARACTERES = (
    "".join(chr(c) for c in range(0x20, 0x7F))
    + "ÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŸÆŒàâäçéèêëîïôöùûüÿæœ"
    + "ÁÍÓÚÑáíóúñ"  # noms propres hispanophones ou lusophones
    + " "  # espace insecable
    + " "  # espace fine insecable, avant : ; ! ? en francais
    + "«»‘’“”–—…·•€£©®°№→←↑↓×÷±≈≤≥™✓"
)

#
# Trois familles : un serif de titrage, une grotesque de texte, une monospace
# pour les etiquettes. Le contraste entre les trois porte la hierarchie.
#
POLICES = [
    {
        "id": "inter",
        "famille": "Inter",
        "source": "node_modules/@fontsource-variable/inter/files/inter-latin-wght-normal.woff2",
        "style": "normal",
        # Le site n'emploie que 400, 500 et 600. Conserver l'axe complet de 100 a
        # 900 reviendrait a payer six graisses jamais affichees.
        "axe": {"wght": (400, 600)},
        "graisse": "400 600",
        # Metriques de la police de repli, pour que la substitution ne decale rien.
        "repli": {
            "local": "Segoe UI",
            "size-adjust": "107%",
            "ascent-override": "90%",
            "descent-override": "22.5%",
            "line-gap-override": "0%",
        },
    },
    {
        "id": "instrument-serif",
        "famille": "Instrument Serif",
        "source": "node_modules/@fontsource/instrument-serif/files/instrument-serif-latin-400-normal.woff2",
        "style": "normal",
        "graisse": "400",
        "repli": {
            "local": "Georgia",
            "size-adjust": "88%",
            "ascent-override": "104%",
            "descent-override": "26%",
            "line-gap-override": "0%",
        },
    },
    {
        "id": "jetbrains-mono",
        "famille": "JetBrains Mono",
        "source": "node_modules/@fontsource-variable/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2",
        "style": "normal",
        # La monospace ne sert qu'aux petites etiquettes, en 500 et 600.
        "axe": {"wght": (500, 600)},
        "graisse": "500 600",
        "repli": {
            "local": "Consolas",
            "size-adjust": "100%",
            "ascent-override": "102%",
            "descent-override": "30%",
            "line-gap-override": "0%",
        },
    },
]


def reduire(source: Path, cible: Path, axe: dict | None = None) -> tuple[int, int]:
    police = TTFont(source)
    avant = source.stat().st_size

    # Restriction de l'axe variable avant le sous-ensemble : les deltas des
    # graisses inutilisees representent l'essentiel du poids d'une variable.
    if axe and "fvar" in police:
        police = instantiateVariableFont(police, axe, updateFontNames=False)
        # Recompilation complete : l'instanciation laisse des references
        # paresseuses vers des glyphes disparus, que le sous-ensemble suivant
        # irait chercher en vain.
        tampon = io.BytesIO()
        police.flavor = None
        police.save(tampon)
        tampon.seek(0)
        police = TTFont(tampon)

    options = subset.Options()
    options.flavor = "woff2"
    options.desubroutinize = False
    options.hinting = True
    options.legacy_kern = False
    options.name_IDs = ["*"]
    options.name_legacy = False
    options.notdef_outline = False
    options.recalc_bounds = True
    # On conserve l'axe de graisse : les variables restent variables.
    options.retain_gids = False
    options.layout_features = ["*"]

    reducteur = subset.Subsetter(options=options)
    reducteur.populate(text=CARACTERES)
    reducteur.subset(police)

    police.flavor = "woff2"
    police.save(cible)
    return avant, cible.stat().st_size


def main() -> None:
    SORTIE.mkdir(parents=True, exist_ok=True)
    declarations = [
        "/*",
        " * Genere par scripts/sous-ensembler-polices.py. Ne pas modifier a la main.",
        " *",
        " * Polices auto-hebergees et reduites au jeu latin francais. Aucun appel a",
        " * un service tiers : sur une connexion moyenne, une connexion reseau",
        " * supplementaire coute plus cher que les octets qu'elle economiserait.",
        " */",
        "",
    ]

    total_avant = total_apres = 0

    for police in POLICES:
        source = RACINE / police["source"]
        cible = SORTIE / f"{police['id']}.woff2"
        avant, apres = reduire(source, cible, police.get("axe"))
        total_avant += avant
        total_apres += apres
        print(f"{police['id']:<28} {avant:>7} o  ->  {apres:>6} o   ({100 - apres * 100 // avant} % en moins)")

        declarations += [
            "@font-face {",
            f"  font-family: '{police['famille']}';",
            f"  font-style: {police['style']};",
            f"  font-weight: {police['graisse']};",
            "  font-display: swap;",
            f"  src: url('./polices/{police['id']}.woff2') format('woff2');",
            "}",
            "",
        ]

        repli = police.get("repli")
        if repli:
            # Police de repli calee sur les memes metriques : le texte ne saute pas
            # au moment ou la vraie police arrive.
            declarations += [
                "@font-face {",
                f"  font-family: '{police['famille']} repli';",
                f"  src: local('{repli['local']}'), local('Arial');",
                f"  size-adjust: {repli['size-adjust']};",
                f"  ascent-override: {repli['ascent-override']};",
                f"  descent-override: {repli['descent-override']};",
                f"  line-gap-override: {repli['line-gap-override']};",
                "}",
                "",
            ]

    (RACINE / "src" / "styles" / "polices.css").write_text(
        "\n".join(declarations), encoding="utf-8"
    )

    print(f"{'TOTAL':<28} {total_avant:>7} o  ->  {total_apres:>6} o   "
          f"({100 - total_apres * 100 // total_avant} % en moins)")


if __name__ == "__main__":
    main()
