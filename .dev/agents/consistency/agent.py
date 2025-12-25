import sys
import os

# Si exécuté via main.py, le path est déjà configuré.
# Si importé, on s'assure qu'on peut trouver les voisins si besoin, mais ici on suppose que main.py a fait le job ou que le package est bien structuré.
# Cependant, comme accounting_agent est maintenant dans un sous-dossier:
from accounting.agent import Accounting

class Consistency:
    def __init__(self):
        self.name = "Agent de Cohérence"
        self.accountant = Accounting()

    def check_charges_fixes(self, rentabilite_path, previsionnel_path):
        """
        Vérifie si le total des charges fixes correspond entre les deux fichiers.
        """
        print(f"\n[{self.name}] Démarrage de la vérification de cohérence...")
        
        # Extraction Rentabilité
        renta_data = self.accountant.parse_markdown_table(rentabilite_path)
        total_renta_an1 = 0
        
        # On cherche la ligne TOTAL dans analyse_rentabilite_zero.md
        # Le format est | Total | ... | 129 768 € | ... 
        # (Basé sur la lecture précédente du fichier)
        for row in renta_data:
            # Les clés dépendent du header exact du fichier. 
            # Dans analyse_rentabilite_zero.md: "Poste de Dépense", "Coût Mensuel (An 1)", "Coût Annuel (An 1)"...
            if "TOTAL" in row.get("Poste de Dépense", "").upper():
                total_renta_str = row.get("Coût Annuel (An 1)", "0")
                total_renta_an1 = self.accountant.extract_numeric(total_renta_str)
                break
        
        # Extraction Prévisionnel
        # Dans previsionnel_financier.md, section 4 "Totaux annuels"
        prev_data = self.accountant.parse_markdown_table(previsionnel_path)
        total_prev_an1 = 0
        
        for row in prev_data:
            # Clés: Année, Charges fixes cash
            if "Année 1" in row.get("Année", ""):
                # Attention: Charges fixes cash + Amortissements ?
                # "Charges fixes cash" = 119 316 €
                # "Amortissements" = 10 450 €
                # Total = 129 766 €
                
                charges_cash = self.accountant.extract_numeric(row.get("Charges fixes cash", "0"))
                amort = self.accountant.extract_numeric(row.get("Amortissements", "0"))
                total_prev_an1 = charges_cash + amort
                break

        print(f"[{self.name}] Total Charges An 1 (Rentabilité) : {total_renta_an1:,.2f}")
        print(f"[{self.name}] Total Charges An 1 (Prévisionnel) : {total_prev_an1:,.2f}")

        diff = abs(total_renta_an1 - total_prev_an1)
        if diff < 5.0: # Tolérance pour les arrondis
            return True, "COHÉRENT (Différence négligeable)"
        else:
            return False, f"INCOHÉRENT (Différence de {diff:,.2f} €)"
