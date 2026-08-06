import * as marques from 'simple-icons';

/**
 * La pile technique, groupee par famille.
 *
 * Les logos viennent de `simple-icons` : traces officiels, un seul chemin,
 * monochromes. C'est ce qui permet de les afficher en gris au repos et dans la
 * couleur exacte de la marque au survol. Le paquet est une dependance de
 * developpement : rien n'est telecharge par le visiteur, les chemins sont
 * inlines dans le HTML au build.
 *
 * `note` dit ce que j'en fais reellement. Une liste de logos sans contexte ne
 * vaut pas grand chose.
 */

export interface Technologie {
  nom: string;
  icone: { path: string; hex: string };
  note: string;
}

export interface FamilleTechnologie {
  famille: string;
  outils: Technologie[];
}

const i = marques as unknown as Record<string, { path: string; hex: string; title: string }>;

/**
 * Noms alternatifs employes ailleurs sur le site.
 * Ils pointent vers la meme entree que le nom canonique.
 */
const ALIAS: Record<string, string> = {
  'React 19': 'React',
  'Node.js / Express': 'Node.js',
  'Cloudflare Pages': 'Cloudflare',
  'Cloudflare R2': 'Cloudflare',
  'Git / GitHub': 'Git',
  SQL: 'PostgreSQL',
  'API REST': 'Node.js',
};

export const PILE: FamilleTechnologie[] = [
  {
    famille: 'Langages',
    outils: [
      { nom: 'TypeScript', icone: i.siTypescript!, note: 'Mon défaut sur tout projet web. Le typage attrape au build ce qui casserait en production.' },
      { nom: 'JavaScript', icone: i.siJavascript!, note: 'Pour les scripts courts et tout ce qui tourne dans le navigateur.' },
      { nom: 'Python', icone: i.siPython!, note: "Traitement d'images, automatisations, scripts de build. Les visuels de ce site en viennent." },
      { nom: 'PHP', icone: i.siPhp!, note: 'Via Laravel, sur des projets académiques et des sites de gestion.' },
      { nom: 'Dart', icone: i.siDart!, note: 'Le langage de Flutter, pour les applications mobiles multiplateformes.' },
    ],
  },
  {
    famille: 'Interfaces',
    outils: [
      { nom: 'React', icone: i.siReact!, note: "Toute l'interface de One Zone, en React 19, avec les hooks et le rendu concurrent." },
      { nom: 'Next.js', icone: i.siNextdotjs!, note: 'Quand il faut du rendu serveur, des routes API et une seule base de code.' },
      { nom: 'Astro', icone: i.siAstro!, note: 'Ce portfolio. Aucun JavaScript de framework envoyé, du contenu validé au build.' },
      { nom: 'Tailwind CSS', icone: i.siTailwindcss!, note: 'Pour tenir un système de design cohérent sans feuille de style qui dérive.' },
      { nom: 'Vite', icone: i.siVite!, note: "L'outil de build de One Zone. Démarrage instantané, remplacement à chaud fiable." },
    ],
  },
  {
    famille: 'Serveur et données',
    outils: [
      { nom: 'Node.js', icone: i.siNodedotjs!, note: "Les API que j'écris tournent dessus, avec Express pour le routage." },
      { nom: 'Express', icone: i.siExpress!, note: "Routes, validation à l'entrée, logique métier, connexion à la base." },
      { nom: 'Supabase', icone: i.siSupabase!, note: "Base, authentification, stockage et temps réel de One Zone, autour d'un PostgreSQL standard." },
      { nom: 'PostgreSQL', icone: i.siPostgresql!, note: "Ma base de référence. Les règles d'accès sont posées dedans, pas dans le code client." },
      { nom: 'MySQL', icone: i.siMysql!, note: "Sur les projets qui l'imposaient, notamment avec Laravel." },
      { nom: 'MongoDB', icone: i.siMongodb!, note: 'Quand le schéma bouge trop vite pour être figé tout de suite.' },
      { nom: 'SQLite', icone: i.siSqlite!, note: 'Pour le local, les prototypes et le stockage embarqué.' },
      { nom: 'Laravel', icone: i.siLaravel!, note: 'Applications de gestion côté PHP, avec Eloquent et les migrations.' },
      { nom: 'Django', icone: i.siDjango!, note: "Côté Python, quand l'administration intégrée fait gagner des semaines." },
    ],
  },
  {
    famille: 'Mobile',
    outils: [
      { nom: 'Flutter', icone: i.siFlutter!, note: 'Une base de code, deux plateformes, et une interface qui ne bavure pas.' },
      { nom: 'React Native', icone: i.siReact!, note: "Quand le projet est déjà en React et que l'équipe connaît l'écosystème." },
    ],
  },
  {
    famille: 'Livraison',
    outils: [
      { nom: 'Git', icone: i.siGit!, note: 'Historique propre, branches courtes, messages qui expliquent le pourquoi.' },
      { nom: 'GitHub', icone: i.siGithub!, note: 'Dépôts, revues et déploiement automatique à chaque poussée.' },
      { nom: 'Cloudflare', icone: i.siCloudflare!, note: "Pages pour l'hébergement, R2 pour les médias, sans frais de sortie." },
      { nom: 'Vercel', icone: i.siVercel!, note: "Déploiement des projets Next.js, avec les aperçus automatiques à chaque branche." },
      { nom: 'Netlify', icone: i.siNetlify!, note: "L'hébergeur de mon ancien portfolio. Je sais aussi d'où je viens." },
    ],
  },
];

const PAR_NOM = new Map<string, Technologie>(
  PILE.flatMap((groupe) => groupe.outils.map((outil) => [outil.nom, outil] as const)),
);

/**
 * Retrouve une technologie par son nom, alias compris.
 * Renvoie `undefined` pour tout ce qui n'a pas de logo officiel, par exemple
 * « Applications web progressives » : dans ce cas l'appelant affiche du texte.
 */
export function trouverTechnologie(nom: string): Technologie | undefined {
  return PAR_NOM.get(nom) ?? PAR_NOM.get(ALIAS[nom] ?? '');
}
