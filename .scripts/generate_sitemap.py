#!/usr/bin/env python3

import os
import re

DIRECTORY_ORDER = ['Documents', 'Annexes', 'Sources']

def get_headers(file_path):
    """Extracts H2, H3, H4, H5 headers from a markdown file."""
    headers = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'^(##+)\s+(.*)', line) # Match ## or more
            if match:
                level = len(match.group(1))
                title = match.group(2).strip()
                headers.append({'level': level, 'title': title})
    return headers

def build_header_tree(headers):
    """Builds a tree structure from a flat list of headers."""
    # Dummy root node at level 1 to be the parent of all H2s
    root = {'level': 1, 'children': []}
    # This list acts as a stack to keep track of the parent at each level
    parent_stack = [root]

    for header in headers:
        level = header['level']
        new_node = {'level': level, 'title': header['title'], 'children': []}

        # Pop from the stack until we find the direct parent
        while parent_stack[-1]['level'] >= level:
            parent_stack.pop()

        parent_stack[-1]['children'].append(new_node)
        parent_stack.append(new_node)

    return root['children']

def format_header_tree(tree, prefix):
    """Recursively formats the header tree into sitemap lines."""
    lines = []
    for i, node in enumerate(tree):
        is_last = (i == len(tree) - 1)
        tree_char = '└──' if is_last else '├──'
        lines.append(f"{prefix}{tree_char} {node['title']}")

        child_prefix = prefix + ('    ' if is_last else '│   ')
        lines.extend(format_header_tree(node['children'], child_prefix))

    return lines

def build_sitemap():
    """Builds the complete sitemap string."""
    root_dir = '.'
    sitemap = [
        '# 📂 SiteMap - ChezSIA',
        '> **Dernière mise à jour :** Généré automatiquement',
        '> **Structure :** Arborescence complète du Business Plan',
        '---',
        'ChezSIA/'
    ]

    # 1. Handle the root README.md
    root_readme = os.path.join(root_dir, 'README.md')
    if os.path.exists(root_readme):
        with open(root_readme, 'r', encoding='utf-8') as f:
            h1_match = re.search(r'^#\s+(.*)', f.read(), re.MULTILINE)
            readme_h1 = h1_match.group(1).strip() if h1_match else "README.md"
        sitemap.append('│')
        sitemap.append(f'├── [**{readme_h1}**](README.md)')

    # 2. Process directories
    all_dirs = [d for d in os.listdir(root_dir) if os.path.isdir(d) and not d.startswith('.')]

    # Sort directories according to the specified order
    sorted_dirs = [d for d in DIRECTORY_ORDER if d in all_dirs]
    other_dirs = sorted([d for d in all_dirs if d not in DIRECTORY_ORDER and d != '.dev'])
    sorted_dirs.extend(other_dirs)
    if os.path.isdir(os.path.join(root_dir, '.dev')):
        sorted_dirs.append('.dev')

    for i, dirname in enumerate(sorted_dirs):
        is_last_dir = (i == len(sorted_dirs) - 1)
        dir_prefix = '└──' if is_last_dir else '├──'
        sitemap.append('│')
        sitemap.append(f'{dir_prefix} 📁 {dirname}/')

        dir_path = os.path.join(root_dir, dirname)
        md_files = sorted([f for f in os.listdir(dir_path) if f.endswith('.md')])

        for j, filename in enumerate(md_files):
            is_last_file = (j == len(md_files) - 1)
            file_path = os.path.join(dir_path, filename)
            relative_path = os.path.join(dirname, filename)

            with open(file_path, 'r', encoding='utf-8') as f_h1:
                 h1_match = re.search(r'^#\s+(.*)', f_h1.read(), re.MULTILINE)
                 h1_title = h1_match.group(1).strip() if h1_match else filename

            dir_line_prefix = '    ' if is_last_dir else '│   '
            file_tree_prefix = '└──' if is_last_file else '├──'
            sitemap.append(f'{dir_line_prefix}{file_tree_prefix} [**{h1_title}**]({relative_path})')

            # Process H2, H3, ...
            headers = get_headers(file_path)
            header_tree = build_header_tree(headers)

            file_line_prefix = '    ' if is_last_file else '│   '
            header_base_prefix = dir_line_prefix + file_line_prefix

            sitemap.extend(format_header_tree(header_tree, header_base_prefix))

    return '\n'.join(sitemap)


if __name__ == '__main__':
    sitemap_content = build_sitemap()
    with open('SiteMap.md', 'w', encoding='utf-8') as f:
        f.write(sitemap_content)
    print("✅ SiteMap.md generated successfully.")
