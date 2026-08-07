# Portfolio NGASSAKI-NDZA

Site personnel, en production. Astro 5, TypeScript strict, Tailwind 4, contenu
en Markdown validé par Zod, déployé sur Cloudflare Pages.

Le [README.md](README.md) explique l'architecture et les décisions. Ce fichier ci
ne retient que ce qu'il faut savoir avant de toucher au code.

## Commandes

```bash
npm run check && npm run build && npm run preview
```

Les scripts de `scripts/` **ne tournent pas au build**. Si une image de
`_sources/` change, relancer le script concerné avant de construire, sinon le
site continue d'afficher l'ancienne version.

## Ce qui n'est pas négociable

- **Aucun tiret long ni demi-cadratin**, ni dans le contenu, ni dans les
  commentaires, ni dans les messages de commit. Pas de traits horizontaux
  décoratifs non plus.
- **Rien de ce qui compte ne dépend du JavaScript pour s'afficher.** Le contenu
  est visible d'abord, l'animation s'ajoute ensuite. Cette règle a déjà évité
  trois pages blanches sur ce projet.
- **Contrastes mesurés, pas estimés.** Chaque jeton de couleur porte son rapport
  en commentaire dans `src/styles/global.css`. Les huit pages passent AA dans les
  deux thèmes, à toutes les largeurs.
- **Cibles tactiles à 24 pixels minimum**, exigence WCAG 2.2.
- **Le graphe d'entités JSON-LD est le cœur du projet.** Les identifiants de
  `src/lib/jsonld.ts` ne doivent jamais changer : c'est par eux que Google
  fusionne les pages en une seule personne reliée à ses travaux.

## Pièges déjà rencontrés, ne pas les refaire

- **`overflow-x: hidden` force `overflow-y: auto`** et crée un conteneur de
  défilement, ce qui casse `position: sticky` sous WebKit. Le site utilise
  `overflow-x: clip`, avec `hidden` en repli.
- **Gecko traite `-webkit-mask` comme un alias de `mask`.** Cette propriété
  raccourcie réinitialise `mask-composite`. Dans `.lueur::before`, les deux
  raccourcies sont déclarées **avant** les deux longues. Ne pas réorganiser.
- **Lightning CSS développe les raccourcies en propriétés longues.** Chercher
  `mask:` dans le CSS livré ne prouve rien. Vérifier la valeur calculée de
  `maskComposite`, qui doit contenir `exclude`.
- **`animation-timeline` n'existe pas dans Gecko.** Réservé aux agréments dont
  l'absence ne se remarque pas. Tout ce qui est structurant passe par un script.
- Le panneau de vérification ne compose pas les images : ni transitions, ni
  `requestAnimationFrame`, ni `IntersectionObserver` ne s'y exécutent. Mesurer
  après avoir neutralisé les transitions. Il fausse aussi `naturalWidth`, qui y
  renvoie la largeur de mise en page : pour connaître la définition réelle d'une
  variante, la recharger dans un `new Image()`.
- **Un style à portée de composant n'atteint pas la racine d'un composant
  enfant.** Astro marque les éléments de son propre gabarit, pas ceux que rend
  un enfant : une classe passée en propriété ne suffit donc pas. `.marque__logo`
  est resté sans effet pendant des semaines, le logo retombant en silence sur le
  `height: 1em` de `Logo.astro`. Écrire `.parent :global(.enfant)`, comme
  `.carte__visuel :global(img)` dans `CarteProjet`.
- **`sizes` décrit la grille de la page hôte, jamais le composant.** La même
  carte est pleine largeur sur l'accueil et sur une colonne sur deux dans
  `/projets`. Une valeur codée en dur dans `CarteProjet` faisait servir une
  image de 640 pixels pour une boîte de 1150, agrandie 1,80 fois. Les points de
  rupture annoncés doivent en plus correspondre exactement à ceux de la grille.
  La largeur annoncée est désormais une propriété, avec la pleine largeur en
  repli, parce qu'une image trop grande reste nette et l'inverse non.
- **Une source déjà floue ne se rattrape pas en aval.** Mesurer la proportion de
  pixels à alpha intermédiaire : un tracé propre en a 3 à 6 %, le logo One Zone
  fourni en avait 23,5 %, donc il avait déjà été agrandi avant d'arriver. Quand
  aucun meilleur fichier n'existe, `vectoriser-logo-one-zone.py` sépare les deux
  choses que porte une image : la **forme** vient du tracé vectoriel, donc elle
  est franche à toute taille, la **couleur** vient d'un agrandissement lisse,
  parce qu'un dégradé n'a aucun détail fin à perdre. Bords ramenés à 1,6 % pour
  98,1 % de fidélité de forme. Ne pas seuiller ailleurs qu'à 128 : le contour se
  déplacerait et la marque changerait de graisse.
- **Une icône installée ne porte jamais son propre arrondi.** Android, iOS et
  Windows appliquent chacun leur forme. Et `convert("RGB")` de Pillow aplatit la
  transparence **sur du noir** : c'est ce qui donnait des angles noirs aux
  icônes. Aplatir explicitement sur la couleur voulue.

## Valeurs à remplir

Dans `site.config.mjs` : `VERIFICATION_GOOGLE` reste vide, en attente de la
vérification Google Search Console. `SITE_URL` devra être corrigé si l'adresse
de déploiement diffère de celle qui y figure.

Les guides `A-FAIRE.md` et `LINKEDIN.md` existent sur le disque mais sont hors
du dépôt : ce sont des marches à suivre personnelles, sans rapport avec le code.
Ne pas les y remettre.
