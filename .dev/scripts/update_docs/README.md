<!-- BREADCRUMB START -->
[🏠](../../../README.md) > [📂 Dev](../../README.md) > [🛠 Scripts Utilitaires](../README.md)
<!-- BREADCRUMB END -->

# 🔄 Script de Maintenance Automatisée des Docs

> [!NOTE]
> Ce document est conçu pour accompagner de l'utilisateur débutant à l'expert technique.

## 1. Fiche d'Identité

| Information | Détail |
| :--- | :--- |
| **Nom du fichier** | `script.py` |
| **Emplacement** | `.dev/scripts/update_docs/` |
| **Langage** | Python 3 |
| **Auteur** | Équipe DeepMind / Assistant IA |
| **Date de Création** | 25 Décembre 2025 |
| **Dernière Modif** | 25 Décembre 2025 |
| **Mode d'Exécution** | Manuel ou Automatisé (CI/CD) |

---

## 2. Pour les Débutants

### 2.1. C'est quoi ce fichier ?
Imaginez ce script comme un **jardinier automatique** pour votre documentation.
Quand vous écrivez beaucoup de fichiers `.md` (Markdown), il est facile d'oublier de mettre à jour la table des matières ou les liens de retour vers l'accueil.

Ce script s'occupe de tout ça pour vous ! Il parcourt tous vos fichiers et ajoute :
1.  Un **Fil d'Ariane** (Breadumb) en haut de page pour savoir où on est (ex: `🏠 > Dossier > Fichier`).
2.  Une **Table des Matières** automatique basée sur vos titres.

### 2.2. Comment l'utiliser ?
Si vous avez ajouté ou modifié un fichier Markdown, lancez simplement cette commande dans votre terminal, à la racine du projet :

```bash
python3 .dev/scripts/update_docs/script.py
```

C'est tout ! Le script va scanner vos fichiers et vous dire ce qu'il a mis à jour avec un ✅.

---

## 3. Pour les Intermédiaires

### 3.1. Pré-requis
- Python 3 installé.
- Avoir les droits d'écriture sur les fichiers du projet.

### 3.2. Fonctionnement Global
Le script fonctionne de manière récursive à partir de la racine du projet.
Il ignore intelligemment :
- Le dossier `.dev` (où il se trouve lui-même).
- Le dossier `.git` (fichiers système de versionning).

Il recherche deux balises HTML spécifiques dans vos fichiers :
*   `<!-- BREADCRUMB START -->
[🏠](../../../README.md) > [📂 Dev](../../README.md) > [🛠 Scripts Utilitaires](../README.md)
<!-- BREADCRUMB END -->`
*   `<!-- TOC START --
- [1. Fiche d'Identité](#1-fiche-didentite)
- [2. Pour les Débutants](#2-pour-les-debutants)
  - [2.1. C'est quoi ce fichier ?](#21-cest-quoi-ce-fichier)
  - [2.2. Comment l'utiliser ?](#22-comment-lutiliser)
- [3. Pour les Intermédiaires](#3-pour-les-intermediaires)
  - [3.1. Pré-requis](#31-pre-requis)
  - [3.2. Fonctionnement Global](#32-fonctionnement-global)
  - [3.3. Personnalisation](#33-personnalisation)
- [4. Pour les Experts](#4-pour-les-experts)
  - [4.1. Architecture du Code](#41-architecture-du-code)
    - [4.1.1. Fonctions Clés](#411-fonctions-cles)
  - [4.2. Extension & Maintenance](#42-extension-maintenance)
  - [4.3. Edge Cases gérés](#43-edge-cases-geres)
<!-- TOC END -->`

S'il ne les trouve pas, **il les crée** intelligemment :
- Le *Breadcrumb* est inséré tout en haut.
- La *Table des Matières* est insérée après le premier titre H1 (`# Titre`).

### 3.3. Personnalisation
Les balises sont définies comme constantes au début du script :
```python
BREADCRUMB_START, BREADCRUMB_END = '<!-- BREADCRUMB START -->
[🏠](../../../README.md) > [📂 Dev](../../README.md) > [🛠 Scripts Utilitaires](../README.md)
<!-- BREADCRUMB END -->'
```
Vous pouvez modifier ces constantes si vous souhaitez utiliser d'autres marqueurs, mais attention à la rétro-compatibilité !

---

## 4. Pour les Experts

### 4.1. Architecture du Code

Le script est modulaire et utilise `pathlib` pour une gestion robuste des chemins cross-platform (Linux/Windows/MacOS).

#### 4.1.1. Fonctions Clés

1.  **`get_document_title(md_file_path)`**
    *   Parse le fichier pour trouver la première ligne commençant par `# `.
    *   Fallback sur le nom du dossier/fichier si aucun H1 n'est trouvé.

2.  **`generate_breadcrumb(file_path, root_path)`**
    *   Calcule le chemin relatif depuis la racine.
    *   Génère des liens relatifs (`../..`) pour garantir que la navigation fonctionne même sans serveur web (en local ou sur GitHub).

3.  **`create_anchor(title)`**
    *   Transforme "Mon Titre Génial !" en `mon-titre-gnial`.
    *   **Note Importante** : Cette fonction tente d'imiter l'algorithme de génération d'ancre de GitHub (`github-slugger`). Elle supprime les emojis et caractères spéciaux.

4.  **`update_markdown_file(file_path, root_path)`**
    *   Lit le fichier en mémoire.
    *   Injecte les structures si absentes.
    *   Utilise des **Regex** (`re.sub` avec `re.DOTALL`) pour remplacer le contenu entre les balises existantes.
    *   Écrit le fichier sur le disque **uniquement si le contenu a changé** (évite de modifier les timestamps inutilement).

### 4.2. Extension & Maintenance
Pour ajouter une nouvelle fonctionnalité (ex: Footer automatique), suivez ce pattern :
1.  Définir les nouvelles balises constantes.
2.  Créer une fonction `generate_footer(content)`.
3.  Dans `update_markdown_file`, ajouter la logique d'injection (si tag absent) et de remplacement (regex).

### 4.3. Edge Cases gérés
*   **Code Blocks** : La génération de TOC ignore les lignes commençant par `#` si elles sont à l'intérieur d'un bloc de code (délimité par des backticks).
*   **Fichier README racine** : Le breadcrumb est vide ou adapté pour ne pas se lier à lui-même de manière redondante.

---
*Documentation générée par Antigravity.*
