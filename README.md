# Portfolio NGASSAKI-NDZA Anaclet Julien

Site personnel. Astro 5, TypeScript strict, Tailwind 4, hébergé sur Cloudflare Pages.

Objectif de référencement, en deux phrases :

1. Quand on cherche un de mes projets, on doit me trouver, moi.
2. Quand on cherche mon nom, on doit trouver mes projets.

## Démarrer

```bash
npm install
```

```bash
npm run dev
```

| Commande          | Effet                                              |
| ----------------- | -------------------------------------------------- |
| `npm run dev`     | Serveur de développement sur `localhost:4321`       |
| `npm run build`   | Génère le site statique dans `dist/`                |
| `npm run preview` | Sert `dist/` comme en production                    |
| `npm run check`   | Vérification TypeScript et Astro                    |

## Ajouter un projet

Un projet est **un seul fichier**. Créer `src/content/projets/mon-projet.md` :

```yaml
---
titre: Mon projet
sousTitre: Une phrase qui dit ce que c'est
resume: >-
  Entre 70 et 185 caractères. Sert de méta description et de texte de partage.
role: Ce que j'ai fait dessus
annee: 2026
statut: en-ligne # en-ligne | en-cours | prime | archive
vedette: true # apparaît sur la page d'accueil
ordre: 1 # ordre d'affichage, croissant
pile: [Astro, TypeScript]
domaines: [Web]
lienDemo: 'https://exemple.com'
couverture: ../../assets/couvertures/mon-projet.png
couvertureAlt: Description de l'image, pour les lecteurs d'écran
typeSchema: WebApplication # WebApplication | SoftwareApplication | CreativeWork
chiffres:
  - valeur: '5'
    libelle: quelque chose de vérifiable
---
Le corps de l'étude de cas, en Markdown.
```

Le schéma est validé au build : une erreur de frontmatter arrête la compilation
plutôt que de produire une page incomplète. Le fichier génère automatiquement sa
page, sa balise canonique, son entrée de sitemap, son fil d'Ariane et son bloc de
données structurées.

Pour l'image de partage, lancer ensuite :

```bash
python scripts/generer-visuels.py
```

## Changer de nom de domaine

Une seule ligne, dans `site.config.mjs` :

```js
export const SITE_URL = 'https://ngassaki.dev';
```

Les canoniques, le sitemap, le `robots.txt`, les données structurées et les
images de partage suivent automatiquement.

## Scripts de génération

Ils ne tournent pas au build : ils produisent des fichiers versionnés, à relancer
seulement quand leur source change.

```bash
pip install vtracer pillow svglib rlPyCairo fonttools brotli
```

| Script                             | Rôle                                                        |
| ---------------------------------- | ----------------------------------------------------------- |
| `scripts/generer-identite.py`      | Vectorise le logo, génère favicons et icônes PWA             |
| `scripts/generer-visuels.py`       | Couvertures de projet et images de partage                    |
| `scripts/sous-ensembler-polices.py`| Réduit les polices au jeu latin français                     |

## Déployer sur Cloudflare Pages

1. Pousser le dépôt sur GitHub.
2. Dans le tableau de bord Cloudflare : **Workers & Pages**, puis **Create**,
   puis **Pages**, puis **Connect to Git**.
3. Renseigner :
   - Commande de build : `npm run build`
   - Répertoire de sortie : `dist`
   - Version de Node : `22` (variable d'environnement `NODE_VERSION`)
4. Déployer. Le fichier `public/_headers` applique le cache et les en-têtes de
   sécurité automatiquement.

Chaque `git push` redéploie.

## Ce que le code ne peut pas faire

Un site techniquement irréprochable qui ne reçoit aucun lien entrant reste
invisible. Sept procédures détaillées, étape par étape, sont réunies dans
[A-FAIRE.md](A-FAIRE.md) : adresse LinkedIn, dépôts GitHub, déploiement, lien
depuis One Zone, Google Search Console, Bing, vérification des cartes de partage.

Trois valeurs sont à remplir dans `site.config.mjs` au fil de ces étapes :
`LINKEDIN`, `VERIFICATION_GOOGLE` et, si l'adresse de déploiement diffère,
`SITE_URL`. Tant qu'une valeur est vide, la fonctionnalité correspondante reste
simplement absente, sans rien casser.

## Décisions structurantes

**Astro plutôt que Next.js.** Le site est à 95 % du contenu. Astro produit du
HTML au build et n'envoie aucun runtime de framework. Total du JavaScript livré :
environ 5,7 Ko compressés, presque entièrement dus aux transitions de page.

**Aucune police depuis un service tiers.** Les trois familles sont
auto-hébergées, réduites au jeu latin français et à l'intervalle de graisses
réellement employé, soit 67 Ko au lieu de 132. Sur une connexion moyenne, une
connexion réseau supplémentaire coûte plus cher que les octets qu'elle économise.

**Révélation à la lecture en CSS pur.** `animation-timeline: view()`, sans
JavaScript. Aucun observateur à initialiser, donc aucun scénario où un script
muet laisse la page vide. Là où la fonctionnalité n'existe pas, le contenu
s'affiche directement.

**Compatibilité des trois moteurs, vérifiée et non supposée.** Deux corrections
issues de cet audit méritent d'être connues avant de toucher au CSS.

`overflow-x: hidden` oblige le navigateur à calculer `overflow-y: auto`, ce qui
transforme l'élément en conteneur de défilement et casse `position: sticky` sous
WebKit. `html` et `body` utilisent donc `overflow-x: clip`, qui coupe le
débordement sans créer de conteneur, avec `hidden` en repli pour Safari
antérieur à la version 16.

L'état de la barre haute est piloté par un script et non par
`animation-timeline: scroll()`, que Gecko ne livre pas encore. Sans cela, la
barre serait restée transparente par dessus le contenu chez tous les visiteurs
Firefox.

Ce qui dégrade proprement, en revanche, reste en CSS : la révélation à la lecture
et la rotation de la lueur sont enveloppées dans `@supports`, et leur absence
laisse simplement le contenu affiché et la lueur immobile.

**Contrastes calculés, pas estimés.** Chaque jeton de couleur porte son rapport
mesuré en commentaire dans `src/styles/global.css`. Les huit pages passent le
niveau AA dans les deux thèmes, à toutes les largeurs testées.

**Navigation mobile en barre inférieure.** Sur un téléphone tenu à une main, le
haut de l'écran est hors de portée du pouce, et un menu caché derrière trois
traits demande de savoir que ces trois traits sont un menu. Quatre destinations
visibles en permanence, avec une icône et un mot, ne demandent rien à apprendre.
La barre haute reprend la main à partir de 768 pixels.

**Captures réelles plutôt qu'illustrations.** Les écrans de One Zone sont de
vraies captures Android, préparées par `scripts/preparer-captures.py`, qui
compose aussi la couverture à trois téléphones. Le certificat DemoTech est
redressé par `scripts/preparer-certificat.py`. Une capture prouve que la chose
existe, une illustration ne prouve rien.

**Deux familles de caractères, pas trois.** Geist et Geist Mono, sous-ensemblées
au latin français et à l'intervalle de graisses employé, soit 34 Ko au lieu de
132 au départ. La hiérarchie vient de la graisse, de la taille et de
l'interlettrage. Pour essayer une autre police de titrage, un seul jeton est à
changer : `--font-titre` dans `src/styles/global.css`.

**Aucun voyant d'état, aucune pilule de statut.** Les statuts sont du texte dans
la ligne de métadonnées, avec des formules de métier : « En production » dit
quelque chose à un recruteur, « En ligne » ne dit rien.

**Logos de technologies via `simple-icons`.** Tracés officiels en un seul chemin,
inlinés au build : aucune requête supplémentaire pour vingt-cinq logos. Les
couleurs de marque sont faites pour un fond blanc, `src/lib/couleurs.ts` les
éclaircit ou les assombrit jusqu'à atteindre 4,5:1 sur le thème concerné.

**Constellation interactive dans le pied de page.** Un nuage de points dessine le
logo. Il fuit le doigt puis revient par ressort, un appui envoie une onde, et au
repos l'ensemble respire lentement. Le tracé n'est pas dupliqué : le script lit
le SVG déjà présent dans la page. Coût réel : 2 Ko compressés.

Une version enrichie a existé, avec liens de proximité entre points, parallaxe de
profondeur et éclosion depuis le centre. Elle a été écartée : trop chargée pour
une signature de pied de page. Le code en garde la trace dans l'historique Git.

Trois garde-fous y sont posés, et ils valent pour tout le site :

- Le nuage est **tracé une fois avant toute animation**. Si `requestAnimationFrame`
  ne produit jamais d'image, on voit le logo immobile, jamais une zone vide.
- Les particules **naissent à leur place**, pas dispersées, pour la même raison.
- La visibilité est calculée dans la boucle à partir de la position réelle,
  **sans IntersectionObserver** : cette API ne se déclenche pas dans certains
  contextes de rendu, et une décoration ne doit jamais dépendre d'un rappel qui
  peut ne pas venir.
