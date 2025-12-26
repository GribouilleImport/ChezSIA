#!/usr/bin/env python3

import os
import re
import unicodedata

# --- Utility Functions (Corrected for GitHub Compatibility) ---

def slugify(header_title):
    """
    Converts a header title to a GitHub-style anchor link, handling
    accents, special characters, and emojis correctly.
    """
    # 1. Remove emojis by checking for character properties
    title_no_emoji = "".join(c for c in header_title if unicodedata.category(c) != 'So')

    # 2. Normalize accents (e.g., 'é' -> 'e')
    normalized_title = unicodedata.normalize('NFKD', title_no_emoji).encode('ascii', 'ignore').decode('ascii')

    # 3. Keep only letters, numbers, spaces, and hyphens
    clean_title = re.sub(r'[^\w\s-]', '', normalized_title).strip()

    # 4. Replace spaces with hyphens and clean up
    slug = re.sub(r'\s+', '-', clean_title).lower()

    # 5. Handle potential empty slugs if title was only symbols/emojis
    return slug if slug else "section"


# --- Core Logic Functions ---

def update_file_content(file_path):
    """
    Processes a single markdown file: renumbers headers (excluding TOC),
    and updates the Table of Contents with correct anchor links.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # --- Pass 1: Renumber headers ---
    renumbered_lines = []
    header_counters = [0, 0, 0, 0] # H2, H3, H4, H5
    new_headers = []

    toc_header_pattern = re.compile(r'#+\s*(\d\.\s*)?📖\s*Table des Matières', re.IGNORECASE)

    for line in lines:
        # Match H1 to H5 headers, but not H1 if it's the main document title
        match = re.match(r'^(#+)\s+', line)
        if match and not (line.startswith('# ') and len(renumbered_lines) < 5):
            level = len(match.group(1))

            # Demote H1 to H2 for numbering purposes
            if level == 1:
                level = 2

            if 2 <= level <= 5 and not toc_header_pattern.search(line):
                title_match = re.match(r'^(#+)\s*([\d\.]*\s*)?(.*)', line)
                clean_title = title_match.group(3).strip() if title_match else line.strip()

                counter_index = level - 2
                header_counters[counter_index] += 1
                for i in range(counter_index + 1, len(header_counters)):
                    header_counters[i] = 0

                numbering_parts = [str(c) for c in header_counters[:counter_index + 1]]
                numbering = '.'.join(numbering_parts) + '.'

                full_title = f"{numbering} {clean_title}"
                new_headers.append({'level': level, 'full_title': full_title})

                hashes = '#' * level
                new_line = f'{hashes} {full_title}\n'
                renumbered_lines.append(new_line)
            else:
                renumbered_lines.append(line)
        else:
            renumbered_lines.append(line)
            if toc_header_pattern.search(line):
                 new_headers.append({'level': 2, 'full_title': line.strip('# \n')})


    # --- Pass 2: Update TOC ---
    content = "".join(renumbered_lines)
    toc_start_marker = '<!-- TOC START -->'
    toc_end_marker = '<!-- TOC END -->'

    start_index = content.find(toc_start_marker)
    end_index = content.find(toc_end_marker)

    if start_index != -1 and end_index != -1:
        toc_lines = []
        headers_for_toc = [h for h in new_headers if not toc_header_pattern.search(h['full_title'])]

        for header in headers_for_toc:
            slug = slugify(header['full_title'])
            indent = '  ' * (header['level'] - 2)
            toc_lines.append(f"{indent}- [{header['full_title']}](#{slug})")

        new_toc_content = '\n'.join(toc_lines)

        pre_toc = content[:start_index + len(toc_start_marker)]
        post_toc = content[end_index:]
        content = f"{pre_toc}\n{new_toc_content}\n{post_toc}"

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


# --- Sitemap Generation Logic (with Perfect Alignment) ---

def get_headers_with_numbers(file_path):
    """Extracts H2-H5 headers, separating number from title."""
    headers = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'^(##+)\s+([\d\.]+)\s+(.*)', line)
            if match:
                level = len(match.group(1))
                number = match.group(2).strip()
                title = match.group(3).strip()
                if not "Table des Matières" in title:
                    headers.append({'level': level, 'number': number, 'title': title})
    return headers

def build_header_tree(headers):
    """Builds a tree from a flat list of headers."""
    root = {'level': 1, 'children': []}
    parent_stack = [root]
    for header in headers:
        new_node = {'level': header['level'], 'number': header['number'], 'title': header['title'], 'children': []}
        while parent_stack[-1]['level'] >= new_node['level']:
            parent_stack.pop()
        parent_stack[-1]['children'].append(new_node)
        parent_stack.append(new_node)
    return root['children']

def format_header_tree(tree, prefix):
    """Recursively formats the header tree with perfect vertical alignment."""
    lines = []
    if not tree:
        return lines

    max_widths = {}

    def find_max_widths(nodes, level=0):
        if not nodes:
            return
        max_w = max(len(node['number']) for node in nodes) if nodes else 0
        max_widths[level] = max(max_widths.get(level, 0), max_w)
        for node in nodes:
            find_max_widths(node['children'], level + 1)

    find_max_widths(tree)

    def format_nodes(nodes, current_prefix, level=0):
        formatted_lines = []
        for i, node in enumerate(nodes):
            is_last = (i == len(nodes) - 1)
            tree_char = '└──' if is_last else '├──'

            padded_number = node['number'].ljust(max_widths.get(level, 0))

            formatted_lines.append(f"{current_prefix}{tree_char} {padded_number} {node['title']}")

            child_prefix = current_prefix + ('    ' if is_last else '│   ')
            formatted_lines.extend(format_nodes(node['children'], child_prefix, level + 1))
        return formatted_lines

    return format_nodes(tree, prefix)

def generate_sitemap_recursive(root_path, prefix=''):
    """Recursively walks the directory tree to build the sitemap."""
    sitemap_lines = []
    try:
        items = sorted(os.listdir(root_path))
    except OSError:
        return []

    excluded_items = ['node_modules']
    dirs = [item for item in items if os.path.isdir(os.path.join(root_path, item)) and item not in excluded_items]
    files = [item for item in items if item.endswith('.md')]

    for i, dirname in enumerate(dirs):
        is_last = (i == len(dirs) - 1) and (len(files) == 0)
        dir_prefix_char = '└──' if is_last else '├──'
        sitemap_lines.append(f'{prefix}{dir_prefix_char} 📁 {dirname}/')
        child_prefix = prefix + ('    ' if is_last else '│   ')
        sitemap_lines.extend(generate_sitemap_recursive(os.path.join(root_path, dirname), child_prefix))

    for i, filename in enumerate(files):
        is_last = (i == len(files) - 1)
        file_path = os.path.join(root_path, filename)
        relative_path = os.path.relpath(file_path, '.')
        with open(file_path, 'r', encoding='utf-8') as f_h1:
            h1_match = re.search(r'^#\s+(.*)', f_h1.read(), re.MULTILINE)
            h1_title = h1_match.group(1).strip() if h1_match else filename
        file_prefix_char = '└──' if is_last else '├──'
        sitemap_lines.append(f'{prefix}{file_prefix_char} {h1_title} ({relative_path})')
        headers = get_headers_with_numbers(file_path)
        header_tree = build_header_tree(headers)
        header_base_prefix = prefix + ('    ' if is_last else '│   ')
        sitemap_lines.extend(format_header_tree(header_tree, header_base_prefix))
    return sitemap_lines

def build_sitemap():
    """Builds the complete sitemap string."""
    sitemap = ['# 📂 SiteMap - ChezSIA', '> **Dernière mise à jour :** Généré automatiquement', '> **Structure :** Arborescence complète du Business Plan', '---', '```', 'ChezSIA/']
    root_dir = '.'

    root_readme_path = os.path.join(root_dir, 'README.md')
    if os.path.exists(root_readme_path):
        with open(root_readme_path, 'r', encoding='utf-8') as f:
            h1_match = re.search(r'^#\s+(.*)', f.read(), re.MULTILINE)
            readme_h1 = h1_match.group(1).strip() if h1_match else "README.md"
        sitemap.append('│')
        sitemap.append(f'├── {readme_h1} (README.md)')
        headers = get_headers_with_numbers(root_readme_path)
        header_tree = build_header_tree(headers)
        sitemap.extend(format_header_tree(header_tree, '│   '))

    excluded_toplevel = ['.git', '.scripts', 'node_modules', '.dev']
    top_level_dirs = sorted([d for d in os.listdir(root_dir) if os.path.isdir(d) and d not in excluded_toplevel])
    if os.path.isdir('.dev'):
        top_level_dirs.append('.dev')

    for i, dirname in enumerate(top_level_dirs):
        is_last_dir = (i == len(top_level_dirs) - 1)
        dir_prefix = '└──' if is_last_dir else '├──'
        sitemap.append('│')
        sitemap.append(f'{dir_prefix} 📁 {dirname}/')
        child_prefix = '    ' if is_last_dir else '│   '
        sitemap.extend(generate_sitemap_recursive(dirname, child_prefix))

    sitemap.append('```')
    return '\n'.join(sitemap)


# --- Main Execution Block ---

if __name__ == '__main__':
    print("--- Maintenance du Business Plan ---")

    all_md_files = []
    excluded_dirs = ['.git', '.scripts', 'node_modules']
    for root, dirs, files in os.walk('.', topdown=True):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for file in sorted(files):
            if file.endswith('.md') and file.lower() != 'sitemap.md':
                all_md_files.append(os.path.join(root, file))

    print(f"\nÉtape 1: Renumérotation et mise à jour des fichiers pour {len(all_md_files)} fichiers...")
    for file_path in all_md_files:
        print(f"  - Traitement de : {file_path}")
        update_file_content(file_path)
    print("✅ Traitement des fichiers terminé.")

    print("\nÉtape 2: Génération du SiteMap...")
    sitemap_content = build_sitemap()
    with open('SiteMap.md', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print("✅ SiteMap.md généré avec succès.")
    print("\n--- Maintenance terminée ---")
