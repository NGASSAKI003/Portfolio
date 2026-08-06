---
titre: One Zone
sousTitre: La place de marché nationale du Congo
resume: >-
  Place de marché nationale du Congo. Application web installable, pensée pour
  les connexions faibles, avec messagerie, réservations et billetterie intégrées.
role: Fondateur et développeur full stack
annee: 2026
periode: 'Depuis juin 2026'
statut: en-ligne
vedette: true
ordre: 1
pile:
  - React 19
  - TypeScript
  - Vite
  - Tailwind CSS
  - Supabase
  - PostgreSQL
  - Cloudflare R2
  - OneSignal
  - PWA
domaines:
  - Place de marché
  - Application web progressive
  - Temps réel
  - Paiement mobile
lienDemo: 'https://onezonecg.pages.dev'
couverture: ../../assets/captures/one-zone-cle.png
couvertureAlt: >-
  Le logo de One Zone, un monogramme 1Z en dégradé violet et cyan, à côté de deux
  écrans de téléphone montrant le catalogue et le formulaire de publication
galerie:
  - image: ../../assets/captures/one-zone-accueil.png
    alt: >-
      Le catalogue de One Zone sur téléphone, avec recherche, filtres par
      catégorie et par ville
    legende: >-
      Le catalogue. Recherche, catégories, villes, offres et demandes, et la
      barre de navigation sous le pouce.
  - image: ../../assets/captures/one-zone-publier.png
    alt: Le formulaire de publication d'une annonce sur One Zone
    legende: >-
      Publier une annonce : offre ou demande, type de produit, prix, médias.
      Tout tient sur un écran, sans champ inutile.
  - image: ../../assets/captures/one-zone-messagerie.png
    alt: La liste des conversations dans la messagerie de One Zone
    legende: >-
      La messagerie intégrée, avec texte, vocal et accusé de lecture. Plus besoin
      de sortir sur WhatsApp pour conclure une vente.
  - image: ../../assets/captures/one-zone-badge-confiance.png
    alt: L'écran du badge de confiance, avec sa progression et ses conditions
    legende: >-
      Le badge de confiance : il se gagne par les ventes vérifiées et les avis,
      il ne s'achète pas, et il se perd si l'on relâche.
  - image: ../../assets/captures/one-zone-langues.png
    alt: >-
      Les paramètres de One Zone montrant les cinq langues disponibles, dont le
      lingala et le kituba
    legende: >-
      Les cinq langues, dans les paramètres. Français, lingala, kituba, anglais
      et chinois, au même niveau.
  - image: ../../assets/captures/one-zone-equipe.png
    alt: L'écran de gestion d'équipe et d'organisation commerciale sur One Zone
    legende: >-
      Les organisations : plusieurs personnes portent une même boutique, chacune
      avec son compte et ses droits, sans mot de passe partagé.
  - image: ../../assets/captures/one-zone-portefeuille.png
    alt: Le portefeuille de One Zone, avec le solde et la vérification par QR
    legende: >-
      Le portefeuille et la vérification de transaction par QR. La structure est
      posée, elle attend l'enregistrement administratif de la société.
  - image: ../../assets/captures/one-zone-one-view.png
    alt: L'écran de création d'une One View sur One Zone
    legende: >-
      One View : un format court qui disparaît après vingt-quatre heures, mais
      relié aux annonces et à la messagerie.
typeSchema: WebApplication
categorieApplication: BusinessApplication
systemeExploitation: 'Web, Android, iOS'
datePublication: '2026-06-01'
chiffres:
  - valeur: '5'
    libelle: langues servies
    source: 'français, anglais, chinois, lingala, kituba'
  - valeur: '0 %'
    libelle: de commission sur les ventes
  - valeur: '4'
    libelle: modules métier
    source: 'réservations, transport, billetterie, demandes urgentes'
  - valeur: '3'
    libelle: rôles par organisation
    source: 'fondateur, associé, employé'
---

## Le problème

Au Congo, vendre en ligne veut dire poster sur son statut WhatsApp et espérer que
ses contacts regardent. Ou publier dans un groupe Facebook saturé, où l'annonce
est enterrée le jour même.

Le commerce est bien là, vivant et créatif. Ce qui manque, c'est l'outil. Un
statut disparaît en vingt-quatre heures, et tout est à refaire. Un vendeur ne
touche que les gens qu'il connaît déjà. Rien ne distingue un vendeur sérieux d'un
inconnu, donc l'acheteur hésite. Et du côté des hôtels ou des agences de voyage,
tout se gère encore par appels et cahier, ce qui produit exactement ce qu'on
imagine : des doubles réservations.

Ce n'est pas un problème de talent, c'est un problème d'outil.

## Ce que j'ai construit

One Zone est une place de marché nationale. Une application web qui s'installe
sur le téléphone comme une application classique, mais qui ne pèse presque rien
et continue de s'afficher quand la connexion faiblit.

On y publie une annonce en trois gestes. On y trouve ce qui se vend près de chez
soi. On y réserve une chambre, une salle, une place de bus. On y discute
directement avec le vendeur, sans sortir de l'application.

Au delà de la petite annonce, quatre modules transforment l'outil en instrument
de travail :

- **Réservations** à la nuit, à l'heure, à la semaine ou au mois, avec un
  calendrier des disponibilités et une garantie contre la double réservation
  posée au niveau de la base de données, pas dans le code applicatif.
- **Transport et billetterie de voyage** : une agence publie ses départs, vend
  ses places et valide l'embarquement en scannant un QR. Les lignes régulières se
  répètent d'elles mêmes, et un départ peut être annulé sans toucher au reste.
- **Billetterie d'événements** avec catégories, quotas et QR à usage unique
  contrôlé à l'entrée.
- **Demandes urgentes**, diffusées en priorité aux personnes proches. Cette
  fonction est née d'une histoire vraie.

S'y ajoutent les **organisations** : un hôtel ou un commerce se tient rarement
seul. Plusieurs personnes portent un même compte boutique en gardant chacune le
sien, avec trois rôles distincts et aucun mot de passe partagé. Le partage des
revenus est visible par toute l'équipe, et la première personne qui ouvre une
conversation client la prend en charge, pour que personne ne réponde deux fois.

## Les choix techniques, et pourquoi

### Une application web installable plutôt qu'une application native

C'est le choix structurant, et il vient du terrain.

Une application du store demande un téléchargement de plusieurs dizaines de
mégaoctets, de la place sur un téléphone qui en manque, et un forfait data pour
chaque mise à jour. Une application web installable ne demande rien de tout ça :
elle s'ajoute à l'écran d'accueil depuis le navigateur, elle se met à jour sans
que l'utilisateur ait à agir, et elle continue de s'ouvrir hors réseau grâce à
une copie locale de la dernière visite.

Le compromis existe et je l'assume : je perds l'accès à certaines interfaces
natives, et la présence sur les stores. En échange, je supprime la barrière qui
aurait bloqué la moitié de mes utilisateurs au premier écran.

### Supabase, pour tenir une infrastructure à une seule paire de mains

Le produit a besoin d'une base relationnelle, d'authentification, de stockage de
fichiers et de temps réel. Assembler et opérer ces quatre briques séparément
aurait consommé le temps que je devais mettre dans le produit.

Supabase les réunit autour d'un PostgreSQL standard, ce qui compte pour deux
raisons. D'abord la sécurité : l'isolation des données entre utilisateurs et
entre organisations est déclarée dans la base, au plus près de la donnée, et non
laissée à la vigilance du code client. Ensuite la réversibilité : c'est du
PostgreSQL, donc rien n'est verrouillé le jour où il faudra partir.

### Le stockage des médias sur Cloudflare R2

Une place de marché, c'est des photos et des vidéos. Chez la plupart des
hébergeurs, ce n'est pas le stockage qui coûte, c'est la sortie de données. R2 ne
facture pas cette sortie, ce qui rend le modèle tenable avant même le premier
franc de revenu. Les photos sont par ailleurs allégées avant l'envoi, pour que
publier une annonce ne coûte pas un forfait au vendeur.

### Cinq langues, dont deux langues nationales

Français, anglais, chinois, lingala et kituba. Le lingala et le kituba ne sont
pas une case à cocher : ce sont les langues dans lesquelles une bonne partie du
commerce se fait réellement, et les traduire correctement demande de connaître
les mots du marché, pas ceux du dictionnaire.

## Où ça en est

Le produit est en ligne depuis juin 2026, il fonctionne, et il évolue chaque
semaine.

La partie économique, elle, est construite mais suspendue à une formalité
administrative : aucun opérateur de paiement mobile n'ouvre de compte marchand
sans enregistrement RCCM. Le portefeuille, les transactions vérifiées par QR et
l'historique sont en place et attendent ce feu vert. Publier restera gratuit dans
tous les cas.

> Sur le marché visé : environ 5,9 millions d'habitants, dont près de 70 % ont
> moins de trente ans. Ces ordres de grandeur viennent de sources publiques
> (Banque mondiale, DataReportal) et servent à situer le contexte, pas à fonder
> une projection.

## Ce que ce projet m'a appris

Construire pour son propre pays impose des contraintes qu'aucun tutoriel ne
mentionne. Le poids d'une page n'est pas une note sur un tableau de bord, c'est
de l'argent que le visiteur dépense. Une fonctionnalité qui suppose une connexion
stable est une fonctionnalité qui ne marche pas. Et un badge de confiance qui
s'achète ne vaut rien, alors qu'un badge qui se gagne par les avis et les ventes
vérifiées change le comportement des deux côtés de la transaction.

C'est aussi le projet qui m'a fait passer du développeur qui exécute une
spécification à celui qui doit décider, arbitrer et vivre avec ses arbitrages.
