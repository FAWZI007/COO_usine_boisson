"""
Script de démonstration du modèle d'usine de production de boissons.
Illustre l'utilisation des différentes classes et fonctionnalités.
"""

from boisson import Boisson, Ingredient, Eau, Jus, Soda, BoissonEnergisante
from usine import Usine, LigneProduction, ProcessusProduction, EtapeProduction, Stock


def creer_etapes_production():
    """Crée les différentes étapes de production."""
    etapes = {
        'preparation': EtapeProduction("Préparation des ingrédients", 5, 
                                      "Mesure et préparation des ingrédients"),
        'melange': EtapeProduction("Mélange", 10, 
                                  "Mélange des ingrédients dans les proportions requises"),
        'carbonatation': EtapeProduction("Carbonatation", 15, 
                                        "Injection de CO2 pour les boissons gazeuses"),
        'filtrage': EtapeProduction("Filtrage", 8, 
                                   "Filtrage pour éliminer les impuretés"),
        'embouteillage': EtapeProduction("Embouteillage", 12, 
                                        "Mise en bouteille et capsulage"),
        'etiquetage': EtapeProduction("Étiquetage", 7, 
                                     "Application des étiquettes et codes-barres"),
        'controle_qualite': EtapeProduction("Contrôle qualité", 10, 
                                           "Vérification de la qualité du produit fini")
    }
    return etapes


def creer_processus_production():
    """Crée les différents processus de production selon le type de boisson."""
    etapes = creer_etapes_production()
    
    processus = {
        'eau': ProcessusProduction("Production d'eau", [
            etapes['preparation'],
            etapes['filtrage'],
            etapes['carbonatation'],  # Optionnelle selon le type d'eau
            etapes['embouteillage'],
            etapes['etiquetage'],
            etapes['controle_qualite']
        ]),
        
        'jus': ProcessusProduction("Production de jus", [
            etapes['preparation'],
            etapes['melange'],
            etapes['filtrage'],
            etapes['embouteillage'],
            etapes['etiquetage'],
            etapes['controle_qualite']
        ]),
        
        'soda': ProcessusProduction("Production de soda", [
            etapes['preparation'],
            etapes['melange'],
            etapes['carbonatation'],
            etapes['embouteillage'],
            etapes['etiquetage'],
            etapes['controle_qualite']
        ]),
        
        'energisante': ProcessusProduction("Production de boisson énergisante", [
            etapes['preparation'],
            etapes['melange'],
            etapes['carbonatation'],
            etapes['filtrage'],
            etapes['embouteillage'],
            etapes['etiquetage'],
            etapes['controle_qualite']
        ])
    }
    
    return processus


def initialiser_stock(usine: Usine):
    """Initialise le stock de l'usine avec des ingrédients de base."""
    ingredients_stock = [
        ("eau", 1000.0, 50.0),
        ("sucre", 500.0, 25.0),
        ("co2", 200.0, 10.0),
        ("fruits_pomme", 150.0, 15.0),
        ("fruits_orange", 120.0, 12.0),
        ("minéraux", 80.0, 8.0),
        ("cafeine", 50.0, 5.0),
        ("taurine", 30.0, 3.0),
        ("aromes_naturels", 100.0, 10.0),
        ("conservateurs", 60.0, 6.0)
    ]
    
    for nom, quantite, seuil in ingredients_stock:
        usine.stock.ajouter_ingredient(nom, quantite, seuil)
    
    print("Stock initialisé avec succès!")
    print(f"Ingrédients disponibles: {len(ingredients_stock)}")


def creer_exemples_boissons():
    """Crée des exemples de boissons de différents types."""
    boissons = []
    
    # Eau minérale gazeuse
    eau_gazeuse = Eau(
        "Eau Cristalline Gazeuse",
        1.0,
        [
            Ingredient("eau", 0.98),
            Ingredient("minéraux", 0.02),
            Ingredient("co2", 0.005)
        ],
        est_gazeuse=True
    )
    boissons.append(eau_gazeuse)
    
    # Jus d'orange
    jus_orange = Jus(
        "Jus d'Orange 100% Pur",
        1.0,
        [
            Ingredient("fruits_orange", 0.8),
            Ingredient("eau", 0.2)
        ],
        pourcentage_fruits=80.0
    )
    boissons.append(jus_orange)
    
    # Soda cola
    soda_cola = Soda(
        "Cola Classic",
        1.0,
        [
            Ingredient("eau", 0.85),
            Ingredient("sucre", 0.12),
            Ingredient("co2", 0.008),
            Ingredient("aromes_naturels", 0.022)
        ],
        taux_sucre=120.0
    )
    boissons.append(soda_cola)
    
    # Boisson énergisante
    boisson_energie = BoissonEnergisante(
        "Energy Max",
        0.5,
        [
            Ingredient("eau", 0.4),
            Ingredient("sucre", 0.06),
            Ingredient("cafeine", 0.0008),
            Ingredient("taurine", 0.002),
            Ingredient("co2", 0.004),
            Ingredient("aromes_naturels", 0.0332)
        ],
        taux_cafeine=320.0
    )
    boissons.append(boisson_energie)
    
    return boissons


def demonstrer_production(usine: Usine, boissons: list):
    """Démontre le processus de production de l'usine."""
    print("\n" + "="*60)
    print("DÉMONSTRATION DE LA PRODUCTION")
    print("="*60)
    
    for i, boisson in enumerate(boissons, 1):
        print(f"\n--- Production {i}: {boisson.nom} ---")
        
        # Vérifier la validité des ingrédients
        if boisson.valider_ingredients():
            print("✅ Ingrédients validés")
        else:
            print("❌ Ingrédients non valides")
            continue
        
        # Calculer le coût de production
        cout = boisson.calculer_cout_production()
        print(f"💰 Coût de production estimé: {cout:.2f}€")
        
        # Tenter la production
        print("\n🏭 Démarrage de la production...")
        resultat = usine.produire_boisson(boisson)
        
        if resultat:
            print("✅ Production réussie!")
        else:
            print("❌ Échec de la production")
        
        print("\n" + "-"*40)


def main():
    """Fonction principale de démonstration."""
    print("🏭 SYSTÈME DE GESTION D'USINE DE BOISSONS")
    print("Modélisation orientée objet d'une usine de production")
    print("="*60)
    
    # Créer l'usine
    usine = Usine("Usine Beverages Inc.")
    print(f"\n🏭 Usine créée: {usine.nom}")
    
    # Créer les processus de production
    processus = creer_processus_production()
    
    # Créer et ajouter les lignes de production
    lignes = [
        LigneProduction("Ligne Eau", 100, processus['eau']),
        LigneProduction("Ligne Jus", 80, processus['jus']),
        LigneProduction("Ligne Soda", 120, processus['soda']),
        LigneProduction("Ligne Énergisante", 60, processus['energisante'])
    ]
    
    for ligne in lignes:
        usine.ajouter_ligne_production(ligne)
    
    # Initialiser le stock
    print(f"\n📦 Initialisation du stock...")
    initialiser_stock(usine)
    
    # Créer des exemples de boissons
    print(f"\n🥤 Création des boissons d'exemple...")
    boissons = creer_exemples_boissons()
    
    for boisson in boissons:
        print(f"  - {boisson.nom}")
    
    # Démontrer la production
    demonstrer_production(usine, boissons)
    
    # Afficher le rapport final
    print("\n" + "="*60)
    print("RAPPORT FINAL DE PRODUCTION")
    print("="*60)
    print(usine.obtenir_rapport_production())
    
    # Afficher les statistiques
    print("\n" + "="*60)
    print("STATISTIQUES")
    print("="*60)
    stats = usine.obtenir_statistiques()
    print(f"Total de boissons produites: {stats['total_boissons_produites']}")
    print(f"Lignes actives: {stats['lignes_actives']}/{stats['total_lignes']}")
    print("Répartition par type:")
    for type_boisson, count in stats['types_boissons'].items():
        print(f"  - {type_boisson}: {count}")
    
    print("\n✨ Démonstration terminée!")


if __name__ == "__main__":
    main()