import os
import re
from pathlib import Path

class DocumentationAgent:
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
        # On itère sur les dossiers parents
        for i, part in enumerate(relative_path.parts[:-1]):
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
            
        if self.TOC_START not in content:
            # Insertion intelligente (après H1 ou avant H2)
            match = re.search(r'^##\s', content, re.MULTILINE)
            if match:
                insertion_point = match.start()
                content = content[:insertion_point] + f"{self.TOC_START}\n{self.TOC_END}\n\n" + content[insertion_point:]
            else:
                match_h1 = re.search(r'^#\s.+', content, re.MULTILINE)
                if match_h1:
                    end_of_h1 = match_h1.end()
                    next_para = content.find('\n\n', end_of_h1)
                    insertion_point = next_para + 2 if next_para != -1 else len(content)
                    content = content[:insertion_point] + f"\n\n{self.TOC_START}\n{self.TOC_END}\n\n" + content[insertion_point:]

        # 2. Update Breadcrumbs
        breadcrumb_text = self.generate_breadcrumb(file_path, root_path)
        content = re.sub(
            f"({re.escape(self.BREADCRUMB_START)})(.*?)({re.escape(self.BREADCRUMB_END)})",
            f"\\1\n{breadcrumb_text}\n\\3",
            content,
            flags=re.DOTALL
        )

        # 3. Update TOC
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
        root_path = Path(root_path).resolve()
        
        for md_file in root_path.rglob('*.md'):
            parts = md_file.relative_to(root_path).parts
            # Vérification via la liste d'exclusion définie dans __init__
            if any(part in self.ignored_folders for part in parts):
                continue
                
            try:
                with open(md_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                errors.append(f"⚠️ Erreur lecture {md_file.name}: {e}")
                continue
                
            lines = content.splitlines()
            in_code_block = False
            
            for line_num, line in enumerate(lines, 1):
                if line.strip().startswith('```'):
                    in_code_block = not in_code_block
                    continue
                
                if in_code_block:
                    continue

                # Regex pour capturer les URLs dans [texte](url)
                links = re.findall(r'\]\(([^)]+)\)', line)
                
                for link in links:
                    link = link.strip()
                    # Ignorer les liens externes, ancres pures, mailto, ou variables simples
                    if link.startswith('http') or link.startswith('#') or link.startswith('mailto:') or '{' in link:
                        continue
                    
                    # Gestion des ancres dans les fichiers (ex: fichier.md#section)
                    file_part = link
                    if '#' in link:
                        file_part = link.split('#')[0]
                    
                    if not file_part: # Cas du lien vide ou juste #
                        continue
                        
                    target_path = (md_file.parent / file_part).resolve()
                    
                    if not target_path.exists():
                        errors.append(f"❌ {md_file.relative_to(root_path)}:L{line_num} pointe vers INEXISTANT: '{link}'")

        if errors:
            print(f"[{self.name}] Rapport: {len(errors)} erreurs trouvées.")
            for e in errors:
                print(e)
        else:
            print(f"[{self.name}] ✅ Tous les liens relatifs vérifiés sont valides.")

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
