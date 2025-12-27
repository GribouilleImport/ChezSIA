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
    Generates a GitHub-compatible anchor slug from a header title.
    Example: "2.1. Mon Titre" -> "21-mon-titre"
    """
    # 1. Nettoyer les éléments non désirés (emojis)
    clean_title = EMOJI_PATTERN.sub(r'', header_title).strip()

    # 2. Convertir en minuscules
    slug = clean_title.lower()

    # 3. Supprimer les points dans les numérotations (ex: "2.1." -> "21")
    #    et remplacer les espaces par des tirets
    slug = re.sub(r'\.', '', slug, count=10) # count pour gérer les numérotations multiples
    slug = slug.replace(' ', '-')

    # 4. Supprimer tous les caractères non-alphanumériques sauf les tirets
    slug = re.sub(r'[^\w-]', '', slug)

    return slug if slug else "section"

def get_headers(file_path):
    """Gets all H2-H5 headers from a file, preserving original titles and emojis."""
    headers = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'^(##+)\s+([\d\.]+)\s+(.*)', line)
            if match:
                level = len(match.group(1))
                number = match.group(2).strip()
                title = match.group(3).strip() # This has emojis
                if "Table des Matières" not in title:
                    headers.append({'level': level, 'title': f"{number} {title}"})
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
            if level == 1: level = 2 # Treat H1s as H2s for numbering
            if 2 <= level <= 5 and not toc_header_pattern.search(line):
                # This regex now correctly captures the entire title after the numbering
                title_match = re.match(r'^(#+)\s*[\d\.]*\s*(.*)', line)
                raw_title = title_match.group(2).strip() if title_match and title_match.group(2) else line.strip('# \n')

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

def format_header_tree_br(tree, prefix, file_path):
    lines = []
    for i, node in enumerate(tree):
        is_last = (i == len(tree) - 1)

        try:
            # Séparer le numéro du titre. Ex: "1. Titre" -> "1.", "Titre"
            number_part, title = node['title'].split(' ', 1)
            # Formatter le numéro. Ex: "1." -> "1)", "2.1." -> "2.1)"
            number = number_part.strip('.') + ')'
        except ValueError:
            number = ""
            title = node['title']

        # Définir le séparateur en fonction du niveau de l'en-tête
        level = node['level']
        if level == 2:
            separator = '-----'
        elif level == 3:
            separator = '---'
        elif level == 4:
            separator = '-'
        else:
            separator = ''

        # Espacement constant pour l'alignement
        padding = '   '

        # Choisir le bon caractère d'arborescence
        char = '└─ ' if is_last else '├─ '

        # Générer le lien d'ancre
        anchor = slugify(node['title'])
        link = f"[{title}]({file_path}#{anchor})"

        # Assembler la ligne finale
        if separator:
            lines.append(f"{prefix}{char}{number} {separator}{padding}{link}<br>")
        else:
            # Gérer les niveaux plus profonds sans séparateur
            lines.append(f"{prefix}{char}{number}{padding}{link}<br>")

        # Définir le préfixe pour les enfants
        child_prefix = prefix + ('    ' if is_last else '│   ')
        if node['children']:
             lines.extend(format_header_tree_br(node['children'], child_prefix, file_path))

    return lines

def generate_sitemap_recursive_br(root, prefix=''):
    lines = []
    items = sorted(os.listdir(root))
    dirs = [i for i in items if os.path.isdir(os.path.join(root, i)) and i not in ['node_modules']]
    files = [i for i in items if i.endswith('.md') and i.lower() != 'readme.md']

    all_items = dirs + files
    for i, item_name in enumerate(all_items):
        is_last = (i == len(all_items) - 1)
        item_path = os.path.join(root, item_name)
        char = '└─ ' if is_last else '├─ '
        child_prefix = prefix + ('    ' if is_last else '│   ')

        if os.path.isdir(item_path):
            readme_path = os.path.join(item_path, "README.md").replace(os.sep, '/')
            link = f"[{item_name}/]({readme_path})" if os.path.exists(readme_path) else f"{item_name}/"
            lines.append(f'{prefix}{char}📁 {link}<br>')
            lines.extend(generate_sitemap_recursive_br(item_path, child_prefix))
        else: # is a file
            rel_path = os.path.relpath(item_path, '.').replace(os.sep, '/')
            with open(item_path, 'r', encoding='utf-8') as h1_f:
                h1 = re.search(r'^#\s+(.*)', h1_f.read(), re.MULTILINE)
                # Remove emojis only for the sitemap display, not from the file
                if h1:
                    title_content = h1.group(1).strip().upper()
                else:
                    title_content = item_name
                title = EMOJI_PATTERN.sub(r'', title_content).strip()
            lines.append(f'{prefix}{char}[{title}]({rel_path})<br>')

            headers = get_headers(item_path)
            if headers:
                # Clean emojis just for the sitemap display
                cleaned_headers = [{'level': h['level'], 'title': EMOJI_PATTERN.sub(r'', h['title']).strip()} for h in headers]
                max_num_len = 0
                for h in cleaned_headers:
                    try:
                        number = h['title'].split(' ', 1)[0]
                        number = number.strip('.') + '.'
                        if len(number) > max_num_len: max_num_len = len(number)
                    except (ValueError, IndexError): continue
                tree = build_header_tree_br(cleaned_headers)
                lines.extend(format_header_tree_br(tree, child_prefix, rel_path))

        if not is_last:
            lines.append(f'{prefix}│<br>')

    return lines

def build_sitemap_br():
    sitemap = [f'# 📂 SiteMap - ChezSIA', '> **Dernière mise à jour :** Généré automatiquement', '> **Structure :** Arborescence complète du Business Plan', '---', 'ChezSIA/<br>']

    # Custom sort order for directories
    order = ['Documents', 'Annexes', 'Sources']
    all_dirs = [d for d in os.listdir('.') if os.path.isdir(d) and d not in ['.git', '.scripts', 'node_modules']]
    ordered_dirs = [d for d in order if d in all_dirs]
    dev_dir = [d for d in all_dirs if d == '.dev']
    other_dirs = sorted([d for d in all_dirs if d not in order and d != '.dev'])
    dirs = ordered_dirs + other_dirs + dev_dir

    if dirs:
        sitemap.append('│<br>')

    for i, d in enumerate(dirs):
        is_last = (i == len(dirs) - 1)
        char, child_prefix = ('└─ ', '    ') if is_last else ('├─ ', '│   ')
        readme_path = os.path.join(d, "README.md").replace(os.sep, '/')
        link = f"[{d}/]({readme_path})" if os.path.exists(readme_path) else f"{d}/"
        sitemap.append(f'{char}📁 {link}<br>')
        sitemap.extend(generate_sitemap_recursive_br(d, child_prefix))

        if not is_last:
            sitemap.append('│<br>')

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
    sitemap_content = build_sitemap_br()
    with open(sitemap_filename, 'w', encoding='utf-8') as f: f.write(sitemap_content)
    print(f"✅ {sitemap_filename} généré.")

    print("\n--- Maintenance terminée ---")
