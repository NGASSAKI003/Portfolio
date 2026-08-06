---
titre: Ce portfolio
sousTitre: Refonte d'un site invisible, et pourquoi il l'était
resume: >-
  Reconstruction complète de ce site après un échec de référencement. Diagnostic,
  graphe d'entités JSON-LD, une page réelle par projet, zéro JavaScript par défaut.
role: Conception, développement et référencement
annee: 2026
periode: '2026'
statut: en-ligne
vedette: false
ordre: 3
pile:
  - Astro
  - TypeScript
  - Tailwind CSS
  - JSON-LD
  - Cloudflare Pages
domaines:
  - Référencement naturel
  - Performance web
  - Accessibilité
  - Architecture de contenu
couverture: ../../assets/couvertures/portfolio-logo.png
couvertureAlt: >-
  Le logo de NGASSAKI-NDZA, un entrelacs bleu en dégradé, sur fond sombre
typeSchema: CreativeWork
chiffres:
  - valeur: '0'
    libelle: mention de mes projets sur l'ancien site
  - valeur: '1'
    libelle: seule adresse dans l'ancien sitemap
  - valeur: '0 Ko'
    libelle: de JavaScript de framework envoyé
---

## Le constat

Mon précédent portfolio était en ligne depuis des mois et n'apparaissait nulle
part. Ni sur mon nom, ni sur mes projets.

L'explication qui vient d'abord à l'esprit, c'est le rendu par JavaScript : une
page vide que le navigateur remplit après coup, et que le moteur de recherche ne
voit pas. Dans mon cas, c'était faux. Le site était du HTML statique, servi déjà
rempli, sans balise bloquante et avec un fichier robots.txt permissif. Techniquement,
rien n'empêchait son indexation.

Le vrai problème était plus bête, et plus grave.

**Le site ne parlait jamais de mes projets.** Le mot One Zone n'y apparaissait pas
une seule fois. La section « projets réalisés » contenait quatre cartes
génériques, sans nom, sans lien et sans capture. Le sitemap déclarait une seule
adresse. Il n'y avait donc rien à faire remonter sur une recherche de projet, et
rien qui reliait mon nom à ce que j'avais construit.

S'y ajoutaient des défauts de finition qui coûtaient cher : des données
structurées invalidées par des adresses mal formées, une image de partage absente
qui faisait afficher une carte vide à chaque envoi sur WhatsApp, et une icône de
site qui répondait en erreur.

## Ce que j'ai refait

Deux objectifs, formulés simplement.

1. Quand on cherche un de mes projets, on doit me trouver, moi.
2. Quand on cherche mon nom, on doit trouver mes projets.

Ces deux phrases décrivent en réalité un seul mécanisme : un graphe d'entités.

### Une page réelle par projet

Chaque projet vit dans un fichier Markdown validé au build par un schéma. Ce
fichier produit une vraie adresse, sa balise canonique, son entrée de sitemap,
son image de partage et son bloc de données structurées. Ajouter un projet est un
fichier, pas un chantier, et il devient impossible d'oublier une métadonnée.

### Un graphe d'entités relié dans les deux sens

Une entité `Person` porte un identifiant stable, réutilisé à l'identique sur
toutes les pages du site. Chaque projet se déclare comme l'œuvre de cette entité.
La page de liste énumère les projets. Le moteur de recherche fusionne ces
déclarations d'une page à l'autre et reconstruit une seule personne, reliée à un
ensemble de travaux.

C'est exactement ce chaînage qui manquait à l'ancienne version, et aucune quantité
de mots clés n'aurait pu le remplacer.

### Zéro JavaScript de framework

Le site est généré en HTML au moment du build. Aucun runtime de framework n'est
envoyé au navigateur pour afficher du texte. Les rares zones interactives sont
chargées séparément, et le contenu reste lisible si le script ne s'exécute pas.

Les polices sont auto-hébergées plutôt que chargées depuis un service tiers. Sur
une connexion moyenne, une connexion réseau supplémentaire coûte plus cher que
les quelques kilo-octets qu'elle économise.

### L'accessibilité traitée comme une contrainte, pas comme une option

Tous les rapports de contraste sont calculés et notés dans la feuille de style.
La navigation au clavier couvre l'intégralité du site, avec un lien d'évitement et
un anneau de focus qui n'est jamais supprimé. Les animations disparaissent
entièrement si le système le demande.

## Ce que ça ne règle pas

Un site techniquement irréprochable qui ne reçoit aucun lien entrant reste
invisible. La partie du travail qui compte le plus ne se code pas : elle consiste
à être cité depuis des endroits qui existent déjà, et à déclarer le site aux
moteurs plutôt qu'à attendre qu'ils le trouvent.

C'est la leçon la plus utile que m'a donnée cet échec.
