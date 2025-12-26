<!-- BREADCRUMB START -->

<!-- BREADCRUMB END -->

# Projet "ChezSIA" : Business Plan & Prévisionnel

Bienvenue sur l'espace de travail du projet de restaurant **ChezSIA**. Ce dépôt centralise l'ensemble des documents constituant le business plan, actuellement en phase de finalisation.

L'objectif est de fournir une vision claire et détaillée de la stratégie, des prévisions financières et des hypothèses opérationnelles pour vous et votre futur associé.

---

<!-- TOC START -->
- [1. 🎯 Indicateur Clé : Seuil de Rentabilité](#1-indicateur-cle-seuil-de-rentabilite)
- [2. 📂 Navigation dans le Projet](#2-navigation-dans-le-projet)
  - [2.1. Documents Financiers Clés](#21-documents-financiers-cles)
  - [2.2. Annexes : Charges & Aides](#22-annexes-charges-aides)
  - [2.3. Source & Inspiration](#23-source-inspiration)
- [3. 🗺️ SiteMap & Maintenance](#3-sitemap-maintenance)
<!-- TOC END -->

## 1. 🎯 Indicateur Clé : Seuil de Rentabilité

L'un des chiffres les plus importants de notre analyse est le point d'équilibre, qui nous indique le niveau d'activité minimum pour être rentable.

> **~ 22 couverts par jour**

Ce chiffre, bien inférieur à nos prévisions de fréquentation, confirme la marge de sécurité et la viabilité du projet. Pour le détail du calcul, consultez le document sur l'[Analyse de Rentabilité](./Documents/analyse_rentabilite_zero.md).

---

## 2. 📂 Navigation dans le Projet

Ce `README.md` sert de porte d'entrée. Voici la description de chaque document pour vous guider :

### 2.1. Documents Financiers Clés

*   **[📄 Prévisionnel Financier](./Documents/previsionnel_financier.md)**
    *   **Description :** C'est le cœur du business plan. Il détaille sur 2 ans les hypothèses d'activité (fréquentation, ticket moyen) et présente le compte de résultat prévisionnel.
    *   **À consulter pour :** Avoir une vue d'ensemble des revenus et des charges attendus.

*   **[📊 Plan de Trésorerie](./Documents/plan_tresorerie.md)**
    *   **Description :** Simule les flux de trésorerie mois par mois (encaissements et décaissements TTC) pour s'assurer de la liquidité de l'entreprise.
    *   **À consulter pour :** Valider la viabilité financière et anticiper les besoins de trésorerie.

*   **[📈 Analyse de la Rentabilité (Point d'Équilibre)](./Documents/analyse_rentabilite_zero.md)**
    *   **Description :** Calcule le chiffre d'affaires minimum à atteindre pour pourvoir toutes les charges. C'est de ce document que provient l'indicateur clé de **22 couverts/jour**.
    *   **À consulter pour :** Comprendre le niveau de risque du projet.

### 2.2. Annexes : Charges & Aides

*   **[👥 Coûts du Personnel et Stratégie](./Annexes/estimation_charges_salaires.md)**
    *   **Description :** Explique la stratégie de gestion du personnel (équipe fixe de 3 CDI) et le coût mensuel associé.
    *   **À consulter pour :** Comprendre la gestion de la masse salariale.

*   **[🧾 Calcul Détaillé des Charges Sociales](./Annexes/estimation_charges_salaires.md#11-du-net-au-brut)**
    *   **Description :** Annexe technique qui détaille le calcul des charges pour un salarié au SMIC Hôtelier.
    *   **À consulter pour :** Justifier les chiffres utilisés dans le prévisionnel.

*   **[💡 Fiche sur l'Aide ACRE](./Annexes/estimation_charges_salaires.md#3-poste-dirigeant-président-de-sasu---1500-net-mensuel)**
    *   **Description :** Document informatif sur l'exonération de charges sociales pour le créateur d'entreprise (ACRE).
    *   **À consulter pour :** Optimiser la rémunération du dirigeant la première année.

### 2.3. Source & Inspiration

*   **[🧠 Discussion Stratégique (Notes Brutes)](./Sources/20251223_echange_alicia.md)**
    *   **Description :** Retranscription de la discussion stratégique qui a servi de base à de nombreuses hypothèses (carte, ticket moyen, leviers de rentabilité).
    *   **À consulter pour :** Comprendre l'origine de la vision et des objectifs du projet.

---

## 3. 🗺️ SiteMap & Maintenance

Un **[🗺️ SiteMap complet](./SiteMap.md)** du projet est disponible à la racine de ce dépôt pour une navigation rapide et hiérarchique.

> [!IMPORTANT]
> Ce SiteMap est généré automatiquement. Si vous modifiez, ajoutez ou supprimez des documents ou des titres, vous devez le mettre à jour en exécutant la commande suivante depuis la racine du projet :
> ```bash
> python .dev/scripts/generate_sitemap.py
> ```
