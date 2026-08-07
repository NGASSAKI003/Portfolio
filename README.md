# Portfolio

Mon site personnel, en ligne sur [ngassaki.pages.dev](https://ngassaki.pages.dev).

Je l'ai construit avec une idée fixe. Quand quelqu'un cherche un de mes projets,
il doit me trouver, moi. Et quand quelqu'un cherche mon nom, il doit trouver mes
projets. Tout le reste en découle : chaque projet a sa page et son adresse
propres au lieu d'être un onglet dans une page unique, le HTML part du serveur
déjà rempli, et les pages sont reliées entre elles par un graphe JSON-LD dont
les identifiants ne bougent jamais, pour que les moteurs comprennent qu'il
s'agit d'une seule personne et de ses travaux.

Astro 5, TypeScript strict, Tailwind 4, contenu en Markdown validé par Zod,
hébergé sur Cloudflare Pages.

Le site envoie 7,6 Ko de JavaScript, 11,5 Ko de CSS et 65 Ko de polices, une
fois compressés. Ce sont des chiffres relevés sur le site construit, pas des
estimations.

## Faire tourner le projet

```bash
npm install
```

```bash
npm run dev
```

Le serveur de développement écoute sur le port 4321. `npm run build` produit le
site statique dans `dist/`, `npm run preview` le sert comme en production, et
`npm run check` passe la vérification TypeScript et Astro.

Je lance les trois avant chaque mise en ligne. Cloudflare exécute exactement la
même commande de build sur ses serveurs : si elle échoue chez moi, elle échouera
chez eux, et le site restera sur l'ancienne version sans que rien ne prévienne.

## Ajouter un projet

Un projet tient dans un seul fichier, déposé dans `src/content/projets/`. Son
frontmatter est validé au build, donc une faute arrête la compilation au lieu de
produire une page incomplète.

```yaml
---
titre: Mon projet
sousTitre: Une phrase qui dit ce que c'est
resume: >-
  Entre 70 et 185 caractères. Sert de méta description et de texte de partage.
role: Ce que j'ai fait dessus
annee: 2026
statut: en-ligne
vedette: true
ordre: 1
pile: [Astro, TypeScript]
domaines: [Web]
lienDemo: 'https://exemple.com'
couverture: ../../assets/couvertures/mon-projet.png
couvertureAlt: Description de l'image, pour les lecteurs d'écran
typeSchema: WebApplication
chiffres:
  - valeur: '5'
    libelle: quelque chose de vérifiable
---
Le corps de l'étude de cas, en Markdown.
```

Ce fichier suffit. Sa page, sa balise canonique, son entrée de sitemap, son fil
d'Ariane et son bloc de données structurées en sont déduits.

Pour changer l'adresse du site, une seule ligne à toucher, `SITE_URL` dans
`site.config.mjs`. Les canoniques, le sitemap, le `robots.txt`, les données
structurées et les images de partage suivent.

## Les images

Les scripts Python de `scripts/` ne tournent pas au build. Ils écrivent des
fichiers versionnés, et je les relance seulement quand une source change dans
`_sources/`. Si j'oublie, le site continue d'afficher l'ancienne version sans
rien signaler.

```bash
pip install vtracer pillow svglib rlPyCairo fonttools brotli
```

`generer-identite.py` vectorise mon logo et en tire les favicons et les icônes
installables, `generer-sigle.py` fait le même travail pour le sigle de la barre
haute. `preparer-captures.py` nettoie les captures Android de One Zone et
compose la couverture du projet, `preparer-certificat.py` redresse le certificat
DemoTech, `generer-couverture-demotech.py` et `generer-couverture-logo.py`
composent les deux autres couvertures. `generer-visuels.py` produit les images
de partage et `sous-ensembler-polices.py` réduit les polices au jeu latin
français.

Deux scripts existent pour une raison particulière. Le logo de One Zone m'est
parvenu en 397 pixels de large et déjà adouci : `vectoriser-logo-one-zone.py` en
reconstruit une source nette, `exporter-logo-one-zone-svg.py` en tire un vrai
fichier vectoriel.

## Ce que j'ai appris en le construisant

### Astro plutôt que Next.js

Le site est à 95 % du contenu. Astro produit du HTML au build et n'envoie aucun
runtime de framework, ce qui explique les 7,6 Ko de JavaScript, dont l'essentiel
sert les transitions de page.

Les polices sont auto-hébergées et réduites au jeu latin français et aux
graisses réellement employées, 65 Ko au lieu de 132. Sur une connexion moyenne,
ouvrir une connexion réseau de plus coûte plus cher que les octets qu'on croit
économiser en la déportant.

### Rien de ce qui compte ne dépend du JavaScript

Le contenu s'affiche d'abord, l'animation s'ajoute ensuite. La révélation à la
lecture est en CSS pur, sans observateur à initialiser, donc sans scénario où un
script muet laisse une page vide. Là où la fonctionnalité n'existe pas, le
contenu s'affiche directement.

Cette règle m'a évité trois pages blanches sur ce projet. Elle vaut aussi pour
la constellation du pied de page : le nuage de points est tracé une fois avant
toute animation, et les particules naissent à leur place plutôt que dispersées.
Si `requestAnimationFrame` ne produit jamais d'image, on voit le logo immobile,
jamais une zone vide.

### Les trois moteurs de rendu, vérifiés et non supposés

`overflow-x: hidden` oblige le navigateur à calculer `overflow-y: auto`, ce qui
transforme l'élément en conteneur de défilement et casse `position: sticky` sous
WebKit. `html` et `body` utilisent donc `overflow-x: clip`, avec `hidden` en
repli pour Safari antérieur à la version 16.

Gecko traite `-webkit-mask` comme un simple alias de `mask`. Comme c'est une
propriété raccourcie, elle réinitialise `mask-composite` : le liseré lumineux
des cartes devenait un balayage de radar sous Firefox. Les deux raccourcies sont
donc déclarées avant les deux propriétés longues, jamais après.

L'état de la barre haute est piloté par un script et non par
`animation-timeline: scroll()`, que Gecko ne livre pas encore. Sans cela, la
barre serait restée transparente par dessus le contenu chez tous les visiteurs
Firefox.

### Les contrastes se mesurent

Chaque jeton de couleur porte son rapport mesuré en commentaire dans
`src/styles/global.css`. Les huit pages passent le niveau AA dans les deux
thèmes, à toutes les largeurs testées, et les cibles tactiles font au minimum
24 pixels, comme l'exige WCAG 2.2.

Une vérification qui donne un résultat trop propre est suspecte. J'ai cru un
moment que quinze contrastes échouaient par page, avant de comprendre que je
mesurais des couleurs en cours de transition.

### `sizes` décrit la page, jamais le composant

Une même carte de projet occupe toute la largeur sur l'accueil et une colonne
sur deux dans `/projets`. La largeur annoncée au navigateur était écrite dans le
composant : il recevait une image de 640 pixels pour une boîte de 1150 et
l'agrandissait de 80 pour cent. Elle est devenue une propriété que chaque page
renseigne selon sa propre grille.

Un second piège se cache derrière celui-là. En `object-fit: cover`, une boîte
plus haute en proportion que l'image oblige le navigateur à agrandir celle-ci
pour couvrir la hauteur, et la largeur réellement peinte dépasse alors celle de
la boîte, jusqu'à 845 pixels pour une boîte de 440. Or le choix de la variante
ne regarde que la largeur annoncée. La question qui compte n'est donc pas de
savoir si la variante couvre la boîte, mais si elle couvre la largeur peinte, à
chaque densité de pixels.

### Une source déjà floue ne se rattrape pas

Le logo de One Zone comptait 23,5 pour cent de pixels de bord diffus, là où un
tracé propre en compte 3 à 6 : il avait été agrandi avant même d'arriver. Quand
aucun meilleur fichier n'existe, on peut séparer les deux choses que porte une
image. La forme vient du tracé vectoriel, donc elle est franche à n'importe
quelle taille. La couleur vient d'un agrandissement lisse, parce qu'un dégradé
n'a aucun détail fin à perdre, contrairement à une arête.

### Chaque système a sa règle pour les icônes

Windows affiche le fichier tel quel, donc l'arrondi doit être dans le fichier et
l'extérieur transparent. iOS applique lui-même sa forme et ignore la
transparence, qu'il compose sur du noir : son icône doit rester un carré plein.
Android découpe la forme de son choix et ne garantit que le disque central de
80 pour cent.

Trois règles contradictoires, donc trois fichiers différents. Et `convert("RGB")`
de Pillow remplace la transparence par du noir sans prévenir, ce qui donnait des
angles noirs à l'installation.

### Le reste des partis pris

La navigation mobile est une barre inférieure. Sur un téléphone tenu à une main,
le haut de l'écran est hors de portée du pouce, et un menu caché derrière trois
traits suppose qu'on sache que ces trois traits sont un menu. Quatre
destinations visibles en permanence ne demandent rien à apprendre.

Les écrans de One Zone sont de vraies captures Android, pas des illustrations.
Une capture prouve que la chose existe.

Il n'y a aucun voyant d'état ni pilule de statut colorée. Les statuts sont du
texte dans la ligne de métadonnées, avec des formules de métier : « En
production » dit quelque chose à un recruteur, « En ligne » ne dit rien.

Les logos de technologies viennent de `simple-icons`, inlinés au build, donc
aucune requête supplémentaire pour vingt-cinq logos. Leurs couleurs de marque
sont faites pour un fond blanc, et `src/lib/couleurs.ts` les éclaircit ou les
assombrit jusqu'à atteindre 4,5 pour 1 sur le thème concerné.

Le sigle de la barre haute est un tracé et non une image. Il pèse 1 Ko, hérite
de `currentColor` et bascule donc avec le thème sans qu'on livre deux fichiers.
Mon nom complet reste porté par le `aria-label` du lien, le titre de la page et
le graphe JSON-LD.
