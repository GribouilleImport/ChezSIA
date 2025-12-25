import os
import sys

# Ajout du dossier parent (.dev/agents) au path pour pouvoir importer les autres agents
current_dir = os.path.dirname(os.path.abspath(__file__))
agents_dir = os.path.dirname(current_dir)
sys.path.append(agents_dir)

from coherence.agent import Coherence
from expert.agent import Expert
from readme.agent import Readme
from documentation.agent import Documentation

def main():
    print("=== Démarrage du Système Multi-Agents ChezSIA ===\n")
    
    # Chemins des fichiers. 
    # Nous sommes dans .dev/agents/orchestrator/main.py
    # Root est à 3 niveaux au-dessus de 'orchestrator' -> .dev -> agents -> orchestrator (Wait ?)
    # __file__ = .../.dev/agents/orchestrator/main.py
    # dir(1) = .../.dev/agents/orchestrator
    # dir(2) = .../.dev/agents
    # dir(3) = .../.dev
    # dir(4) = .../ (ROOT)
    
    # Verification simple: si agents_dir est ".../.dev/agents", dirname(agents_dir) est ".../.dev", dirname(...) est root.
    # Attends, agents_dir = .../.dev/agents
    # dirname(agents_dir) = .../.dev
    # dirname(dirname(agents_dir)) = .../ (ROOT)
    
    from pathlib import Path
    project_root = Path(agents_dir).parent.parent
    
    # 0. Agent Documentaliste : Vérification de la structure (Readme & Docs)
    librarian = Readme()
    librarian.run(str(project_root))
    
    doc_updater = Documentation()
    doc_updater.run(str(project_root))
    
    print("") # spacer
    
    rentabilite_file = project_root / 'Documents' / 'analyse_rentabilite_zero.md'
    previsionnel_file = project_root / 'Documents' / 'previsionnel_financier.md'
    
    print(f"Répertoire de base : {project_root}")
    print(f"Fichier Rentabilité : {rentabilite_file}")
    print(f"Fichier Prévisionnel : {previsionnel_file}")
    
    if not rentabilite_file.exists() or not previsionnel_file.exists():
        print("ERREUR : Impossible de trouver les fichiers Markdown.")
        # Fallback debug si path incorrect
        print(f"Debug: Current Dir: {os.getcwd()}")
        return

    # 1. L'Agent de Cohérence fait son travail (il utilise l'Agent Comptable en interne)
    auditor = Coherence()
    result = auditor.check_charges_fixes(rentabilite_file, previsionnel_file)
    
    # 2. L'Agent Expert donne son verdict
    daf = Expert()
    daf.generate_report(result)

if __name__ == "__main__":
    main()
