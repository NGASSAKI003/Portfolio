/**
 * Ajustement des couleurs de marque.
 *
 * Les couleurs officielles des technologies sont faites pour un fond blanc.
 * Sur fond noir, celles d'Express, de Next.js ou de GitHub deviennent
 * invisibles. On les eclaircit ou on les assombrit juste ce qu'il faut pour
 * atteindre un rapport de contraste utilisable, sans les denaturer.
 */

type Rvb = [number, number, number];

function versRvb(hex: string): Rvb {
  const propre = hex.replace('#', '');
  const complet =
    propre.length === 3
      ? propre
          .split('')
          .map((c) => c + c)
          .join('')
      : propre;
  return [
    parseInt(complet.slice(0, 2), 16),
    parseInt(complet.slice(2, 4), 16),
    parseInt(complet.slice(4, 6), 16),
  ];
}

function versHex([r, v, b]: Rvb): string {
  const deux = (n: number) => Math.round(Math.max(0, Math.min(255, n))).toString(16).padStart(2, '0');
  return `#${deux(r)}${deux(v)}${deux(b)}`;
}

function luminance([r, v, b]: Rvb): number {
  const lineaire = (c: number) => {
    const n = c / 255;
    return n <= 0.03928 ? n / 12.92 : Math.pow((n + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * lineaire(r) + 0.7152 * lineaire(v) + 0.0722 * lineaire(b);
}

export function contraste(a: string, b: string): number {
  const la = luminance(versRvb(a));
  const lb = luminance(versRvb(b));
  return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
}

/** Melange une couleur vers le blanc ou vers le noir, par pas de 4 %. */
function melanger(couleur: Rvb, vers: Rvb, part: number): Rvb {
  return [
    couleur[0] + (vers[0] - couleur[0]) * part,
    couleur[1] + (vers[1] - couleur[1]) * part,
    couleur[2] + (vers[2] - couleur[2]) * part,
  ];
}

/**
 * Rapproche une couleur du blanc jusqu'a atteindre le contraste demande sur
 * un fond sombre. Renvoie la couleur d'origine si elle convient deja.
 */
export function lisibleSurSombre(hex: string, fond = '#0e0f12', cible = 4.5): string {
  let couleur = versRvb(hex);
  for (let i = 0; i <= 25; i++) {
    const candidat = versHex(couleur);
    if (contraste(candidat, fond) >= cible) return candidat;
    couleur = melanger(versRvb(hex), [255, 255, 255], (i + 1) * 0.04);
  }
  return '#e8e8ea';
}

/** Meme principe, vers le noir, pour un fond clair. */
export function lisibleSurClair(hex: string, fond = '#ffffff', cible = 4.5): string {
  let couleur = versRvb(hex);
  for (let i = 0; i <= 25; i++) {
    const candidat = versHex(couleur);
    if (contraste(candidat, fond) >= cible) return candidat;
    couleur = melanger(versRvb(hex), [0, 0, 0], (i + 1) * 0.04);
  }
  return '#18181b';
}
