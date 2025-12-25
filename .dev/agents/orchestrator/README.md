<!-- BREADCRUMB START -->
[🏠](../../../README.md) > [📂 .dev](../../README.md) > [🤖 Agents](../README.md) > [Orchestrateur (Main)](README.md)
<!-- BREADCRUMB END -->

# Orchestrateur (Main)

C'est le point d'entrée du système multi-agents.

<!-- TOC START -->
## 📖 Table des Matières

- [📖 Table des Matières](#table-des-matières)
- [Usage](#usage)
- [Rôle](#rôle)
<!-- TOC END -->

## Usage
Depuis la racine du projet :
```bash
python .dev/agents/orchestrator/main.py
```

## Rôle
- Initialise les chemins vers les documents financiers.
- Lance l'Agent de Cohérence pour la vérification technique.
- Transmet les résultats à l'Agent Expert pour le rapport final.
