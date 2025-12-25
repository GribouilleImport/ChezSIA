#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Ajout du dossier parent des agents au path pour import
# On est dans .dev/scripts/update_docs/script.py
# On veut atteindre .dev/agents
current_dir = Path(__file__).resolve().parent
dev_dir = current_dir.parent.parent # .dev
agents_dir = dev_dir / 'agents'
sys.path.append(str(agents_dir))

from documentation_agent.documentation_agent import DocumentationAgent

def main():
    project_root = dev_dir.parent
    
    # Instanciation et execution de l'agent
    agent = DocumentationAgent()
    agent.run(project_root)
    agent.verify_links(project_root)

if __name__ == "__main__":
    main()
