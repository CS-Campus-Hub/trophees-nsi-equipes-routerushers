# Dark Quest 2D

**Trophées NSI 2025-2026 — Dossier n°2108**  
Lycée Français Alioune Blondin Beye — Luanda, Angola

## Présentation

RouteRush est un jeu éducatif de simulation de routage réseau développé en HTML5/JavaScript pur. Le joueur incarne un paquet de données qui doit traverser un réseau informatique en construisant manuellement un chemin entre une source et une destination. Il aborde les protocoles de routage au programme de Terminale NSI — RIP, OSPF et BGP — à travers 4 niveaux de difficulté croissante, avec des pannes dynamiques, un compte à rebours et un moteur graphique canvas animé.

## Équipe

|Membre|Classe|Contributions|

[Mohamed Ali]Terminale NSIArchitecture du projet, algorithme de Dijkstra, définition des niveaux (LEVELS[])

[Sakaiza Rajaofetra et Tiany Cerca]Terminale NSIMoteur de rendu canvas, animations, personnage Baymax, effets de particules

[Sidi Ebade]Terminale NSIPanneau latéral, HUD, pannes dynamiques, overlays, sélection de niveaux

## Installation

open RouteRush.html

## Structure du projet

```
RouteRush.html     → Fichier unique contenant HTML, CSS et JavaScript
README.md          → Présentation du projet
docs/              → Dossier technique PDF
```

## Fonctionnalités

4 niveaux de difficulté : Initiation (RIP), Modéré (OSPF WAN), Difficile (BGP inter-AS), Boss (Opérateur Télécom)

3 protocoles de routage simulés : RIP (métrique en sauts), OSPF (coût = 100 / bande passante), BGP (AS-path, liens bloqués)

Pannes statiques et pannes dynamiques déclenchées en cours de partie

Système TTL : un chemin trop long détruit le paquet

Passerelles obligatoires selon les missions

Algorithme de Dijkstra intégré pour valider et comparer les chemins

Personnage Baymax animé suivant le chemin construit

Journal d'événements horodaté, table de routage interactive, analyse lien par lien

3 tentatives par niveau avec score cumulé

## Technologies

HTML5
CSS3
JavaScript (Canvas API, sans framework ni dépendance externe)
