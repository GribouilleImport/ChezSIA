<!-- BREADCRUMB START -->
[🏠](../../../README.md) > [📂 Dev](../../README.md) > [🛠 Scripts Utilitaires](../README.md) > [🔄 Script de Maintenance Automatisée des Docs](README.md)
<!-- BREADCRUMB END -->

# 🔄 Script de Maintenance Automatisée des Docs

> [!NOTE]
> Ce document est conçu pour accompagner de l'utilisateur débutant à l'expert technique.

## 📋 Fiche d'Identité

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

## 🐣 Pour les Débutants

### C'est quoi ce fichier ?
Imaginez ce script comme un **jardinier automatique** pour votre documentation.
Quand vous écrivez beaucoup de fichiers `.md` (Markdown), il est facile d'oublier de mettre à jour la table des matières ou les liens de retour vers l'accueil.

Ce script s'occupe de tout ça pour vous ! Il parcourt tous vos fichiers et ajoute :
1.  Un **Fil d'Ariane** (Breadumb) en haut de page pour savoir où on est (ex: `🏠 > Dossier > Fichier`).
2.  Une **Table des Matières** automatique basée sur vos titres.

### Comment l'utiliser ?
Si vous avez ajouté ou modifié un fichier Markdown, lancez simplement cette commande dans votre terminal, à la racine du projet :

```bash
python3 .dev/scripts/update_docs/script.py
```

C'est tout ! Le script va scanner vos fichiers et vous dire ce qu'il a mis à jour avec un ✅.

---

## 🤓 Pour les Intermédiaires

### Pré-requis
- Python 3 installé.
- Avoir les droits d'écriture sur les fichiers du projet.

### Fonctionnement Global
Le script fonctionne de manière récursive à partir de la racine du projet.
Il ignore intelligemment :
- Le dossier `.dev` (où il se trouve lui-même).
- Le dossier `.git` (fichiers système de versionning).

Il recherche deux balises HTML spécifiques dans vos fichiers :
*   `<!-- BREADCRUMB START -->
[🏠](../../../README.md) > [📂 Dev](../../README.md) > [🛠 Scripts Utilitaires](../README.md) > [🔄 Script de Maintenance Automatisée des Docs](README.md)
<!-- BREADCRUMB END -->`
*   `<!-- TOC START -->
## 📖 Table des Matières

- [📋 Fiche d'Identité](#fiche-didentité)
- [🐣 Pour les Débutants](#pour-les-débutants)
  - [C'est quoi ce fichier ?](#cest-quoi-ce-fichier)
  - [Comment l'utiliser ?](#comment-lutiliser)
- [🤓 Pour les Intermédiaires](#pour-les-intermédiaires)
  - [Pré-requis](#pré-requis)
  - [Fonctionnement Global](#fonctionnement-global)
- [📖 Table des Matières](#table-des-matières)
  - [Personnalisation](#personnalisation)
- [🧙‍♂️ Pour les Experts](#pour-les-experts)
  - [Architecture du Code](#architecture-du-code)
  - [Extension & Maintenance](#extension-maintenance)
  - [Edge Cases gérés](#edge-cases-gérés)
<!-- TOC END -->`

S'il ne les trouve pas, **il les crée** intelligemment :
- Le *Breadcrumb* est inséré tout en haut.
- La *Table des Matières* est insérée après le premier titre H1 (`# Titre`).

### Personnalisation
Les balises sont définies comme constantes au début du script :
```python
BREADCRUMB_START, BREADCRUMB_END = '<!-- BREADCRUMB START -->
[🏠](../../../README.md) > [📂 Dev](../../README.md) > [🛠 Scripts Utilitaires](../README.md) > [🔄 Script de Maintenance Automatisée des Docs](README.md)
<!-- BREADCRUMB END -->'
```
Vous pouvez modifier ces constantes si vous souhaitez utiliser d'autres marqueurs, mais attention à la rétro-compatibilité !

---

## 🧙‍♂️ Pour les Experts

### Architecture du Code

Le script est modulaire et utilise `pathlib` pour une gestion robuste des chemins cross-platform (Linux/Windows/MacOS).

#### Fonctions Clés

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

### Extension & Maintenance
Pour ajouter une nouvelle fonctionnalité (ex: Footer automatique), suivez ce pattern :
1.  Définir les nouvelles balises constantes.
2.  Créer une fonction `generate_footer(content)`.
3.  Dans `update_markdown_file`, ajouter la logique d'injection (si tag absent) et de remplacement (regex).

### Edge Cases gérés
*   **Code Blocks** : La génération de TOC ignore les lignes commençant par `#` si elles sont à l'intérieur d'un bloc de code (délimité par des backticks).
*   **Fichier README racine** : Le breadcrumb est vide ou adapté pour ne pas se lier à lui-même de manière redondante.

---
*Documentation générée par Antigravity.*
