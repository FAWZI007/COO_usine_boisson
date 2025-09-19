# COO_usine_boisson 🏭

Projet académique de modélisation d'une usine de production de boissons utilisant les principes de la Conception Orientée Objets (COO).

## 📋 Description

Ce projet implémente un système complet de gestion d'une usine de production de boissons en utilisant les principes fondamentaux de la programmation orientée objet :

- **Abstraction** : Classes abstraites pour les boissons
- **Encapsulation** : Gestion des données privées dans les classes
- **Héritage** : Hiérarchie de classes pour les différents types de boissons
- **Polymorphisme** : Méthodes adaptées selon le type de boisson

## 🏗️ Architecture du Système

### Classes Principales

#### 🥤 Module `boisson.py`
- **`Ingredient`** : Représente un ingrédient avec nom, quantité et unité
- **`Boisson`** (abstraite) : Classe de base pour tous les types de boissons
- **`Eau`** : Boisson à base d'eau (plate ou gazeuse)
- **`Jus`** : Jus de fruits avec pourcentage de fruits
- **`Soda`** : Boisson gazeuse sucrée avec taux de sucre
- **`BoissonEnergisante`** : Boisson énergisante avec taux de caféine

#### 🏭 Module `usine.py`
- **`Stock`** : Gestion des ingrédients et alertes de stock
- **`EtapeProduction`** : Étape individuelle du processus de production
- **`ProcessusProduction`** : Séquence d'étapes pour un type de boisson
- **`LigneProduction`** : Ligne de production avec capacité et processus
- **`Usine`** : Classe principale gérant l'ensemble de la production

## 🚀 Utilisation

### Installation
```bash
git clone https://github.com/FAWZI007/COO_usine_boisson.git
cd COO_usine_boisson
```

### Exécution de la démonstration
```bash
python demonstration.py
```

### Exécution des tests
```bash
python tests.py
```

## 💡 Exemples d'utilisation

### Création d'une boisson
```python
from boisson import Eau, Ingredient

# Créer une eau gazeuse
eau_gazeuse = Eau(
    "Eau Pétillante",
    1.0,  # Volume en litres
    [
        Ingredient("eau", 0.98),
        Ingredient("minéraux", 0.02),
        Ingredient("co2", 0.005)
    ],
    est_gazeuse=True
)

# Calculer le coût de production
cout = eau_gazeuse.calculer_cout_production()
print(f"Coût de production: {cout:.2f}€")
```

### Configuration d'une usine
```python
from usine import Usine, LigneProduction, ProcessusProduction, EtapeProduction

# Créer une usine
usine = Usine("Usine Exemple")

# Créer un processus de production
etapes = [
    EtapeProduction("Préparation", 5),
    EtapeProduction("Mélange", 10),
    EtapeProduction("Embouteillage", 8)
]
processus = ProcessusProduction("Production Eau", etapes)

# Ajouter une ligne de production
ligne = LigneProduction("Ligne 1", 100, processus)
usine.ajouter_ligne_production(ligne)

# Initialiser le stock
usine.stock.ajouter_ingredient("eau", 1000.0, 50.0)
usine.stock.ajouter_ingredient("co2", 100.0, 10.0)
```

### Production d'une boisson
```python
# Produire la boisson
resultat = usine.produire_boisson(eau_gazeuse)

if resultat:
    print("✅ Production réussie!")
    print(usine.obtenir_rapport_production())
else:
    print("❌ Échec de la production")
```

## 🧪 Tests et Validation

Le projet inclut une suite complète de tests unitaires couvrant :

- ✅ Création et validation des ingrédients
- ✅ Fonctionnement de tous les types de boissons
- ✅ Gestion du stock et alertes
- ✅ Processus de production
- ✅ Lignes de production
- ✅ Fonctionnement global de l'usine

### Résultats des tests
```
Tests exécutés: 21
Échecs: 0
Erreurs: 0
✅ Tous les tests sont passés avec succès!
```

## 📊 Fonctionnalités

### Gestion des Boissons
- ✅ Validation automatique des ingrédients selon le type
- ✅ Calcul automatique du coût de production
- ✅ Traçabilité avec numéros de lot et dates de production

### Gestion de la Production
- ✅ Processus de production configurables par étapes
- ✅ Lignes de production avec capacités spécifiques
- ✅ Gestion automatique des numéros de lots

### Gestion du Stock
- ✅ Suivi en temps réel des quantités d'ingrédients
- ✅ Alertes automatiques pour les stocks faibles
- ✅ Vérification de disponibilité avant production

### Rapports et Statistiques
- ✅ Rapports détaillés de production
- ✅ Statistiques par type de boisson
- ✅ Historique de production par ligne

## 🎯 Objectifs Pédagogiques

Ce projet démontre :

1. **Conception Orientée Objet** : Utilisation appropriée des classes et méthodes
2. **Principes SOLID** : Respect des bonnes pratiques de développement
3. **Tests Unitaires** : Validation systématique du code
4. **Documentation** : Code bien documenté et lisible
5. **Modélisation Métier** : Représentation fidèle d'un système industriel

## 📁 Structure du Projet

```
COO_usine_boisson/
├── README.md              # Documentation principale
├── boisson.py            # Classes des boissons et ingrédients
├── usine.py              # Classes de l'usine et production
├── demonstration.py      # Script de démonstration
└── tests.py             # Tests unitaires
```

## 🏆 Résultats de la Démonstration

La démonstration produit avec succès 4 types de boissons différentes :

- 🌊 **Eau Cristalline Gazeuse** (0.60€) - Processus complet avec carbonatation
- 🍊 **Jus d'Orange 100% Pur** (2.10€) - 80% de fruits
- 🥤 **Cola Classic** (1.12€) - Soda avec 120g/L de sucre
- ⚡ **Energy Max** (1.16€) - 320mg/L de caféine

Chaque boisson est produite avec un numéro de lot unique et passe par toutes les étapes de production définies.

## 🔧 Extensibilité

Le système est conçu pour être facilement extensible :

- ➕ Nouveaux types de boissons par héritage
- ➕ Nouvelles étapes de production
- ➕ Nouvelles métriques et rapports
- ➕ Intégration avec des systèmes externes

## 📝 Licence

Projet académique à des fins éducatives.