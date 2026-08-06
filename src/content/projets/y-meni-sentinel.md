---
titre: Y-MENI Sentinel
sousTitre: Sécurité minière en temps réel, du capteur à la voix
resume: >-
  Système intelligent de sécurité, de récolte et de gestion en mine. Capteurs
  ESP32, tableau de bord installable, assistant vocal fonctionnant hors ligne.
role: Développement web, API et assistant vocal
annee: 2026
periode: 'DemoTech 9, 2026'
statut: finaliste
vedette: true
ordre: 2
pile:
  - ESP32
  - Objets connectés
  - PWA
  - API REST
  - Reconnaissance vocale
  - Synthèse vocale
domaines:
  - Objets connectés
  - Temps réel
  - Intelligence artificielle appliquée
  - Sécurité industrielle
couverture: ../../assets/couvertures/demotech-9.png
couvertureAlt: >-
  L'affiche de DemoTech 9 sur le thème MineTech, à côté du certificat décerné à
  NGASSAKI-NDZA Anaclet Julien pour sa participation à la phase finale
preuve:
  image: ../../assets/certificats/demotech-9-mockup.jpg
  alt: >-
    Certificat DemoTech 9 décerné à NGASSAKI-NDZA Anaclet Julien pour sa
    participation à la phase finale, thème MineTech, signé par le président
    directeur général de l'ISIPA
  legende: >-
    Le certificat, tel quel et lisible. Il mentionne « participation remarquable
    à la phase finale », l'équipe OBS GRID et l'intitulé complet du projet.
typeSchema: SoftwareApplication
categorieApplication: BusinessApplication
systemeExploitation: 'Web, Android, iOS'
chiffres:
  - valeur: '3'
    libelle: familles de capteurs
    source: 'gaz, température, présence'
  - valeur: 'Finale'
    libelle: DemoTech 9
    source: 'thème MineTech, ISIPA, mai 2026'
  - valeur: 'Hors ligne'
    libelle: assistant vocal fonctionnel
---

## Le problème

Dans une galerie de mine, l'information de sécurité arrive souvent trop tard, et
elle arrive sous une forme que personne ne peut consulter sur le terrain. Un
opérateur qui porte des gants, dans le bruit, avec un casque et une lampe, ne
sort pas un téléphone pour lire un tableau.

La question n'était donc pas seulement de mesurer, mais de faire parvenir la
mesure à quelqu'un qui a les mains occupées, dans un endroit où le réseau est
mauvais ou absent.

## Ce que nous avons construit

Y-MENI est un système de bout en bout, réalisé en équipe au sein d'OBS GRID, sous
les couleurs de mon école, l'ESTAM, également désignée Institut Congo
Technologie. Son intitulé complet, celui déposé au concours, est « Y MENI,
système intelligent assurant la sécurité, la récolte et la gestion ».

Des cartes ESP32 équipées de capteurs de gaz, de température et de présence
relèvent l'état du site en continu et le transmettent à une API. Un tableau de
bord web installable affiche l'état en temps réel, avec l'historique et les
alertes.

Par dessus, un assistant vocal permet d'interroger le système et d'être alerté à
la voix, sans écran et sans les mains.

## Les choix techniques, et pourquoi

### Un tableau de bord web installable plutôt qu'une application de bureau

Le poste de supervision n'est pas toujours un poste : c'est parfois un téléphone
dans la poche d'un chef d'équipe. Une application web installable donne le même
outil sur un écran de contrôle et sur un mobile, sans double développement et
sans procédure d'installation.

### Un assistant vocal hybride, hors ligne d'abord

C'est le point le plus intéressant du projet, et celui qui a demandé le plus
d'arbitrage.

La reconnaissance et la synthèse vocales fonctionnent en mode hybride : le
traitement local prend le relais dès que la liaison est mauvaise ou absente. Une
alerte de sécurité qui dépend d'une connexion est une alerte qui manque à
l'appel précisément le jour où elle compte.

Le compromis est réel : le modèle local est moins précis que ce qu'un service
distant produirait. Sur un vocabulaire métier restreint, cette perte de précision
est largement compensée par la garantie de fonctionnement.

### Un mode démonstration assumé

Le système embarque un mode de démonstration qui rejoue des scénarios sans
matériel branché. Ce n'est pas un artifice de présentation : c'est ce qui permet
de montrer le produit à un décideur, de former quelqu'un, et de tester
l'interface sans immobiliser une installation.

## Le résultat

Le projet a atteint la phase finale de la neuvième édition de DemoTech, sur le
thème MineTech, compétition organisée par l'ISIPA et dotée de 10 000 dollars pour
le premier prix, avec Cisco et Huawei parmi les partenaires. La finale s'est
tenue le 21 mai 2026 au Silikin Village. Mon certificat porte la mention
« participation remarquable à la phase finale ».

> Je préfère l'écrire tel quel plutôt que de laisser croire à une victoire. Ce
> qui compte est ce que le système fait, et un jury a estimé qu'il méritait
> d'aller au bout.

Ce que j'en retiens tient surtout à la contrainte physique. Écrire une interface
pour quelqu'un qui a les mains prises, dans le bruit et sans réseau, oblige à
retirer beaucoup de choses. C'est un exercice qui m'a rendu plus dur avec mes
propres interfaces.
