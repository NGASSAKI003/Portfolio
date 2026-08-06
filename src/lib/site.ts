import { SITE, SITE_URL, PROFILES, VERIFICATION_GOOGLE } from '../../site.config.mjs';

export { SITE, SITE_URL, PROFILES, VERIFICATION_GOOGLE };

/** Identifiants stables du graphe d'entites. Ils ne doivent jamais changer. */
export const ID = {
  personne: `${SITE_URL}/#personne`,
  siteWeb: `${SITE_URL}/#site`,
  organisation: `${SITE_URL}/#atelier`,
} as const;

/**
 * Construit une URL absolue, sans barre oblique finale.
 * Seule exception : la racine, qui garde la sienne, car c'est la forme
 * canonique attendue d'une page d'accueil.
 */
export function url(chemin = '/'): string {
  const propre = `/${chemin}`.replace(/\/+/g, '/').replace(/\/$/, '');
  return propre === '' ? `${SITE_URL}/` : `${SITE_URL}${propre}`;
}

export const NAVIGATION = [
  { libelle: 'Projets', href: '/projets' },
  { libelle: 'Parcours', href: '/a-propos' },
  { libelle: 'Contact', href: '/contact' },
] as const;

/**
 * Libelles de statut.
 *
 * Formules de metier plutot que d'etiquette : « En production » dit quelque
 * chose a un recruteur technique, « En ligne » ne dit rien. Ils s'affichent
 * comme du texte dans la ligne de metadonnees, jamais comme une pastille
 * coloree posee sur une image.
 */
export const LIBELLES_STATUT: Record<string, string> = {
  'en-ligne': 'En production',
  'en-cours': 'En développement',
  finaliste: 'Sélectionné en finale',
  archive: 'Archivé',
};
