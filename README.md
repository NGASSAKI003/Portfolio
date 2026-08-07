# Portfolio NGASSAKI-NDZA Anaclet Julien

**[ngassaki.pages.dev](https://ngassaki.pages.dev)**

Site personnel. Astro 5, TypeScript strict, Tailwind 4, hébergé sur Cloudflare Pages.

Objectif de référencement, en deux phrases :

1. Quand on cherche un de mes projets, on doit me trouver, moi.
2. Quand on cherche mon nom, on doit trouver mes projets.

Tout le reste en découle. Huit pages, chacune avec sa propre adresse. Du HTML
servi déjà rempli, jamais rempli après coup par un script. Et un graphe
d'entités JSON-LD dont les identifiants ne changent jamais, pour que les moteurs
fusionnent ces pages en une seule personne reliée à ses travaux.

Ce qui part réellement sur le réseau, mesuré sur le site construit et non
estimé : **7,6 Ko de JavaScript**, **11,5 Ko de CSS**, **65 Ko de polices**, le
tout compressé.

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

| Script                                | Rôle                                                      |
| ------------------------------------- | --------------------------------------------------------- |
| `scripts/generer-identite.py`         | Vectorise le logo, génère favicons et icônes installables  |
| `scripts/generer-sigle.py`            | Vectorise le sigle NNAJ de la barre haute                  |
| `scripts/generer-visuels.py`          | Images de partage des pages                                |
| `scripts/generer-couverture-logo.py`  | Couverture de la fiche du portfolio                        |
| `scripts/generer-couverture-demotech.py` | Couverture de la fiche Y-MENI                           |
| `scripts/vectoriser-logo-one-zone.py` | Reconstruit une source nette du logo One Zone              |
| `scripts/preparer-captures.py`        | Captures Android de One Zone et couverture du projet       |
| `scripts/preparer-certificat.py`      | Redresse le certificat DemoTech                            |
| `scripts/sous-ensembler-polices.py`   | Réduit les polices au jeu latin français                   |

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

## Mettre le site à jour, une fois qu'il est en ligne

Le premier déploiement est décrit dans [A-FAIRE.md](A-FAIRE.md). Après, tout
passe par Git : Cloudflare surveille le dépôt et redéploie à chaque poussée sur
la branche principale.

### La routine, à chaque changement

```bash
npm run check
```

```bash
npm run build
```

```bash
npm run preview
```

Ouvre `localhost:4322`, vérifie ce que tu viens de changer. Si c'est bon :

```bash
git add -A
```

```bash
git commit -m "Décris ce qui change et pourquoi"
```

```bash
git push
```

Cloudflare démarre le déploiement dans les secondes qui suivent et le termine en
deux à trois minutes. Tu peux suivre l'avancement dans **Workers & Pages**, ton
projet, onglet **Deployments**.

> `npm run build` avant de pousser n'est pas une formalité. Cloudflare exécute la
> même commande sur ses serveurs : si elle échoue chez toi, elle échouera chez
> eux, et le site restera sur l'ancienne version sans que rien ne te prévienne.

### Quand tu changes une image source

Les scripts de `scripts/` ne tournent pas au build. Si tu remplaces un logo, une
capture ou un certificat dans `_sources/`, relance le script concerné avant de
construire, sinon le site continuera d'afficher l'ancienne version.

```bash
python scripts/preparer-captures.py
```

```bash
python scripts/generer-visuels.py
```

### Si tu ne vois pas ton changement

Dans cet ordre, en s'arrêtant dès que ça marche.

1. Recharge en forçant : **Ctrl+Maj+R**.
2. Purge les caches locaux, puis reconstruis.

```bash
rm -rf .astro node_modules/.astro dist
```

3. Purge le cache de Cloudflare : tableau de bord, ton projet, **Settings**,
   section **Caching**, bouton **Purge everything**.

### Revenir en arrière

Un déploiement raté se répare sans toucher au code. Dans **Deployments**, ouvre
le dernier déploiement qui fonctionnait et clique sur **Rollback to this
deployment**. Le site revient à cet état en quelques secondes. Corrige ensuite
tranquillement, et repousse.

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
7,6 Ko compressés, dont l'essentiel sert les transitions de page.

**Aucune police depuis un service tiers.** Les trois familles sont
auto-hébergées, réduites au jeu latin français et à l'intervalle de graisses
réellement employé, soit 65 Ko au lieu de 132. Sur une connexion moyenne, une
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

**`sizes` décrit la grille de la page, jamais le composant.** Une même carte de
projet occupe toute la largeur sur l'accueil et une colonne sur deux dans
`/projets`. La largeur annoncée au navigateur était écrite dans le composant :
il recevait donc une image de 640 pixels pour une boîte de 1150 et l'agrandissait
de 80 pour cent. Elle est devenue une propriété que chaque page renseigne selon
sa propre grille, avec la pleine largeur en repli, parce qu'une image trop grande
reste nette et qu'une image trop petite ne le sera jamais.

Un second piège se cache derrière le premier. En `object-fit: cover`, une boîte
plus haute en proportion que l'image oblige le navigateur à agrandir celle-ci
pour couvrir la hauteur : la largeur réellement peinte dépasse alors celle de la
boîte, jusqu'à 845 pixels pour une boîte de 440 sur la grande carte. Or le choix
de la variante ne regarde que la largeur annoncée, jamais le recadrage. La
vérification qui compte n'est donc pas « la variante couvre-t-elle la boîte »
mais « couvre-t-elle la largeur peinte, à chaque densité de pixels ».

**Une icône installée ne porte jamais son propre arrondi.** Android, iOS et
Windows appliquent chacun la leur. Les icônes livrées sont donc des carrés
pleins ; seule la favicon garde ses coins arrondis, puisqu'un onglet n'applique
aucune forme. Et `convert("RGB")` de Pillow remplace la transparence par du
noir sans prévenir, ce qui donnait des angles noirs à l'installation :
l'aplatissement se fait désormais sur la couleur de la tuile.

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

**Trois familles, une par fonction.** Instrument Serif en titrage, Inter en
texte courant, JetBrains Mono pour les étiquettes et les métadonnées. Geist et
Geist Mono ont été essayées puis écartées : la hiérarchie y reposait sur la
seule graisse, ce qui manquait de caractère en titrage. Pour en essayer une
autre, un seul jeton est à changer : `--font-titre` dans `src/styles/global.css`.

**Le sigle de la barre haute est un tracé, pas une image.** Les quatre
initiales sont vectorisées par `scripts/generer-sigle.py`, qui contrôle son
travail en rastérisant le résultat et en le comparant au dessin d'origine
pixel par pixel. Le tracé pèse 1 Ko, hérite de `currentColor`, et bascule donc
avec le thème sans qu'on livre deux fichiers. Le nom complet reste porté par
le `aria-label` du lien, le titre de la page et le graphe JSON-LD.

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
#   P o r t f o l i o  
 