import os
import re
from pathlib import Path

class Documentation:
    def __init__(self):
        self.name = "Agent Documentation (Auto-Update)"
        # Balises
        self.BREADCRUMB_START = '<!-- BREADCRUMB START -->'
        self.BREADCRUMB_END = '<!-- BREADCRUMB END -->'
        self.TOC_START = '<!-- TOC START -->'
        self.TOC_END = '<!-- TOC END -->'
        
        # Ignorer SEULEMENT les dossiers systèmes strictement nécessaires
        self.ignored_folders = {'.git', '__pycache__'}

    def get_document_title(self, md_file_path):
        """Extracts the H1 title from the markdown file."""
        if not md_file_path.exists():
            return None
        try:
            with open(md_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith('# '):
                        return line[2:].strip()
        except Exception:
            pass
        return None

    def generate_breadcrumb(self, file_path, root_path):
        if file_path == root_path / 'README.md':
            return "" # Pas de breadcrumb sur la root
            
        try:
            relative_path = file_path.relative_to(root_path)
        except ValueError:
            return "" 

        depth = len(relative_path.parts) - 1
        # Si depth = 0 (racine), on veut quand même le lien vers la maison (README.md)
        # sauf si c'est déjà le README.md (géré au tout début de la fonction)

        root_link = os.path.join(*(['..'] * depth), 'README.md')
        
        breadcrumbs = [f'[🏠]({root_link})']
        
        current_path = root_path
        # On itère sur les dossiers parents. 
        # Si c'est un README.md, on s'arrête au dossier parent du dossier actuel (parts[:-2])
        # Sinon, on s'arrête au dossier parent du fichier (parts[:-1])
        parts_to_iterate = relative_path.parts[:-2] if file_path.name == 'README.md' else relative_path.parts[:-1]
        
        for i, part in enumerate(parts_to_iterate):
            current_path = current_path / part
            readme_path = current_path / 'README.md'
            
            # Reconstruction du lien relatif
            # CORRECTION : On ne redescend pas dans 'part', on remonte juste le bon nombre de fois
            # Si on est à profondeur 3, pour aller au parent (i=1), on remonte 1 fois (../)
            # Formule : depth - i - 1 remontees
            up_steps = depth - i - 1
            if up_steps == 0:
                link_target = 'README.md'
            else:
                link_target = os.path.join(*(['..'] * up_steps), 'README.md')
            
            title = self.get_document_title(readme_path)
            if not title:
                title = f"📂 {part}"
            
            breadcrumbs.append(f'[{title}]({link_target})')
            
        return ' > '.join(breadcrumbs)

    def create_anchor(self, title):
        anchor = title.lower()
        anchor = re.sub(r'[^\w\s-]', '', anchor) 
        anchor = re.sub(r'\s+', '-', anchor)
        return anchor.strip('-')

    def generate_toc(self, content):
        toc = []
        in_code_block = False
        
        lines = content.splitlines()
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if in_code_block:
                continue
                
            match = re.match(r'^(##|###)\s+(.+)', line)
            if match:
                level, title = match.groups()
                anchor = self.create_anchor(title)
                indent = "  " if level == '###' else ""
                toc.append(f"{indent}- [{title.strip()}](#{anchor})")
                
        if toc:
            return "## 📖 Table des Matières\n\n" + '\n'.join(toc)
        return ""

    def update_markdown_file(self, file_path, root_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"[{self.name}] ⚠️ Erreur lecture {file_path}: {e}")
            return False

        original_content = content
        
        # 1. Ensure Tags Exist
        if self.BREADCRUMB_START not in content:
            content = f"{self.BREADCRUMB_START}\n{self.BREADCRUMB_END}\n\n" + content
            
        # 2. Ensure H1 exists
        has_h1 = False
        in_code_block = False
        for line in content.splitlines():
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if not in_code_block and line.startswith('# '):
                has_h1 = True
                break
        
        if not has_h1:
            if file_path.name == 'README.md':
                title = file_path.parent.name.replace('-', ' ').replace('_', ' ').capitalize()
            else:
                title = file_path.stem.replace('-', ' ').replace('_', ' ').capitalize()
            
            match_breadcrumb = re.search(f"{re.escape(self.BREADCRUMB_END)}", content)
            if match_breadcrumb:
                insertion_point = match_breadcrumb.end()
                content = content[:insertion_point] + f"\n\n# {title}\n" + content[insertion_point:]
            else:
                content = f"# {title}\n\n" + content
            print(f"[{self.name}] 🆕 Ajout H1 manquant : '# {title}' dans {file_path.relative_to(root_path)}")

        # 3. Ensure TOC Tags Exist
        if self.TOC_START not in content:
            match_h1 = re.search(r'^#\s.+', content, re.MULTILINE)
            if match_h1:
                end_of_h1 = match_h1.end()
                next_para = content.find('\n\n', end_of_h1)
                insertion_point = next_para + 2 if next_para != -1 else len(content)
                content = content[:insertion_point] + f"{self.TOC_START}\n{self.TOC_END}\n\n" + content[insertion_point:]
            else:
                match_h2 = re.search(r'^##\s', content, re.MULTILINE)
                if match_h2:
                    insertion_point = match_h2.start()
                    content = content[:insertion_point] + f"{self.TOC_START}\n{self.TOC_END}\n\n" + content[insertion_point:]

        # 4. Auto-link Key Directories
        target_dirs = ['Documents', 'Annexes', 'Sources', '.dev']
        try:
            rel_to_root = file_path.parent.relative_to(root_path)
            depth = len(rel_to_root.parts)
        except ValueError:
            depth = 0
        up_prefix = os.path.join(*(['..'] * depth)) if depth > 0 else '.'
        
        for dir_name in target_dirs:
            pattern = rf'(?<![\[/\w.])(`?){re.escape(dir_name)}/\1(?![\]\w./])'
            
            def replace_with_link(match):
                ticks = match.group(1) or ""
                link_target = os.path.normpath(os.path.join(up_prefix, dir_name, 'README.md'))
                return f"[{ticks}{dir_name}/{ticks}]({link_target})"
            
            content = re.sub(pattern, replace_with_link, content)

        # 5. Update Breadcrumbs (renumbered)
        breadcrumb_text = self.generate_breadcrumb(file_path, root_path)
        content = re.sub(
            f"({re.escape(self.BREADCRUMB_START)})(.*?)({re.escape(self.BREADCRUMB_END)})",
            f"\\1\n{breadcrumb_text}\n\\3",
            content,
            flags=re.DOTALL
        )

        # 6. Update TOC (renumbered)
        toc_text = self.generate_toc(content)
        content = re.sub(
            f"({re.escape(self.TOC_START)})(.*?)({re.escape(self.TOC_END)})",
            f"\\1\n{toc_text}\n\\3",
            content,
            flags=re.DOTALL
        )

        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            # print(f"[{self.name}] ✅ Mis à jour : {file_path.relative_to(root_path)}")
            return True
        return False

    def verify_links(self, root_path):
        """Vérifie que tous les liens locaux dans les fichiers Markdown pointent vers des fichiers existants."""
        print(f"\n[{self.name}] 🕵️‍♂️ Vérification des liens (Audit)...")
        errors = []
        fixed_count = 0
        root_path = Path(root_path).resolve()
        
        target_dirs = ['Documents', 'Annexes', 'Sources', '.dev']
        
        for md_file in root_path.rglob('*.md'):
            parts = md_file.relative_to(root_path).parts
            if any(part in self.ignored_folders for part in parts):
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                errors.append(f"⚠️ Erreur lecture {md_file.name}: {e}")
                continue
            
            original_content = content
            lines = content.splitlines()
            new_lines = []
            in_code_block = False
            file_modified = False
            
            for line_num, line in enumerate(lines, 1):
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    new_lines.append(line)
                    continue
                
                if in_code_block:
                    new_lines.append(line)
                    continue

                # 1. Auto-FIX pour les casses de dossiers connus (ex: ./documents/ -> ./Documents/)
                # On ne fait ça que pour les vrais liens Markdown (pas ceux déjà entre ` `)
                for dir_name in target_dirs:
                    # Regex pour match [label](.../dir_lowercase/...)
                    # On ignore si c'est déjà la bonne casse
                    incorrect_casings = [dir_name.lower(), dir_name.upper()] if dir_name != '.dev' else []
                    if dir_name == 'Sources': incorrect_casings.append('SOURCE')
                    
                    for wrong_case in incorrect_casings:
                        if wrong_case == dir_name: continue
                        
                        # On cherche ](./wrong/ ou ](wrong/ ou ](../wrong/
                        # Mais on évite de casser les liens qui sont déjà parfaits
                        # On utilise une approche prudente
                        wrong_pattern = rf'(\]\()(\.\.?/)*{re.escape(wrong_case)}/'
                        if re.search(wrong_pattern, line):
                            line = re.sub(wrong_pattern, rf'\1\2{dir_name}/', line)
                            file_modified = True

                # 2. AUDIT: Regex pour capturer les URLs dans [texte](url)
                # On essaie d'ignorer les liens dans les backticks `[text](url)`
                # On cherche les liens qui ne sont pas précédés d'un backtick impair 
                # (Simplification: si le lien est entouré de backticks on l'ignore)
                
                links_with_context = re.finditer(r'(`)?(\[.*?\])\(([^)]+)\)\1', line)
                
                for match in links_with_context:
                    is_backticked = match.group(1) is not None
                    link = match.group(3).strip()

                    if is_backticked:
                        continue # C'est un exemple ou du code, on ignore l'audit
                        
                    if link.startswith('http') or link.startswith('#') or link.startswith('mailto:') or '{' in link:
                        continue
                    
                    file_part = link.split('#')[0] if '#' in link else link
                    if not file_part:
                        continue
                        
                    target_path = (md_file.parent / file_part).resolve()
                    if not target_path.exists():
                        errors.append(f"❌ {md_file.relative_to(root_path)}:L{line_num} pointe vers INEXISTANT: '{link}'")

                new_lines.append(line)

            if file_modified:
                try:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(new_lines))
                    fixed_count += 1
                    print(f"[{self.name}] 🔧 Auto-fix des liens dans {md_file.relative_to(root_path)}")
                except Exception as e:
                    print(f"[{self.name}] ⚠️ Erreur écriture auto-fix {md_file.name}: {e}")

        if fixed_count > 0:
            print(f"[{self.name}] 🛠 {fixed_count} fichiers ont été réparés automatiquement.")

        if errors:
            print(f"[{self.name}] Rapport: {len(errors)} erreurs de liens persistantes.")
            for e in errors:
                print(e)
        else:
            print(f"[{self.name}] ✅ Tous les liens relatifs ont été vérifiés et sont valides.")

    def run(self, root_path):
        print(f"\n[{self.name}] Vérification et mise à jour de la documentation...")
        root_path = Path(root_path).resolve()
        count_updated = 0
        
        for md_file in root_path.rglob('*.md'):
            # Ignorer les dossiers systèmes
            # On N'IGNORE PLUS .dev ICI pour répondre à la demande
            parts = md_file.relative_to(root_path).parts
            # Vérification via la liste d'exclusion définie dans __init__
            if any(part in self.ignored_folders for part in parts):
                continue
                
            if self.update_markdown_file(md_file, root_path):
                print(f"[{self.name}] ✅ Mis à jour : {md_file.relative_to(root_path)}")
                count_updated += 1
            else:
                # Log even if not updated to confirm it was checked
                # print(f"[{self.name}] ℹ️ Déjà à jour : {md_file.relative_to(root_path)}")
                pass
                
        if count_updated > 0:
            print(f"[{self.name}] {count_updated} fichiers mis à jour.")
        else:
            print(f"[{self.name}] Documentation déjà à jour.")
        
        # 3. Lancer l'audit des liens à la fin
        self.verify_links(root_path)
