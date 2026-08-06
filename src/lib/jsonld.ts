import { SITE, SITE_URL, PROFILES, ID, url } from './site';

type Noeud = Record<string, unknown>;

/**
 * Le graphe d'entites.
 *
 * Deux objectifs, un seul mecanisme :
 *   1. chercher un projet doit mener a l'auteur   -> chaque projet declare `author`
 *      pointant vers un @id de Person stable et identique sur tout le site ;
 *   2. chercher l'auteur doit mener aux projets   -> la page d'accueil publie les
 *      oeuvres, et /projets publie un ItemList qui les enumere.
 *
 * Les @id ne doivent jamais changer : ce sont eux que Google fusionne d'une page
 * a l'autre pour reconstruire une seule et meme entite.
 */

export function noeudPersonne(options: { image?: string; complet?: boolean } = {}): Noeud {
  const { image, complet = false } = options;

  const base: Noeud = {
    '@type': 'Person',
    '@id': ID.personne,
    name: SITE.name,
    url: SITE_URL,
  };

  if (!complet) return base;

  return {
    ...base,
    givenName: 'Anaclet Julien',
    familyName: 'NGASSAKI-NDZA',
    alternateName: ['Anaclet Julien Ngassaki-Ndza', 'Julien Ngassaki', SITE.initials],
    jobTitle: SITE.jobTitle,
    description: SITE.description,
    mainEntityOfPage: { '@id': ID.siteWeb },
    ...(image ? { image: { '@type': 'ImageObject', url: image, caption: SITE.name } } : {}),
    email: `mailto:${SITE.email}`,
    telephone: SITE.phone,
    address: {
      '@type': 'PostalAddress',
      addressLocality: SITE.city,
      addressRegion: SITE.region,
      addressCountry: SITE.country,
    },
    homeLocation: {
      '@type': 'Place',
      name: `${SITE.city}, ${SITE.countryName}`,
      geo: {
        '@type': 'GeoCoordinates',
        latitude: SITE.geo.lat,
        longitude: SITE.geo.lng,
      },
    },
    alumniOf: {
      '@type': 'CollegeOrUniversity',
      name: 'ESTAM',
      description: 'École supérieure de technologie et de management, Pointe-Noire',
      address: {
        '@type': 'PostalAddress',
        addressLocality: 'Pointe-Noire',
        addressCountry: 'CG',
      },
    },
    knowsLanguage: [
      { '@type': 'Language', name: 'Français', alternateName: 'fr' },
      { '@type': 'Language', name: 'Anglais', alternateName: 'en' },
    ],
    knowsAbout: [
      'Développement web',
      'Développement mobile',
      'TypeScript',
      'React',
      'Next.js',
      'Astro',
      'Node.js',
      'Express',
      'Flutter',
      'Supabase',
      'PostgreSQL',
      'MongoDB',
      'API REST',
      'Applications web progressives',
      'Référencement naturel',
      "Intégration de l'intelligence artificielle",
    ],
    // Seules des URL exactes et verifiees entrent ici : une URL malformee fait
    // tomber tout le bloc, et avec lui le lien entre le nom et l'identite en ligne.
    sameAs: PROFILES.map((p) => p.url),
  };
}

export function noeudSiteWeb(): Noeud {
  return {
    '@type': 'WebSite',
    '@id': ID.siteWeb,
    url: SITE_URL,
    name: `${SITE.name}, ${SITE.jobTitle}`,
    description: SITE.description,
    inLanguage: SITE.lang,
    publisher: { '@id': ID.personne },
    author: { '@id': ID.personne },
    copyrightHolder: { '@id': ID.personne },
  };
}

export function noeudPage(options: {
  chemin: string;
  titre: string;
  description: string;
  type?: 'WebPage' | 'ProfilePage' | 'CollectionPage' | 'ContactPage' | 'AboutPage';
  image?: string;
  dateModification?: string;
}): Noeud {
  const { chemin, titre, description, type = 'WebPage', image, dateModification } = options;
  return {
    '@type': type,
    '@id': `${url(chemin)}#page`,
    url: url(chemin),
    name: titre,
    description,
    isPartOf: { '@id': ID.siteWeb },
    inLanguage: SITE.lang,
    ...(type === 'ProfilePage' ? { mainEntity: { '@id': ID.personne } } : {}),
    ...(image ? { primaryImageOfPage: { '@type': 'ImageObject', url: image } } : {}),
    ...(dateModification ? { dateModified: dateModification } : {}),
  };
}

export interface DonneesProjet {
  slug: string;
  titre: string;
  sousTitre: string;
  resume: string;
  annee: number;
  pile: string[];
  domaines: string[];
  lienDemo?: string;
  lienCode?: string;
  typeSchema: 'SoftwareApplication' | 'WebApplication' | 'CreativeWork';
  categorieApplication?: string;
  systemeExploitation?: string;
  datePublication?: string;
  dateModification?: string;
  image?: string;
  gratuit?: boolean;
}

/** Identifiant stable d'un projet, reutilise a l'identique sur toutes les pages. */
export function idProjet(slug: string): string {
  return `${url(`/projets/${slug}`)}#projet`;
}

export function noeudProjet(projet: DonneesProjet, complet = true): Noeud {
  const adresse = url(`/projets/${projet.slug}`);

  const base: Noeud = {
    '@type': projet.typeSchema,
    '@id': idProjet(projet.slug),
    name: projet.titre,
    url: adresse,
    // C'est cette ligne qui dit a Google : ce projet est de cette personne.
    author: { '@id': ID.personne },
  };

  // Forme courte : publiee sur les pages qui citent le projet sans le detailler.
  // Elle porte tout de meme la description, car c'est elle qui permet de relier
  // une recherche sur le nom du projet a la personne qui l'a fait.
  if (!complet) return { ...base, description: projet.resume };

  const liensOfficiels = [projet.lienDemo, projet.lienCode].filter(Boolean) as string[];

  return {
    ...base,
    headline: projet.sousTitre,
    description: projet.resume,
    creator: { '@id': ID.personne },
    mainEntityOfPage: { '@id': `${adresse}#page` },
    isPartOf: { '@id': ID.siteWeb },
    inLanguage: SITE.lang,
    keywords: [...projet.pile, ...projet.domaines].join(', '),
    ...(projet.image ? { image: projet.image, screenshot: projet.image } : {}),
    ...(projet.datePublication ? { datePublished: projet.datePublication } : {}),
    ...(projet.dateModification ? { dateModified: projet.dateModification } : {}),
    ...(liensOfficiels.length ? { sameAs: liensOfficiels } : {}),
    ...(projet.typeSchema !== 'CreativeWork'
      ? {
          applicationCategory: projet.categorieApplication ?? 'BusinessApplication',
          operatingSystem: projet.systemeExploitation ?? 'Web',
          ...(projet.gratuit
            ? {
                offers: {
                  '@type': 'Offer',
                  price: '0',
                  priceCurrency: 'XAF',
                  availability: 'https://schema.org/InStock',
                },
              }
            : {}),
        }
      : {}),
  };
}

export function noeudFilAriane(etapes: { nom: string; chemin: string }[]): Noeud {
  return {
    '@type': 'BreadcrumbList',
    '@id': `${url(etapes[etapes.length - 1]!.chemin)}#fil`,
    itemListElement: etapes.map((etape, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: etape.nom,
      item: url(etape.chemin),
    })),
  };
}

export function noeudListeProjets(projets: { slug: string; titre: string }[]): Noeud {
  return {
    '@type': 'ItemList',
    '@id': `${url('/projets')}#liste`,
    name: `Projets de ${SITE.name}`,
    numberOfItems: projets.length,
    itemListOrder: 'https://schema.org/ItemListOrderDescending',
    itemListElement: projets.map((projet, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: projet.titre,
      url: url(`/projets/${projet.slug}`),
    })),
  };
}

/** Assemble le graphe final injecte dans la page. */
export function graphe(noeuds: Noeud[]): string {
  return JSON.stringify(
    { '@context': 'https://schema.org', '@graph': noeuds },
    null,
    0,
  );
}
