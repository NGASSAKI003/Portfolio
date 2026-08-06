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
  après avoir neutralisé les transitions.

## Valeurs à remplir

Dans `site.config.mjs` : `VERIFICATION_GOOGLE` reste vide, voir l'étape 5 de
[A-FAIRE.md](A-FAIRE.md). `SITE_URL` devra être corrigé si l'adresse de
déploiement diffère de celle qui y figure.
