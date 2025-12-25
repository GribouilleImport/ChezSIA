<!-- BREADCRUMB START -->
[🏠](../../../README.md) > [📂 .dev](../../README.md) > [🤖 Système Multi-Agents ChezSIA](../README.md) > [🤖 Agent Documentation (Auto-Update)](README.md)
<!-- BREADCRUMB END -->

# 🤖 Agent Documentation (Auto-Update)

Cet agent a pour mission de maintenir la structure standard des fichiers Markdown du projet.

<!-- TOC START -->
## 📖 Table des Matières

- [📖 Table des Matières](#table-des-matières)
- [Fonctionnalités](#fonctionnalités)
- [Comportement](#comportement)
<!-- TOC END -->

## Fonctionnalités
- **Fil d'Ariane (Breadcrumbs)** : Injecte et met à jour automatiquement les liens de navigation en haut de page.
- **Table des Matières (TOC)** : Génère une TOC basée sur les titres H2 et H3 du document.
- **Support Global** : Scanne l'intégralité du projet, y compris le dossier `.dev`.

## Comportement
Il ignore uniquement les dossiers techniques (`.git`, `__pycache__`).
Il ne modifie le fichier que si le contenu généré est différent de l'existant (préservation des timestamps).
