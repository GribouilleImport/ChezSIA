<!-- BREADCRUMB START -->
[🏠](README.md)
<!-- BREADCRUMB END -->

# 🤖 Instructions pour les Agents & Développeurs

Bienvenue sur le projet **ChezSIA**. Ce document sert de "Vérité Terrain" et de guide pour tous les agents et développeurs travaillant sur ce dépôt.

<!-- TOC START -->
## 📖 Table des Matières

- [📖 Table des Matières](#table-des-matières)
- [📜 Règles d'Or](#règles-dor)
- [🛠 Architecture & Outils](#architecture-outils)
  - [🔄 Script de Maintenance (`.dev/scripts/update_docs/script.py`)](#script-de-maintenance-devscriptsupdate_docsscriptpy)
- [📖 Table des Matières](#table-des-matières)
- [🎯 Titre H2 avec Emoji](#titre-h2-avec-emoji)
  - [🔹 Titre H3 avec Emoji](#titre-h3-avec-emoji)
<!-- TOC END -->

## 📜 Règles d'Or

1.  **Pas de Régression de Contenu** : Ne jamais supprimer ou altérer le contenu informatif des fichiers existants lors des restructurations.
2.  **Documentation Vivante** : Tout ajout de connaissance doit être immédiatement répercuté dans la documentation.
3.  **Reflexes Visuels** : Utiliser des Emojis pour chaque titre (H1, H2, H3) afin de faciliter la lecture rapide (scan visuel).
4.  **Liens Explicites** : Tout lien vers un dossier doit pointer explicitement vers son `README.md` (ex: `[Dossier] (./dossier/README.md)` et non `[Dossier] (./dossier/)`).

## 🛠 Architecture & Outils

Le dossier `.dev/scripts/` contient les outils de maintenance du projet.

### 🔄 Script de Maintenance (`.dev/scripts/update_docs/script.py`)
> **Note** : Ce script est désormais une simple interface pour exécuter le **Documentation Agent** (`.dev/agents/documentation/`).

Il doit être exécuté régulièrement (ou est lancé automatiquement par l'Orchestrateur).
Il assure que :
*   Tous les fichiers MD ont un fil d'ariane.
*   Tous les fichiers MD ont une table des matières.
*   Le dossier `.dev` est également maintenu.

**Fonctionnalités :**
1.  **Fil d'Ariane (Breadcrumbs)** : Génère automatiquement la navigation en haut de fichier (entre `<!-- BREADCRUMB START -->
[🏠](README.md)
<!-- BREADCRUMB END -->

# 🔭 Titre H1 avec Emoji

Introduction/Contexte...

<!-- TOC START -->
## 📖 Table des Matières

- [📖 Table des Matières](#table-des-matières)
- [📜 Règles d'Or](#règles-dor)
- [🛠 Architecture & Outils](#architecture-outils)
  - [🔄 Script de Maintenance (`.dev/scripts/update_docs/script.py`)](#script-de-maintenance-devscriptsupdate_docsscriptpy)
- [📖 Table des Matières](#table-des-matières)
- [🎯 Titre H2 avec Emoji](#titre-h2-avec-emoji)
  - [🔹 Titre H3 avec Emoji](#titre-h3-avec-emoji)
<!-- TOC END -->

## 🎯 Titre H2 avec Emoji
...
### 🔹 Titre H3 avec Emoji
...
```

### Emojis Suggérés

*    **Finance** : 💰, 💳, 🧾, 📊
*    **Analyse** : 🧠, 🔬, 📈, 📉
*    **Navigation** : 🏠, 📂, 📄, 🔙
*    **Technique** : ⚙️, 🛠, 💻, 🤖
*    **Humain** : 👥, 🤝, 👤

## 📂 Organisation des Dossiers

*   `/` (Racine) : Documents de synthèse et points d'entrée (`README.md`, `AGENTS.md`, Prévisionnels).
*   `/SOURCE` : Documents bruts, transcriptions, recherches datées (ex: `YYYYMMDD_sujet.md`).
*   `/.dev` : Outils techniques et configuration "meta" du projet.

---
*Dernière mise à jour par l'Agent IA.*
