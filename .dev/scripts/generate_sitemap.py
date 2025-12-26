#!/usr/bin/env python3

import os
import re
import unicodedata

# --- Constants & Patterns ---

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U00002700-\U000027BF"  # dingbats
    "\U000024C2-\U0001F251"
    "\U0001f926-\U0001f937"
    "\U00010000-\U0010ffff"
    "\u2640-\u2642"
    "\u2600-\u2B55"
    "\u200d"
    "\u23cf"
    "\u23e9"
    "\u231a"
    "\ufe0f"  # variation selector
    "\u3030"
    "]+", flags=re.UNICODE)

# --- Utility Functions ---

def slugify(header_title):
    """
    Converts a header title to a GitHub-style anchor link, handling
    accents, special characters, and emojis correctly.
    """
    title_no_emoji = EMOJI_PATTERN.sub(r'', header_title)
    normalized_title = unicodedata.normalize('NFKD', title_no_emoji).encode('ascii', 'ignore').decode('ascii')
    clean_title = re.sub(r'[^\w\s-]', '', normalized_title).strip()
    slug = re.sub(r'\s+', '-', clean_title).lower()
    return slug if slug else "section"

# --- Core Logic Functions (File Processing) ---

def update_file_content(file_path):
    """
    Processes a single markdown file: renumbers and cleans headers (excluding TOC),
    and updates the Table of Contents with correct anchor links.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # --- Pass 1: Renumber and clean headers ---
    renumbered_lines = []
    header_counters = [0, 0, 0, 0] # H2, H3, H4, H5
    new_headers = []
    toc_header_pattern = re.compile(r'#+\s*(\d\.\s*)?(📖\s*)?Table des Matières', re.IGNORECASE)

    for line in lines:
        match = re.match(r'^(#+)\s+', line)
        # Process headers, but not H1s at the start of the file (usually the main title)
        if match and not (line.startswith('# ') and len(renumbered_lines) < 5):
            level = len(match.group(1))
            if level == 1: level = 2 # Demote H1 to H2 for consistency

            # Process H2-H5, but skip the "Table of Contents" header itself
            if 2 <= level <= 5 and not toc_header_pattern.search(line):
                title_match = re.match(r'^(#+)\s*([\d\.]*\s*)?(.*)', line)
                raw_title = title_match.group(3).strip() if title_match else line.strip()
                clean_title = EMOJI_PATTERN.sub(r'', raw_title).strip()

                counter_index = level - 2
                header_counters[counter_index] += 1
                for i in range(counter_index + 1, len(header_counters)):
                    header_counters[i] = 0

                numbering = '.'.join([str(c) for c in header_counters[:counter_index + 1]]) + '.'
                full_title = f"{numbering} {clean_title}"
                new_headers.append({'level': level, 'full_title': full_title})

                hashes = '#' * level
                new_line = f'{hashes} {full_title}\n'
                renumbered_lines.append(new_line)
            else:
                renumbered_lines.append(line)
        else:
            renumbered_lines.append(line)
            # Add TOC header to the list for context, but it will be filtered out later
            if toc_header_pattern.search(line):
                 clean_toc_title = EMOJI_PATTERN.sub(r'', line.strip('# \n')).strip()
                 new_headers.append({'level': 2, 'full_title': clean_toc_title})

    # --- Pass 2: Update TOC ---
    content = "".join(renumbered_lines)
    toc_start_marker = '<!-- TOC START -->'
    toc_end_marker = '<!-- TOC END -->'
    start_index = content.find(toc_start_marker)
    end_index = content.find(toc_end_marker)

    if start_index != -1 and end_index != -1:
        toc_lines = []
        # Filter out the "Table of Contents" header from the TOC entries
        headers_for_toc = [h for h in new_headers if "Table des Matières" not in h['full_title']]
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


# --- Sitemap Generation Logic ---

def get_clean_headers_for_sitemap(file_path):
    """Extracts H2-H5 headers and returns a clean title for the sitemap."""
    headers = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'^(##+)\s+([\d\.]+)\s+(.*)', line)
            if match:
                level = len(match.group(1))
                number = match.group(2).strip()
                title = match.group(3).strip()
                # Headers should be clean already, but this is a safeguard
                clean_title = EMOJI_PATTERN.sub(r'', title).strip()
                if "Table des Matières" not in clean_title:
                    headers.append({'level': level, 'title': f"{number} {clean_title}"})
    return headers

def build_header_tree_sitemap(headers):
    """Builds a tree from a flat list of headers for the sitemap."""
    root = {'level': 1, 'children': []}
    parent_stack = [root]
    for header in headers:
        new_node = {'level': header['level'], 'title': header['title'], 'children': []}
        while parent_stack[-1]['level'] >= new_node['level']:
            parent_stack.pop()
        parent_stack[-1]['children'].append(new_node)
        parent_stack.append(new_node)
    return root['children']

def format_header_tree_sitemap(tree, prefix):
    """Recursively formats the header tree with clean titles for the sitemap."""
    lines = []
    for i, node in enumerate(tree):
        is_last = (i == len(tree) - 1)
        tree_char = '└──' if is_last else '├──'
        lines.append(f"{prefix}{tree_char} {node['title']}")
        child_prefix = prefix + ('    ' if is_last else '│   ')
        lines.extend(format_header_tree_sitemap(node['children'], child_prefix))
    return lines

def generate_sitemap_recursive(root_path, prefix=''):
    """Recursively walks the directory tree to build the sitemap with clickable links."""
    sitemap_lines = []
    try:
        items = sorted(os.listdir(root_path))
    except OSError: return []

    excluded_items = ['node_modules']
    dirs = [item for item in items if os.path.isdir(os.path.join(root_path, item)) and item not in excluded_items]
    files = [item for item in items if item.endswith('.md')]

    for i, dirname in enumerate(dirs):
        is_last = (i == len(dirs) - 1) and (len(files) == 0)
        dir_prefix_char = '└──' if is_last else '├──'
        readme_path = os.path.join(root_path, dirname, "README.md").replace(os.sep, '/')
        link = f"[{dirname}/]({readme_path})" if os.path.exists(readme_path) else f"{dirname}/"
        sitemap_lines.append(f'{prefix}{dir_prefix_char} 📁 {link}')
        child_prefix = prefix + ('    ' if is_last else '│   ')
        sitemap_lines.extend(generate_sitemap_recursive(os.path.join(root_path, dirname), child_prefix))

    for i, filename in enumerate(files):
        is_last = (i == len(files) - 1)
        file_path = os.path.join(root_path, filename)
        relative_path = os.path.relpath(file_path, '.').replace(os.sep, '/')
        with open(file_path, 'r', encoding='utf-8') as f_h1:
            h1_match = re.search(r'^#\s+(.*)', f_h1.read(), re.MULTILINE)
            h1_title = h1_match.group(1).strip() if h1_match else filename

        file_prefix_char = '└──' if is_last else '├──'
        sitemap_lines.append(f'{prefix}{file_prefix_char} [{h1_title}]({relative_path})')
        headers = get_clean_headers_for_sitemap(file_path)
        header_tree = build_header_tree_sitemap(headers)
        header_base_prefix = prefix + ('    ' if is_last else '│   ')
        sitemap_lines.extend(format_header_tree_sitemap(header_tree, header_base_prefix))
    return sitemap_lines

def build_sitemap():
    """Builds the complete sitemap string in the new Markdown link format."""
    sitemap = ['# 📂 SiteMap - ChezSIA', '> **Dernière mise à jour :** Généré automatiquement', '> **Structure :** Arborescence complète du Business Plan', '---', 'ChezSIA/']
    root_dir = '.'

    root_readme_path = os.path.join(root_dir, 'README.md')
    if os.path.exists(root_readme_path):
        with open(root_readme_path, 'r', encoding='utf-8') as f:
            h1_match = re.search(r'^#\s+(.*)', f.read(), re.MULTILINE)
            readme_h1 = h1_match.group(1).strip() if h1_match else "README.md"
        sitemap.append('│')
        sitemap.append(f'├── [{readme_h1}](README.md)')
        headers = get_clean_headers_for_sitemap(root_readme_path)
        header_tree = build_header_tree_sitemap(headers)
        sitemap.extend(format_header_tree_sitemap(header_tree, '│   '))

    excluded_toplevel = ['.git', '.scripts', 'node_modules', '.dev']
    top_level_dirs = sorted([d for d in os.listdir(root_dir) if os.path.isdir(d) and d not in excluded_toplevel])
    if os.path.isdir('.dev'): top_level_dirs.append('.dev')

    for i, dirname in enumerate(top_level_dirs):
        is_last_dir = (i == len(top_level_dirs) - 1)
        dir_prefix = '└──' if is_last_dir else '├──'
        readme_path = os.path.join(dirname, "README.md").replace(os.sep, '/')
        link = f"[{dirname}/]({readme_path})" if os.path.exists(readme_path) else f"{dirname}/"
        sitemap.append('│')
        sitemap.append(f'{dir_prefix} 📁 {link}')
        child_prefix = '    ' if is_last_dir else '│   '
        sitemap.extend(generate_sitemap_recursive(dirname, child_prefix))

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

    print(f"\nÉtape 1: Renumérotation et nettoyage des fichiers pour {len(all_md_files)} fichiers...")
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
