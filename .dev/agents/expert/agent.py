class Expert:
    def __init__(self):
        self.name = "Agent Expert (DAF)"

    def generate_report(self, consistency_result):
        is_consistent, message = consistency_result
        
        print(f"\n--- RAPPORT FINAL DE L'{self.name.upper()} ---")
        print(f"Analyse du dossier 'ChezSIA' en cours...\n")
        
        if is_consistent:
            print("✅ CONCLUSION : Le dossier financier est COHÉRENT.")
            print("Les charges fixes identifiées dans le calcul du seuil de rentabilité sont parfaitement alignées avec le prévisionnel financier.")
            print("Recommandation : Le dossier est prêt à être présenté aux partenaires bancaires.")
            print("Points forts : Transparence des coûts salariaux et structure claire des coûts fixes.")
        else:
            print("⚠️ CONCLUSION : ATTENTION, INCOHÉRENCE DÉTECTÉE.")
            print(f"Détail : {message}")
            print("Recommandation : Ne pas présenter le dossier en l'état. Une révision des calculs d'amortissement ou des charges cash est nécessaire.")
            print("Il est probable qu'une charge ait été oubliée d'un côté ou comptée deux fois.")

        print("\n--- Fin de mission ---")
