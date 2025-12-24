#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
from pathlib import Path

def get_h1_title(md_file_path):
    """Extrait le titre H1 d'un fichier Markdown."""
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('# '):
                    title = line[2:].strip()
                    title = re.sub(r'^\s*[^\w\s]*\s*', '', title)
                    return title
    except FileNotFoundError:
        return None
    return None

def generate_breadcrumb(file_path, root_path):
    """Génère le fil d'Ariane pour un fichier donné."""
    file_path = Path(file_path).resolve()
    root_path = Path(root_path).resolve()

    if file_path == root_path / 'README.md':
        return ''

    relative_path = file_path.relative_to(root_path)
    depth = len(relative_path.parts) - 1
    root_link = Path(*(['..'] * depth)) / 'README.md'
    breadcrumbs = [f'[🏠]({root_link})']

    current_path = Path(root_path)
    for i, part in enumerate(relative_path.parts[:-1]):
        current_path = current_path / part
        readme_path = current_path / 'README.md'
        link_path = Path(*(['..'] * (depth - i - 1))) / part
        dir_name = get_h1_title(readme_path) or part

        if readme_path.is_file():
            breadcrumbs.append(f'[{dir_name}]({link_path / "README.md"})')
        else:
            breadcrumbs.append(f'{dir_name}')

    return ' > '.join(breadcrumbs)

def update_markdown_file(file_path, root_path):
    """Applique la mise à jour du fil d'Ariane sur un fichier Markdown."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Erreur de lecture du fichier {file_path}: {e}")
        return

    original_content = content

    breadcrumb_start_tag = '<!-- BREADCRUMB START -->'
    breadcrumb_end_tag = '<!-- BREADCRUMB END -->'

    breadcrumb_content = generate_breadcrumb(file_path, root_path)

    new_content = re.sub(
        f"({breadcrumb_start_tag})(.*?)({breadcrumb_end_tag})",
        f"\\1\n{breadcrumb_content}\n\\3",
        content,
        flags=re.DOTALL
    )

    if new_content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Fil d'Ariane mis à jour pour : {file_path}")
        except Exception as e:
            print(f"Erreur d'écriture dans le fichier {file_path}: {e}")

def main():
    """Fonction principale du script."""
    project_root = Path(__file__).parent.parent.parent.resolve()

    print(f"🚀 Lancement de la mise à jour des fils d'Ariane depuis la racine : {project_root}")

    # S'assurer que chaque fichier a les balises BREADCRUMB
    for md_file in project_root.rglob('*.md'):
        with open(md_file, 'r+', encoding='utf-8') as f:
            content = f.read()
            if '<!-- BREADCRUMB START -->' not in content:
                f.seek(0, 0)
                f.write('<!-- BREADCRUMB START -->\n<!-- BREADCRUMB END -->\n\n' + content)

    for md_file in project_root.rglob('*.md'):
        update_markdown_file(str(md_file), str(project_root))

    print("🎉 Terminé.")

if __name__ == "__main__":
    main()
