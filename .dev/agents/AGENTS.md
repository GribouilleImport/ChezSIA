<!-- BREADCRUMB START -->
[🏠](../../README.md) > [📂 .dev](../README.md) > [🤖 Agents](README.md)
<!-- BREADCRUMB END -->

# 🤖 Instructions pour les Agents & Développeurs

Bienvenue sur le projet **ChezSIA**. Ce document sert de "Vérité Terrain" et de guide pour tous les agents et développeurs travaillant sur ce dépôt.

<!-- TOC START -->
## 📖 Table des Matières

- [📖 Table des Matières](#table-des-matières)
- [📜 Règles d'Or](#règles-dor)
- [🛠 Architecture & Outils](#architecture-outils)
  - [🎼 Orchestrateur (`.dev/agents/orchestrator/main.py`)](#orchestrateur-devagentsorchestratormainpy)
  - [🔄 Documentation Agent (`.dev/agents/documentation/agent.py`)](#documentation-agent-devagentsdocumentationagentpy)
- [🎨 Conventions Visuelles](#conventions-visuelles)
  - [Emojis Suggérés](#emojis-suggérés)
- [📂 Organisation des Dossiers](#organisation-des-dossiers)
<!-- TOC END -->

## 📜 Règles d'Or

1.  **Pas de Régression de Contenu** : Ne jamais supprimer ou altérer le contenu informatif des fichiers existants lors des restructurations.
2.  **Documentation Vivante** : Tout ajout de connaissance doit être immédiatement répercuté dans la documentation.
3.  **Reflexes Visuels** : Utiliser des Emojis pour chaque titre (H1, H2, H3) afin de faciliter la lecture rapide (scan visuel).
4.  **Liens Explicites** : Tout lien vers un dossier doit pointer explicitement vers son `README.md` (ex: `[Dossier](./dossier/README.md)` et non `[Dossier](./dossier/)`).
5.  **Français par défaut** : Toute communication, commentaire de code (si possible) et documentation doit être rédigée en Français.

## 🛠 Architecture & Outils

Le système repose sur une architecture multi-agents pilotée par un orchestrateur central.

### 🎼 Orchestrateur (`.dev/agents/orchestrator/main.py`)
C'est le point d'entrée unique. Il coordonne l'exécution des agents dans l'ordre logique (Readme -> Documentation -> Coherence -> Expert).

### 🔄 Documentation Agent (`.dev/agents/documentation/agent.py`)
Assure la maintenance automatique :
*   Génération des fils d'Ariane (Breadcrumbs).
*   Génération des Tables des Matières (TOC).
*   Maintien de la cohérence des liens.

## 🎨 Conventions Visuelles

### Emojis Suggérés
*   **Finance** : 💰, 💳, 🧾, 📊, 📈, 📉
*   **Analyse** : 🧠, 🔬
*   **Navigation** : 🏠, 📂, 📄, 📜, 🔙
*   **Technique** : ⚙️, 🛠, 💻, 🤖, 🎼
*   **Humain** : 👥, 🤝, 👤, 🎩

## 📂 Organisation des Dossiers

*   `/` (Racine) : Contient les dossiers thématiques (`/documents`, `/annexes`) et le point d'entrée `README.md`.
*   `/SOURCE` : Documents bruts, transcriptions et archives de recherches.
*   `/.dev` : Cœur technique du projet (Agents, Scripts, Configuration).
    *   `/.dev/agents` : Définition de chaque agent spécialisé.

---
*Dernière mise à jour par l'Agent IA.*
