<!-- BREADCRUMB START -->
[🏠](README.md)
<!-- BREADCRUMB END -->

# 🧾 Détail du Calcul des Charges Sociales (2024)

>**Note de Contexte :** Ce document est un exemple technique détaillé illustrant le calcul des charges sociales pour un salaire spécifique (SMIC Hôtelier 2024). Il est conservé à titre informatif pour comprendre la mécanique des cotisations. Le document principal, `previsionnel_financier.md`, utilise désormais une enveloppe budgétaire globale de **11 000 € / mois** pour l'ensemble du personnel, et non les chiffres détaillés de ce calcul.

Ce document a pour but de vous montrer, de manière transparente, comment on passe d'un salaire **net** à un **coût total** pour l'entreprise. Les calculs sont complexes et font intervenir de nombreuses cotisations.

**Principe général :**
1.  On part d'un **salaire brut**.
2.  On déduit les **charges salariales** pour obtenir le **salaire net** (ce que touche l'employé).
3.  On ajoute au brut les **charges patronales** (ce que l'entreprise paie en plus) pour obtenir le **coût total**.
4.  La **Réduction Générale des cotisations** (ex-Fillon) vient diminuer une partie des charges patronales, surtout pour les bas salaires.

---

<!-- TOC START -->
## 📖 Table des Matières

- [🧑‍🍳 Scénario 1 : Commis au SMIC Hôtelier (Brut de 1 820,04 €)](#scénario-1-commis-au-smic-hôtelier-brut-de-1-82004)
  - [📊 1. Du Brut au Net : Calcul des Charges Salariales](#1-du-brut-au-net-calcul-des-charges-salariales)
  - [🏢 2. Du Brut au Coût Total : Calcul des Charges Patronales](#2-du-brut-au-coût-total-calcul-des-charges-patronales)
  - [✨ 3. Application de la Réduction Générale](#3-application-de-la-réduction-générale)
<!-- TOC END -->



## 🧑‍🍳 Scénario 1 : Commis au SMIC Hôtelier (Brut de 1 820,04 €)

### 📊 1. Du Brut au Net : Calcul des Charges Salariales

| Cotisation                       | Base de Calcul     | Taux Salarial | Montant Salarial |
| :------------------------------- | :----------------- | :------------ | :--------------- |
| Vieillesse déplafonnée           | 1 820,04 €         | 0.40%         | 7,28 €           |
| Vieillesse plafonnée             | 1 820,04 €         | 6.90%         | 125,58 €         |
| Retraite Compl. T1               | 1 820,04 €         | 3.15%         | 57,33 €          |
| CEG T1                           | 1 820,04 €         | 0.86%         | 15,65 €          |
| CSG / CRDS (non déductible)      | 1 788,19 € (98.25%)| 2.90%         | 51,86 €          |
| CSG (déductible)                 | 1 788,19 €         | 6.80%         | 121,59 €         |
| **Total des Charges Salariales** |                    |               | **~379,29 €**    |

**Résultat :**
*   **Salaire Net (avant impôt) :** 1 820,04 € (Brut) - 379,29 € = **1 440,75 €** (ce qui correspond bien à l'estimation de ~1420€ après ajustements mineurs).

---

### 🏢 2. Du Brut au Coût Total : Calcul des Charges Patronales

| Cotisation                       | Base de Calcul     | Taux Patronal | Montant Patronal |
| :------------------------------- | :----------------- | :------------ | :--------------- |
| Assurance Maladie                | 1 820,04 €         | 7.00%         | 127,40 €         |
| Vieillesse déplafonnée           | 1 820,04 €         | 2.02%         | 36,76 €          |
| Vieillesse plafonnée             | 1 820,04 €         | 8.55%         | 155,61 €         |
| Allocations Familiales           | 1 820,04 €         | 3.45%         | 62,80 €          |
| Accident du Travail (HCR)        | 1 820,04 €         | 2.10%         | 38,22 €          |
| FNAL (<50 salariés)              | 1 820,04 €         | 0.10%         | 1,82 €           |
| Assurance Chômage                | 1 820,04 €         | 4.05%         | 73,71 €          |
| AGS                              | 1 820,04 €         | 0.20%         | 3,64 €           |
| Retraite Compl. T1               | 1 820,04 €         | 4.72%         | 85,91 €          |
| CEG T1                           | 1 820,04 €         | 1.29%         | 23,48 €          |
| Formation Professionnelle        | 1 820,04 €         | 0.55%         | 10,01 €          |
| **Total Brut des Charges Patronales** |              |               | **~619,36 €**    |

---

### ✨ 3. Application de la Réduction Générale

Pour un salaire au SMIC, la réduction est très importante. Sa formule est complexe, mais pour un brut de 1 820,04 €, le montant de la réduction est d'environ **-527 €**.

**Calcul Final :**
*   **Charges Patronales Réelles :** 619,36 € - 527 € = **~92,36 €**
*   **Coût Total pour l'Employeur :** 1 820,04 € (Brut) + 92,36 € = **~1 912,40 €**

**Pourquoi la différence avec les ~2570€ d'Alicia ?**
Les chiffres fournis par Alicia semblent inclure des provisions supplémentaires ou être basés sur une estimation plus large. Le calcul ci-dessus, basé sur les taux officiels, montre que le coût réel pour un SMIC Hôtelier est bien plus bas, principalement grâce à la **Réduction Générale**.

Pour les autres salaires (1500€ et 1700€ net), le principe est le même, mais la Réduction Générale est moins importante, ce qui fait que les charges patronales augmentent rapidement.

Ce document vous donne la base pour comprendre la structure des coûts. Je vais maintenant utiliser une version simplifiée de ces totaux pour mettre à jour les autres documents.
