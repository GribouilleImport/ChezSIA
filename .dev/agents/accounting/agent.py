import re

class Accounting:
    def __init__(self):
        self.name = "Agent Comptable"

    def parse_markdown_table(self, file_path):
        """
        Extrait les données des tableaux markdown d'un fichier.
        Retourne une liste de lignes (dictionnaires).
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except FileNotFoundError:
            print(f"[{self.name}] Erreur : Fichier non trouvé - {file_path}")
            return []

        # Regex simple pour trouver les lignes de tableau | ... |
        # On ignore la ligne de séparation |---|---|
        lines = content.split('\n')
        table_data = []
        headers = []

        for line in lines:
            if line.strip().startswith('|'):
                # Nettoyage de la ligne
                parts = [p.strip() for p in line.split('|') if p]  # Le split crée des chaines vides aux extrémités
                
                if not parts:
                    continue

                # Si c'est la ligne de séparation (---), on ignore
                if '---' in parts[0]:
                    continue

                if not headers:
                    headers = parts
                else:
                    # Création du dictionnaire pour la ligne
                    row_dict = {}
                    for i, header in enumerate(headers):
                        if i < len(parts):
                            row_dict[header] = parts[i]
                    table_data.append(row_dict)
            else:
                # Si on sort d'un tableau et qu'on en a déjà parsé un, on pourrait s'arrêter ou continuer
                # Pour cet exemple simple, on reset headers si on rencontre une ligne vide pour supporter plusieurs tableaux
                if not line.strip():
                    headers = []

        print(f"[{self.name}] Fichier '{file_path}' analysé : {len(table_data)} lignes de données trouvées.")
        return table_data

    def extract_numeric(self, value_str):
        """Convertit une chaine '10 000 €' en float 10000.0"""
        clean_str = re.sub(r'[^\d,\.-]', '', value_str).replace(' ', '').replace(',', '.')
        try:
            return float(clean_str)
        except ValueError:
            return 0.0

    def verify_previsionnel(self, file_path):
        """
        Vérifie spécifiquement le fichier previsionnel_financier.md
        """
        data = self.parse_markdown_table(file_path)
        report = []
        
        # Exemple de vérification : Somme des "Résultat exploitation A1"
        total_exploitation = 0.0
        calculated_exploitation = 0.0
        
        for row in data:
            # On cherche les lignes de mois (Jan, Fév...)
            if 'Mois' in row: 
                # C'est probablement le tableau mensuel
                try:
                    res_expl = self.extract_numeric(row.get('Résultat exploitation A1', '0'))
                    calculated_exploitation += res_expl
                except:
                    pass
            
            # On cherche la ligne TOTAL pour comparer
            if 'Total' in str(row.values()):
                 # Ceci est très simpliste et dépend du format exact
                 pass

        return data
