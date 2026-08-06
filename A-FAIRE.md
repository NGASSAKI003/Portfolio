# Ce que tu dois faire toi même

Le site est prêt. Ce qui suit ne se code pas, et pèse autant que tout le reste :
un site techniquement irréprochable que personne ne cite reste invisible.

Les sept procédures sont dans l'ordre où il faut les faire. Compte deux heures
en tout, la première fois.

---

## 1. Récupérer l'adresse exacte de ton LinkedIn

**Pourquoi c'est important.** Cette adresse va dans le champ `sameAs` de tes
données structurées. C'est ce champ qui dit à Google « la personne de ce site est
la même que celle de ce profil LinkedIn ». Sur ton ancien site, l'adresse était
mal formée, ce qui invalidait tout le bloc. Une adresse approximative est pire
que pas d'adresse du tout.

### Depuis un ordinateur

1. Va sur `linkedin.com` et connecte toi.
2. En haut à droite, clique sur ta photo, puis sur **Voir le profil**.
3. Regarde la barre d'adresse du navigateur. Elle affiche quelque chose comme :
   `https://www.linkedin.com/in/anaclet-julien-ngassaki-ndza-1a2b3c4d/`
4. Sélectionne toute cette adresse et copie la.
5. **Retire ce qui suit un point d'interrogation**, s'il y en a un. Exemple :
   `.../in/mon-nom/?originalSubdomain=cg` devient `.../in/mon-nom`
6. Retire aussi la barre oblique finale.

### Depuis l'application mobile

1. Ouvre l'application, touche ta photo en haut à gauche, puis **Voir le profil**.
2. Touche les **trois points** à droite de ton nom.
3. Choisis **Partager via**, puis **Copier le lien**.
4. Colle le quelque part pour le lire, et applique le point 5 ci-dessus.

### Pendant que tu y es : nettoie cette adresse

Si ton adresse contient une suite de chiffres et de lettres au hasard, rends la
lisible. Depuis un ordinateur, sur ta page de profil, colonne de droite, clique
sur **Modifier le profil public et l'URL**, puis sur le crayon à côté de
**Modifier votre URL personnalisée**. Mets `anaclet-julien-ngassaki-ndza` ou
`ngassaki-ndza`. Une adresse propre se retient et se cite.

### Où la coller

Ouvre `site.config.mjs` à la racine du projet, et remplis la ligne :

```js
export const LINKEDIN = 'https://www.linkedin.com/in/ton-adresse';
```

Tant que cette ligne est vide, LinkedIn n'apparaît ni dans le pied de page, ni
dans les données structurées. C'est voulu.

### Puis complète ton profil LinkedIn

Le profil entier, champ par champ, avec les textes prêts à coller, est dans
[LINKEDIN.md](LINKEDIN.md). Compte une heure, depuis un ordinateur.

---

## 2. Mettre tes projets sur GitHub

Tu me dis que ton compte est vide. C'est le point le plus coûteux de ta situation
actuelle : un recruteur technique regarde GitHub avant le portfolio, et un compte
vide dit exactement le contraire de ce que dit One Zone.

### D'abord, le plus rapide : ton profil

GitHub permet d'afficher un texte de présentation en haut de ton profil. Il
suffit de créer un dépôt qui porte **exactement ton nom d'utilisateur**.

1. Va sur `github.com`, clique sur le **+** en haut à droite, puis
   **New repository**.
2. Dans **Repository name**, tape exactement `NGASSAKI003`. GitHub affiche alors
   un encadré qui dit que c'est un dépôt spécial.
3. Coche **Public**.
4. Coche **Add a README file**.
5. Clique sur **Create repository**.
6. Sur la page du dépôt, clique sur le crayon à droite du fichier `README.md`,
   remplace le contenu par une présentation courte avec le lien vers ton
   portfolio, puis clique sur **Commit changes**.

### Ensuite, le champ site web du profil

1. Clique sur ta photo en haut à droite, puis **Your profile**.
2. Clique sur **Edit profile**, dans la colonne de gauche.
3. Remplis **Website** avec l'adresse du portfolio, et **Bio** avec ton titre.
4. Clique sur **Save**.

### Enfin, publier du code

Tu n'es pas obligé de publier One Zone en entier si tu préfères le garder fermé.
Mais publie au moins **ce portfolio**, qui est propre, documenté et qui montre ce
que tu sais faire.

Dans le dossier du portfolio, ouvre un terminal et lance ces commandes une par
une. La première ligne n'est à faire qu'une seule fois, si tu ne l'as jamais
faite sur cet ordinateur.

```bash
git config --global user.name "NGASSAKI-NDZA Anaclet Julien"
```

```bash
git config --global user.email "ngassakindzaa@gmail.com"
```

```bash
git init
```

```bash
git add .
```

```bash
git commit -m "Portfolio, premiere version"
```

Va ensuite sur GitHub créer un dépôt nommé `portfolio`, **sans** cocher
« Add a README ». GitHub affiche alors deux commandes à copier. Elles ressemblent
à ceci :

```bash
git remote add origin https://github.com/NGASSAKI003/portfolio.git
```

```bash
git branch -M main
```

```bash
git push -u origin main
```

Ensuite, sur la page du dépôt, clique sur la roue dentée à côté de **About**, en
haut à droite, et mets l'adresse du portfolio dans **Website**. Chaque dépôt qui
pointe vers ton site est un lien de plus.

> Le fichier `.gitignore` est déjà en place : `node_modules`, `dist` et le
> dossier `_sources` ne partiront pas sur GitHub.

---

## 3. Déployer le site sur Cloudflare Pages

Tu as déjà un compte, puisque One Zone y est.

1. Va sur `dash.cloudflare.com` et connecte toi.
2. Dans le menu de gauche, clique sur **Workers & Pages**.
3. Clique sur **Create**, puis sur l'onglet **Pages**, puis sur
   **Connect to Git**.
4. Autorise Cloudflare à accéder à ton compte GitHub, puis choisis le dépôt
   `portfolio`.
5. Dans l'écran de configuration, renseigne exactement :
   - **Framework preset** : `Astro`
   - **Build command** : `npm run build`
   - **Build output directory** : `dist`
6. Déplie **Environment variables** et ajoute :
   - Nom : `NODE_VERSION`, valeur : `22`
7. Clique sur **Save and Deploy**. Compte deux à trois minutes.
8. Cloudflare te donne une adresse du type `portfolio-xyz.pages.dev`.

### Important, juste après

Si l'adresse donnée n'est pas exactement `ngassaki.pages.dev`, il faut la
reporter dans le code, sinon toutes les adresses canoniques pointeront à côté.

Ouvre `site.config.mjs` et corrige la première ligne :

```js
export const SITE_URL = 'https://ton-adresse-reelle.pages.dev';
```

Puis relance un `git add .`, un `git commit -m "adresse du site"` et un
`git push`. Cloudflare redéploie tout seul.

Pour changer le nom du projet : dans Cloudflare, ouvre le projet, onglet
**Settings**, section **General**, champ **Project name**.

À partir de là, **chaque `git push` redéploie le site automatiquement**.

---

## 4. Ajouter un lien vers ton portfolio depuis One Zone

**C'est l'action la plus importante de cette liste.** C'est littéralement ce qui
crée l'association « One Zone = NGASSAKI-NDZA Anaclet Julien » aux yeux de
Google, et tu es la seule personne au monde qui puisse la faire.

Dans le code de One Zone, ajoute dans le pied de page, ou dans l'écran
« Comment ça marche », une ligne de ce genre :

```html
Conçu et développé par
<a href="https://ton-adresse.pages.dev" rel="author">
  NGASSAKI-NDZA Anaclet Julien
</a>
```

Deux détails comptent : le lien doit contenir **ton nom complet en toutes
lettres**, et il ne doit pas porter `rel="nofollow"`.

Fais la même chose dans le sens inverse si tu le souhaites : le portfolio pointe
déjà vers One Zone depuis plusieurs endroits.

---

## 5. Déclarer le site à Google

Sans cette étape, tu attends que Google trouve ton site par hasard. Avec, tu le
lui présentes.

1. Va sur `search.google.com/search-console`.
2. Clique sur **Ajouter une propriété**.
3. Choisis la case de droite, **Préfixe de l'URL**, pas celle de gauche.
4. Colle l'adresse complète du site, avec `https://` et sans barre finale.
5. Clique sur **Continuer**.
6. Dans la liste des méthodes de validation, déplie **Balise HTML**.
7. Google affiche une ligne comme :
   `<meta name="google-site-verification" content="AbCdEf123456..." />`
8. **Copie uniquement ce qui est entre les guillemets après `content=`.**
9. Ouvre `site.config.mjs` et colle cette valeur :

```js
export const VERIFICATION_GOOGLE = 'AbCdEf123456...';
```

10. Fais `git add .`, `git commit -m "verification google"`, `git push`, et
    attends que Cloudflare ait fini de redéployer.
11. Reviens sur Search Console et clique sur **Valider**.

### Puis, immédiatement après

1. Dans le menu de gauche, clique sur **Sitemaps**.
2. Dans le champ, tape `sitemap-index.xml` et clique sur **Envoyer**.
3. Dans le menu de gauche, clique sur **Inspection de l'URL** en haut, colle
   l'adresse de ta page d'accueil, puis clique sur **Demander une indexation**.
   Répète pour `/projets/one-zone`.

Compte entre trois jours et trois semaines avant de voir tes pages apparaître.
C'est normal. Reviens vérifier dans **Pages** au bout d'une semaine.

---

## 6. Déclarer le site à Bing

Cinq minutes, et ça alimente aussi les réponses de plusieurs assistants IA.

1. Va sur `bing.com/webmasters`.
2. Connecte toi, puis choisis **Importer depuis Google Search Console**. Tout se
   remplit tout seul.
3. Si l'import échoue, ajoute le site à la main et soumets le même
   `sitemap-index.xml`.

---

## 7. Vérifier que le partage fonctionne

Avant d'envoyer ton lien à qui que ce soit, vérifie ce que les gens vont voir.

1. Va sur `developers.facebook.com/tools/debug`, colle l'adresse de ton site,
   clique sur **Déboguer**. Tu dois voir la grande carte sombre avec ton nom.
   Si elle n'apparaît pas, clique sur **Extraire de nouveau les informations**.
2. Va sur `linkedin.com/post-inspector`, colle la même adresse, et vérifie.
3. Envoie toi le lien à toi même sur WhatsApp. La carte doit s'afficher.

Refais l'opération avec l'adresse d'une page projet, par exemple
`/projets/one-zone` : chaque page a sa propre carte.

---

## Après tout ça

Trois habitudes qui valent plus que n'importe quelle astuce technique.

- **Chaque nouveau projet fini est un fichier Markdown de plus.** Voir le README
  pour la marche à suivre. Un projet documenté vaut dix dépôts vides.
- **Cite ton portfolio partout** : signature d'e-mail, bio Twitter, description
  YouTube, réponses sur des forums techniques, dépôts GitHub.
- **Quand tu auras 15 EUR à mettre**, achète `ngassaki.dev`. C'est le seul levier
  de référencement que le code ne peut pas remplacer, et une ligne suffit à
  migrer.
