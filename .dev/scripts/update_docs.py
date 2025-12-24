#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

# --- Fonctions pour le Fil d'Ariane ---

def get_h1_title(md_file_path):
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('# '):
                    title = re.sub(r'#\s* emojis\s*', '', line).strip()
                    return title
    except FileNotFoundError:
        return None
    return Path(md_file_path).stem

def generate_breadcrumb(file_path, root_path):
    file_path = Path(file_path).resolve()
    root_path = Path(root_path).resolve()
    if file_path == root_path / 'README.md':
        return ""
    relative_path = file_path.relative_to(root_path)
    depth = len(relative_path.parts) - 1
    root_link = os.path.join(*(['..'] * depth), 'README.md')
    breadcrumbs = [f'[🏠]({root_link})']
    for i, part in enumerate(relative_path.parts[:-1]):
        readme_path = root_path / Path(*relative_path.parts[:i+1]) / 'README.md'
        link_path = os.path.join(*(['..'] * (depth - i - 1)), part, 'README.md')
        dir_name = get_h1_title(readme_path)
        breadcrumbs.append(f'[{dir_name}]({link_path})')
    return ' > '.join(breadcrumbs)

# --- Fonctions pour la Table des Matières ---

def create_anchor(title):
    title = title.lower()
    # Enlève les emojis et la ponctuation, garde les lettres, chiffres, espaces
    title = re.sub(r'[^\w\s-]', '', title)
    # Remplace les espaces par des tirets
    return re.sub(r'\s+', '-', title).strip('-')

def generate_toc(content):
    toc = []
    headers = re.findall(r'^(##|###)\s(.+)', content, re.MULTILINE)
    for level, title in headers:
        anchor = create_anchor(title)
        indent = "  " if level == '###' else ""
        toc.append(f"{indent}- [{title}](#{anchor})")
    if toc:
        return "## 📖 Table des Matières\n\n" + '\n'.join(toc)
    return ""

# --- Script Principal ---

def update_markdown_file(file_path, root_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return

    original_content = content

    # --- Gestion des balises ---
    BREADCRUMB_START, BREADCRUMB_END = '<!-- BREADCRUMB START -->', '<!-- BREADCRUMB END -->'
    TOC_START, TOC_END = '<!-- TOC START -->', '<!-- TOC END -->'

    if BREADCRUMB_START not in content:
        content = f"{BREADCRUMB_START}\n{BREADCRUMB_END}\n\n" + content

    if TOC_START not in content:
        # Insère les balises TOC après la première section (après le '---')
        parts = content.split('---', 1)
        if len(parts) == 2:
            content = f"{parts[0]}---\n\n{TOC_START}\n{TOC_END}\n\n{parts[1]}"
        # Ou après le H1 si pas de '---'
        else:
             parts = content.split('\n', 1)
             if len(parts) == 2:
                 content = f"{parts[0]}\n\n{TOC_START}\n{TOC_END}\n\n{parts[1]}"

    # --- Mise à jour du Fil d'Ariane ---
    breadcrumb_text = generate_breadcrumb(file_path, root_path)
    content = re.sub(
        f"({BREADCRUMB_START})(.*?)({BREADCRUMB_END})",
        f"\\1\n{breadcrumb_text}\n\\3",
        content,
        flags=re.DOTALL
    )

    # --- Mise à jour de la Table des Matières ---
    toc_text = generate_toc(content)
    content = re.sub(
        f"({TOC_START})(.*?)({TOC_END})",
        f"\\1\n{toc_text}\n\\3",
        content,
        flags=re.DOTALL
    )

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Document mis à jour : {file_path}")

def main():
    project_root = Path(__file__).resolve().parent.parent.parent
    for md_file in project_root.rglob('*.md'):
        # Exclure les fichiers dans .dev pour éviter les boucles
        if ".dev" not in str(md_file):
            update_markdown_file(md_file, project_root)

if __name__ == "__main__":
    print("🚀 Lancement de la mise à jour des documents...")
    main()
    print("🎉 Terminé.")
