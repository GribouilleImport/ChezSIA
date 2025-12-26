<!-- BREADCRUMB START -->
[🏠](../../README.md) > [📂 Dev](../README.md)
<!-- BREADCRUMB END -->

# 🛠 Scripts Utilitaires

Ce dossier contient l'ensemble des scripts de maintenance et d'automatisation du projet **ChezSIA**.

<!-- TOC START -->
- [1. Contenu](#1-contenu)
- [2. Politique de Maintenance](#2-politique-de-maintenance)
<!-- TOC END -->

## 1. Contenu

| Dossier | Description |
| :--- | :--- |
| **[update_docs](./update_docs/)** | Contient le script `script.py` responsable de la mise à jour automatique des fils d'Ariane (breadcrumbs) et des tables des matières (TOC) dans tous les fichiers Markdown. |

## 2. Politique de Maintenance

Chaque script doit être placé dans son propre sous-dossier contenant :
1.  Le script lui-même (ex: `script.py` ou `nom_explicite.sh`).
2.  Un `README.md` détaillant son fonctionnement, ses pré-requis et son mode d'exécution.

> [!TIP]
> Pour ajouter un nouveau script, créez un nouveau dossier ici et suivez le modèle de documentation existant dans `update_docs/README.md`.
