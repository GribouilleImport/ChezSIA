import os

class ReadmeAgent:
    def __init__(self):
        self.name = "Agent Documentaliste (ReadmeGenerator)"
        self.ignored_folders = {'.git', '__pycache__', '.idea', '.vscode'}

    def generate_default_content(self, folder_name, files, subdirs):
        """génère le contenu Markdown par défaut."""
        content = []
        content.append(f"# 📂 {folder_name}\n")
        content.append("Bienvenue dans ce dossier. Voici un aperçu de son contenu.\n")
        
        content.append("## 📄 Contenu\n")
        content.append("| Nom | Type |")
        content.append("| :--- | :--- |")
        
        for d in sorted(subdirs):
            content.append(f"| **[{d}](./{d}/README.md)** | 📁 Dossier |")
            
        for f in sorted(files):
            if f == "README.md": continue
            content.append(f"| [{f}](./{f}) | 📄 Fichier |")
            
        content.append("\n> [!NOTE]")
        content.append("> Ce fichier a été généré automatiquement par le **ReadmeAgent** car il était manquant.")
        content.append("> N'hésitez pas à l'éditer pour ajouter une description plus détaillée !")
        
        return "\n".join(content)

    def process_directory(self, dir_path):
        """Vérifie si un README existe, sinon le crée."""
        readme_path = os.path.join(dir_path, "README.md")
        
        if os.path.exists(readme_path):
            return False, "Existant"

        # List contents
        try:
            items = os.listdir(dir_path)
        except PermissionError:
            return False, "Accès Refusé"

        files = [i for i in items if os.path.isfile(os.path.join(dir_path, i))]
        subdirs = [i for i in items if os.path.isdir(os.path.join(dir_path, i)) and i not in self.ignored_folders]
        
        # Generation
        folder_name = os.path.basename(dir_path)
        if not folder_name: # Root case
            folder_name = "Racine du Projet"
            
        content = self.generate_default_content(folder_name, files, subdirs)
        
        try:
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True, "Généré"
        except Exception as e:
            return False, f"Erreur: {e}"

    def run(self, root_path):
        print(f"\n[{self.name}] Scan des dossiers en cours...")
        count_created = 0
        
        for dirpath, dirnames, filenames in os.walk(root_path):
            # Filtrage des dossiers ignorés in-place pour os.walk
            dirnames[:] = [d for d in dirnames if d not in self.ignored_folders]
            
            created, status = self.process_directory(dirpath)
            if created:
                rel_path = os.path.relpath(dirpath, root_path)
                print(f"[{self.name}] ✅ README créé pour : {rel_path}")
                count_created += 1
                
        if count_created == 0:
            print(f"[{self.name}] Tout est en ordre. Aucun README manquant.")
        else:
            print(f"[{self.name}] Terminé. {count_created} fichiers README ont été créés.")
