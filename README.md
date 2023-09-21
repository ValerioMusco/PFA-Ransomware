# PFA-Ransomware (Non fini)

## Description du projet :

Dans l'optique du cours d'intégration des risques (HELMo), nous avions reçu comme projet de créer un ransomware avec toute une infrastructure réseaux derrière.
Il nous fallait créer.
- Un serveur de clés
  
    Ce serveur gérait la base de données et était connecté à une console de contrôle qui nous permettais de voir combien de personnes ont été infectées ainsi que donner l'ordre au ransomware de déchiffrer les infos de l'utilisateur si ce dernier avait procédé au paiement.
- Un serveur frontal

    Ce serveur gérait la communication entre les clients infecté et le serveur de clés. Il se connectait periodiquement à certain ransomware pour avoir les infos a renvoyer pour l'enregistrement DB.
- La console de contrôle

  Elle était l'application qu'on lançait. Elle se connectais au serveur de clés et nous permettais de faire plusieurs chose. Voir les infos de la DB (User infectés, combien de fichiers on été cryptés, etc..), permettre de rendre l'accès aux fichiers d'un utilisateur
- Le ransomware

  Assez basique c'etait le malware qui scannait l'ordinateur de la personne infectée, générais les hash, chiffrais les données et renvoyais tout au serveur frontal. Le chiffrement ne commençait qu'une fois le serveur frontal ait pris connaissance du nouveau infecté.

Toutes les communications entre chaques noeuds devait être sérialisée et chiffrée afin de ne rien exposer.
J'avais utilisé la libraire pickle pour sérialiser les envois de données. 
Le chiffrement des données était fait avec la méthode d'échange DiffieHellman.
La gestion de la base de données était faites avec SQLite
Il fallait gérer toutes les connections TCP et utiliser des threads pour pouvoir avoir plusieurs connection en même temps.
Et je devais gérer les configurations des serveurs sur des fichiers JSON et ne pas les laisser dans les codes sources.

## Raison de l'abandon du projet :

Je n'ai pas su finir le projet car nous étions censé travailler en groupe dessus. Sauf qu'un des membres de notre groupe à arrêté les cours et le 3ème ne savais pas programmer en python. Je me suis retrouvé seul à faire la plupart des fonctionnalité du projet.
J'ai aussi été bloqué par les innondations et n'avais plus accès à un ordinateur et ne pouvait donc plus travailler sur le projet. 

## Compétences acquises lors de ce projet :

Utilisation des protocoles TCP en languages de programmation

Utilisation de librairies externe et recherche de doc

Chiffrement des données
