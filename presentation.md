# Présentation — Dark Quest 2D

**Trophées NSI 2025-2026 — Dossier n°2108**  
Lycée Français Alioune Blondin Beye — Luanda, Angola

\---

## 1\. Résumé

RouteRush est un jeu éducatif de simulation de routage réseau, entièrement développé en HTML5/JavaScript pur. Le joueur incarne un paquet de données qui doit traverser un réseau informatique en construisant manuellement un chemin entre un nœud source et un nœud destination. Le jeu couvre les protocoles de routage au programme de Terminale NSI : RIP (métrique en sauts), OSPF (métrique inversement proportionnelle à la bande passante) et BGP (routage inter-AS). Il comprend 4 niveaux de difficulté croissante avec des pannes dynamiques, un compte à rebours, un système de vies et un moteur graphique canvas animé.
\---

## 2\. Description détaillée

RouteRush est développé en un fichier HTML5 autonome, sans dépendance externe ni framework. Le joueur sélectionne un niveau depuis l'écran d'accueil, puis construit son chemin de routage en cliquant sur les nœuds du réseau affiché dans un canvas. L'interface est divisée en une zone graphique principale (canvas) et un panneau latéral de contrôle avec plusieurs onglets (Mission, Routage, Chemin construit, Journal).

### Structure des fichiers

|Fichier|Rôle|
|-|-|
RouteRush.html (avec le code) cela permet a visualiser le jeux mais aussi le code 

### Mécanique de jeu

 •	4 niveaux de difficulté : Initiation (RIP), Modéré (OSPF WAN), Difficile (OSPF + BGP inter-AS), Boss (Opérateur Télécom — 16 nœuds, 3 AS)

•	Chaque niveau contient 2 à 3 missions à enchaîner avec des contraintes différentes

•	Pannes statiques (nœuds déjà hors ligne au départ) et pannes dynamiques (nœuds qui tombent après n secondes)

•	Système TTL : chaque saut décrémente le compteur — un chemin trop long détruit le paquet
•	Passerelle obligatoire : certaines missions imposent d'utiliser une gateway spécifique pour entrer dans un autre sous-réseau

•	3 tentatives par niveau, score cumulé, overlay de réussite/échec avec analyse du chemin optimal.

•	Personnage Baymax animé (flottant, avec ombre dynamique) qui suit le dernier nœud sélectionné du chemin


\---

## 3\. Nature du code et répartition du travail

Le projet est une création originale. L'ensemble de la logique de jeu, de l'interface et des niveaux a été conçu et écrit par l'équipe à partir de zéro, sans utilisation de template ou de tutoriel.

###Mohamed Ali

•	Conception de l'architecture générale du projet (fichier HTML unique, séparation CSS/JS, organisation des données en JSON)

•	Implémentation de l'algorithme de Dijkstra générique supportant trois modes de coût : RIP (coût = 1 par saut), OSPF (coût = 100 / bande_passante) et BGP (coût = AS-path length)

•	Développement du système de validation de chemin : vérification de la connexité, des nœuds hors ligne, des liens BGP bloqués, du TTL et de la passerelle requise

•	Conception et implémentation des 4 niveaux (définition des nœuds, arêtes, missions et contraintes dans le tableau LEVELS[])

### Sakaiza Rajaofetra et Tiany Cerca

•	Développement du moteur de rendu canvas : boucle d'animation avec requestAnimationFrame, dessin des zones AS colorées, des routes de fond, des arêtes (avec animation de flux de données et couleur selon le protocole), des nœuds (source, routeur, destination) avec leurs étiquettes IP

•	Animation du personnage Baymax : flottement sinusoïdal, ombre portée dynamique, déplacement en fonction du dernier nœud sélectionné dans le chemin

•	Système de particules : effets d'explosion de couleur lors de pannes dynamiques (burst())

•	Gestion des événements souris sur le canvas : survol avec tooltip détaillé, clic pour construction du chemin


### Sidi Ebade

•	Développement du panneau latéral avec ses quatre onglets : Mission, Routage, Chemin construit, Journal

•	Implémentation du HUD (score, vies en points lumineux, chronomètre avec barre de progression colorée, badge protocole)

•	Système de pannes dynamiques : minuteur par setInterval, déclenchement à T+N secondes, invalidation automatique du chemin en cours, recalcul du chemin optimal, entrée dans le journal

•	Overlay de résultat (succès / échec / victoire) avec statistiques, conseil d'optimisation et boutons d'action

•	Interface de sélection de niveau avec cartes de difficulté et système de progression (niveaux verrouillés jusqu'à déblocage)


\---

## 4\. Utilisation de l'Intelligence Artificielle

Conformément aux règles du concours, l'équipe déclare avec transparence tous les usages de l'IA dans ce projet.

Workik (Anthropic) — Aide au débogage (~30 % du code)
•	Identification et correction d'un bug de recalcul du chemin optimal (G.optResult) lors de pannes dynamiques : le chemin n'était pas recalculé correctement si le nœud tombant était déjà dans la liste downNodes

•	Aide à la correction du calcul du coût OSPF dans l'algorithme de Dijkstra (arrondis flottants)

•	Aide au débogage de la gestion du resize du canvas lors du changement d'onglet ou de la transition entre les écrans

•	Explication du fonctionnement de requestAnimationFrame et de la boucle d'animation pour synchroniser rendu et logique


**IA conversationnelle — Reformulation pédagogique (\~9 % du contenu)**

*Les descriptions des protocoles RIP, OSPF et BGP affichées dans le guide d'aide ont été vérifiées et reformulées pour garantir leur exactitude technique. Les formulations originales ont été entièrement rédigées par l'équipe.

### Bilan global

|Élément|Équipe|IA|
|-|-|-|
|Code JavaScript / HTML / CSS / Equipe = 75 % original / IA = 30 % débogage assisté
Niveaux et données réseau (LEVELS[]) /	Equipe = 100 % original	/ IA = 0 %
Contenu pédagogique (guide protocoles)	Equipe = 95 % original / IA = 9 % reformulation
Visuels / rendu canvas	/ Equipe = 100 % original / IA = 0 %
Scénario / game design	/ Equipe = 80 % original / IA = 20 %

L'équipe certifie que le code, le scénario et le contenu pédagogique constituent une production originale, et que tous les usages de l'IA ont été limités, réfléchis et transparents.

