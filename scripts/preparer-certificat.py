"""
Redresse la photo du certificat DemoTech.

La photo est prise de biais, sur un lit. On corrige la perspective a partir des
quatre coins du document, puis on ajuste legerement la lumiere : le but est
qu'un recruteur puisse lire le texte, pas de faire joli.

Source : _sources/captures-one-zone/IMG_20260804_093708.jpg
Sortie  : src/assets/certificats/demotech-9.jpg
"""

from pathlib import Path

from PIL import Image, ImageEnhance

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "_sources" / "captures-one-zone" / "IMG_20260804_093708.jpg"
SORTIE = RACINE / "src" / "assets" / "certificats"

# Coins du certificat dans la photo d'origine (4080x3072), releves a la main :
# haut gauche, haut droit, bas droit, bas gauche.
COINS = [(300, 148), (4016, 100), (3982, 2852), (148, 2884)]

CIBLE = (1700, 1240)


def resoudre(matrice: list[list[float]], second: list[float]) -> list[float]:
    """Elimination de Gauss avec pivot partiel. Evite une dependance a numpy."""
    n = len(second)
    a = [ligne[:] + [second[i]] for i, ligne in enumerate(matrice)]

    for colonne in range(n):
        pivot = max(range(colonne, n), key=lambda l: abs(a[l][colonne]))
        a[colonne], a[pivot] = a[pivot], a[colonne]
        if abs(a[colonne][colonne]) < 1e-12:
            raise ValueError("systeme singulier : verifier les coins")
        for ligne in range(colonne + 1, n):
            facteur = a[ligne][colonne] / a[colonne][colonne]
            for k in range(colonne, n + 1):
                a[ligne][k] -= facteur * a[colonne][k]

    solution = [0.0] * n
    for ligne in range(n - 1, -1, -1):
        somme = sum(a[ligne][k] * solution[k] for k in range(ligne + 1, n))
        solution[ligne] = (a[ligne][n] - somme) / a[ligne][ligne]
    return solution


def coefficients(source: list[tuple[float, float]],
                 cible: list[tuple[float, float]]) -> list[float]:
    """
    Coefficients attendus par Image.transform en mode PERSPECTIVE.

    Pillow transforme la destination vers la source : les points de destination
    sont donc les entrees du systeme, et les points source les sorties.
    """
    matrice, second = [], []
    for (xc, yc), (xs, ys) in zip(cible, source):
        matrice.append([xc, yc, 1, 0, 0, 0, -xs * xc, -xs * yc])
        second.append(xs)
        matrice.append([0, 0, 0, xc, yc, 1, -ys * xc, -ys * yc])
        second.append(ys)
    return resoudre(matrice, second)


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"Photo introuvable : {SOURCE}")
    SORTIE.mkdir(parents=True, exist_ok=True)

    image = Image.open(SOURCE).convert("RGB")
    largeur, hauteur = CIBLE
    rectangle = [(0, 0), (largeur, 0), (largeur, hauteur), (0, hauteur)]

    coeffs = coefficients(COINS, rectangle)
    redresse = image.transform(CIBLE, Image.PERSPECTIVE, coeffs, Image.BICUBIC)

    # La photo est prise a la lumiere du jour, un peu grise. On raffermit
    # legerement, sans pousser au point de faire douter du document.
    redresse = ImageEnhance.Brightness(redresse).enhance(1.06)
    redresse = ImageEnhance.Contrast(redresse).enhance(1.14)
    redresse = ImageEnhance.Color(redresse).enhance(1.05)

    cible = SORTIE / "demotech-9.jpg"
    redresse.save(cible, quality=88, optimize=True, progressive=True)
    print(f"  {cible.name:<24} {redresse.size[0]}x{redresse.size[1]}  {cible.stat().st_size:>8} o")


if __name__ == "__main__":
    main()
