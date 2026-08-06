/**
 * Source unique de verite pour l'identite du site.
 *
 * Le jour ou tu achetes un nom de domaine (ngassaki.dev par exemple),
 * une seule ligne change ici : SITE_URL.
 * Les canoniques, le sitemap, le JSON-LD, les images OpenGraph et le robots.txt
 * suivent automatiquement.
 */

export const SITE_URL = 'https://ngassaki.pages.dev';

export const SITE = {
  url: SITE_URL,
  lang: 'fr',
  locale: 'fr_FR',
  name: 'NGASSAKI-NDZA Anaclet Julien',
  shortName: 'NGASSAKI-NDZA',
  initials: 'NNAJ',
  jobTitle: 'Développeur full stack',
  tagline: 'Développeur full stack, web, mobile et IA',
  description:
    "Développeur full stack à Pointe-Noire, Congo. Créateur de One Zone, la place de marché nationale du Congo. React, Next.js, Astro, Node.js, Flutter, Supabase.",
  email: 'ngassakindzaa@gmail.com',
  phone: '+242064505633',
  phoneDisplay: '+242 06 450 56 33',
  city: 'Pointe-Noire',
  region: 'Pointe-Noire',
  country: 'CG',
  countryName: 'République du Congo',
  geo: { lat: -4.7692, lng: 11.8636 },
};

/**
 * Adresse LinkedIn.
 *
 * A REMPLIR. Marche a suivre pour obtenir l'adresse exacte :
 *   1. Ouvrir LinkedIn, cliquer sur sa photo en haut, puis « Voir le profil ».
 *   2. Copier l'adresse affichee dans la barre du navigateur.
 *      Elle ressemble a https://www.linkedin.com/in/anaclet-julien-ngassaki-ndza
 *   3. Retirer tout ce qui suit un point d'interrogation, s'il y en a un.
 *   4. Coller ici, entre les guillemets.
 *
 * Tant que cette chaine est vide, LinkedIn n'apparait ni dans le pied de page,
 * ni dans le `sameAs` du schema Person. C'est voulu : une adresse approximative
 * invalide tout le bloc, et avec lui le lien entre le nom et l'identite en ligne.
 */
export const LINKEDIN = 'https://www.linkedin.com/in/anaclet-julien-ngassaki-ndza';

/**
 * Code de verification Google Search Console.
 *
 * A REMPLIR une seule fois. Dans Search Console, choisir la methode
 * « Balise HTML ». Google affiche une ligne du type :
 *   <meta name="google-site-verification" content="AbCdEf123..." />
 * Ne coller ici que la valeur de `content`, sans les guillemets ni la balise.
 * Laisser vide tant que ce n'est pas fait : aucune balise ne sera emise.
 */
export const VERIFICATION_GOOGLE = '';

/**
 * Profils externes. Ces URL alimentent le champ `sameAs` du schema Person,
 * qui est le mecanisme par lequel Google relie ce nom a cette identite.
 * Une seule URL invalide fait tomber tout le bloc : ne mettre ici que des
 * adresses exactes, verifiees, sans espace.
 */
export const PROFILES = [
  { name: 'GitHub', url: 'https://github.com/NGASSAKI003', handle: '@NGASSAKI003' },
  { name: 'One Zone', url: 'https://onezonecg.pages.dev', handle: 'onezonecg.pages.dev' },
  ...(LINKEDIN
    ? [{ name: 'LinkedIn', url: LINKEDIN, handle: 'Profil professionnel' }]
    : []),
];
