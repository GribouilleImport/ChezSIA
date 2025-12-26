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
    """Generates a GitHub-compatible anchor slug from a header title."""
    title_no_emoji = EMOJI_PATTERN.sub(r'', header_title)
    title_no_numbering = re.sub(r'^[\d\.]+\s*', '', title_no_emoji).strip()
    slug = title_no_numbering.lower()
    slug = slug.replace(' ', '-')
    slug = re.sub(r'[?\[\]`.,()*"\'!:@+/]', '', slug)
    return slug if slug else "section"

def get_clean_headers(file_path):
    headers = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'^(##+)\s+([\d\.]+)\s+(.*)', line)
            if match:
                level = len(match.group(1))
                number = match.group(2).strip()
                title = match.group(3).strip()
                clean_title = EMOJI_PATTERN.sub(r'', title).strip()
                if "Table des Matières" not in title:
                    headers.append({'level': level, 'title': f"{number} {clean_title}"})
    return headers

# --- Core Logic: File Renumbering & TOC Update ---

def update_file_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    renumbered_lines, new_headers = [], []
    header_counters = [0, 0, 0, 0] # H2-H5
    toc_header_pattern = re.compile(r'#+\s*(\d\.\s*)?(📖\s*)?Table des Matières', re.IGNORECASE)

    for line in lines:
        match = re.match(r'^(#+)\s+', line)
        if match and not (line.startswith('# ') and len(renumbered_lines) < 5):
            level = len(match.group(1))
            if level == 1: level = 2
            if 2 <= level <= 5 and not toc_header_pattern.search(line):
                title_match = re.match(r'^(#+)\s*([\d\.]*\s*)?(.*)', line)
                raw_title = title_match.group(3).strip() if title_match else line.strip()
                counter_index = level - 2
                header_counters[counter_index] += 1
                for i in range(counter_index + 1, len(header_counters)): header_counters[i] = 0
                numbering = '.'.join(str(c) for c in header_counters[:counter_index + 1]) + '.'
                full_title = f"{numbering} {raw_title}"
                new_headers.append({'level': level, 'full_title': full_title})
                renumbered_lines.append(f"{'#' * level} {full_title}\n")
            else:
                renumbered_lines.append(line)
        else:
            renumbered_lines.append(line)
            if toc_header_pattern.search(line):
                 new_headers.append({'level': 2, 'full_title': line.strip('# \n').strip()})

    content = "".join(renumbered_lines)
    toc_start, toc_end = content.find('<!-- TOC START -->'), content.find('<!-- TOC END -->')
    if toc_start != -1 and toc_end != -1:
        headers_for_toc = [h for h in new_headers if "Table des Matières" not in h['full_title']]
        toc_lines = [f"{'  ' * (h['level'] - 2)}- [{h['full_title']}](#{slugify(h['full_title'])})" for h in headers_for_toc]
        content = f"{content[:toc_start + 17]}\n" + "\n".join(toc_lines) + f"\n{content[toc_end:]}"

    with open(file_path, 'w', encoding='utf-8') as f: f.write(content)

# --- Sitemap Generator: Tree Format with <br> ---

def build_header_tree_br(headers):
    root = {'level': 1, 'children': []}
    stack = [root]
    for h in headers:
        node = {'level': h['level'], 'title': h['title'], 'children': []}
        while stack[-1]['level'] >= node['level']: stack.pop()
        stack[-1]['children'].append(node)
        stack.append(node)
    return root['children']

def format_header_tree_br(tree, prefix):
    lines = []
    for i, node in enumerate(tree):
        is_last = (i == len(tree) - 1)

        try:
            number, rest_of_title = node['title'].split(' ', 1)
            formatted_title = f"{number.strip('.')} {rest_of_title})"
        except ValueError:
            formatted_title = f"{node['title']})"

        if node['level'] <= 2:
            char = '└──' if is_last else '├──'
        else:
            char = '└─' if is_last else '├─'

        lines.append(f"{prefix}{char} {formatted_title}<br>")

        child_prefix = prefix + ('    ' if is_last else '│   ')

        if node['children']:
             lines.extend(format_header_tree_br(node['children'], child_prefix))

        if node['level'] == 2 and not is_last:
            lines.append(f"{prefix}├----------------<br>")

    return lines

def generate_sitemap_recursive_br(root, prefix=''):
    lines = []
    items = sorted(os.listdir(root))
    dirs = [i for i in items if os.path.isdir(os.path.join(root, i)) and i not in ['node_modules']]
    files = [i for i in items if i.endswith('.md') and i.lower() != 'readme.md']

    for i, d in enumerate(dirs):
        is_last = (i == len(dirs) - 1) and not files
        char = '└──' if is_last else '├──'
        readme_path = os.path.join(root, d, "README.md").replace(os.sep, '/')
        link = f"[{d}/]({readme_path})" if os.path.exists(readme_path) else f"{d}/"
        lines.append(f'{prefix}{char} 📁 {link}<br>')
        lines.extend(generate_sitemap_recursive_br(os.path.join(root, d), prefix + ('    ' if is_last else '│   ')))

    if files and dirs:
        lines.append(f'{prefix}│<br>')

    for i, f in enumerate(files):
        is_last = (i == len(files) - 1)
        path, rel_path = os.path.join(root, f), os.path.relpath(os.path.join(root, f), '.').replace(os.sep, '/')
        with open(path, 'r', encoding='utf-8') as h1_f:
            h1 = re.search(r'^#\s+(.*)', h1_f.read(), re.MULTILINE)
            title = EMOJI_PATTERN.sub(r'', h1.group(1).strip() if h1 else f).strip()
        lines.append(f'{prefix}{"└──" if is_last else "├──"} [{title}]({rel_path})<br>')

        headers = get_clean_headers(path)
        if headers:
            tree = build_header_tree_br(headers)
            lines.extend(format_header_tree_br(tree, prefix + ('    ' if is_last else '│   ')))

        if not is_last:
            lines.append(f'{prefix}│<br>')

    return lines

def build_sitemap_br(filename):
    sitemap = [f'# 📂 SiteMap - ChezSIA', '> **Dernière mise à jour :** Généré automatiquement', '> **Structure :** Arborescence complète du Business Plan', '---', 'ChezSIA/<br>']

    excluded = ['.git', '.scripts', 'node_modules', '.dev']
    dirs = sorted([d for d in os.listdir('.') if os.path.isdir(d) and d not in excluded])
    if os.path.isdir('.dev'): dirs.append('.dev')

    for i, d in enumerate(dirs):
        is_last = (i == len(dirs) - 1)
        char, child_prefix = ('└──', '    ') if is_last else ('├──', '│   ')
        readme_path = os.path.join(d, "README.md").replace(os.sep, '/')
        link = f"[{d}/]({readme_path})" if os.path.exists(readme_path) else f"{d}/"
        sitemap.append('│<br>')
        sitemap.append(f'{char} 📁 {link}<br>')
        sitemap.extend(generate_sitemap_recursive_br(d, child_prefix))

    return '\n'.join(sitemap)

# --- Main Execution Block ---

if __name__ == '__main__':
    print("--- Maintenance du Business Plan ---")

    files_to_process = []
    for root, dirs, files in os.walk('.', topdown=True):
        dirs[:] = [d for d in dirs if d not in ['.git', '.scripts', 'node_modules']]
        for file in sorted(files):
            if file.endswith('.md') and 'sitemap' not in file.lower():
                files_to_process.append(os.path.join(root, file))

    print(f"\nÉtape 1: Renumérotation et mise à jour des TOC de {len(files_to_process)} fichiers...")
    for path in files_to_process:
        print(f"  - Traitement de : {path}")
        update_file_content(path)
    print("✅ Traitement des fichiers terminé.")

    sitemap_filename = 'SiteMap.md'
    print(f"\nÉtape 2: Génération du Sitemap final : {sitemap_filename}...")
    sitemap_content = build_sitemap_br(sitemap_filename)
    with open(sitemap_filename, 'w', encoding='utf-8') as f: f.write(sitemap_content)
    print(f"✅ {sitemap_filename} généré.")

    print("\n--- Maintenance terminée ---")
