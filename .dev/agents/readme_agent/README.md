<!-- BREADCRUMB START -->
[🏠](../../../README.md) > [📂 .dev](../../README.md) > [📂 agents](../README.md) > [🤖 Agent Documentaliste (ReadmeAgent)](README.md)
<!-- BREADCRUMB END -->

# 🤖 Agent Documentaliste (ReadmeAgent)

Cet agent a pour mission de s'assurer qu'aucun dossier du projet ne reste "muet".
Il parcourt récursivement toute l'arborescence du projet et, s'il trouve un dossier sans `README.md`, il en génère un automatiquement.

<!-- TOC START -->
## 📖 Table des Matières

- [📖 Table des Matières](#table-des-matières)
- [Fonctionnalités](#fonctionnalités)
- [Utilisation](#utilisation)
<!-- TOC END -->

## Fonctionnalités
- **Scan Récursif** : Ignore intelligemment les dossiers techniques (`.git`, `__pycache__`).
- **Génération Automatique** : Crée un tableau listant les fichiers et sous-dossiers présents.
- **Message d'Avertissement** : Ajoute une note indiquant que le fichier est auto-généré et doit être enrichi.

## Utilisation
Cet agent est généralement appelé par l'Orchestrateur via le script principal, mais peut être utilisé de manière autonome ou importé.
