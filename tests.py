"""
Tests unitaires pour le modèle d'usine de production de boissons.
Valide le bon fonctionnement des différentes classes et méthodes.
"""

import unittest
from datetime import datetime
from boisson import Boisson, Ingredient, Eau, Jus, Soda, BoissonEnergisante
from usine import Usine, LigneProduction, ProcessusProduction, EtapeProduction, Stock


class TestIngredient(unittest.TestCase):
    """Tests pour la classe Ingredient."""
    
    def test_creation_ingredient(self):
        """Test de création d'un ingrédient."""
        ingredient = Ingredient("eau", 1.0, "L")
        self.assertEqual(ingredient.nom, "eau")
        self.assertEqual(ingredient.quantite, 1.0)
        self.assertEqual(ingredient.unite, "L")
    
    def test_representation_ingredient(self):
        """Test de la représentation textuelle d'un ingrédient."""
        ingredient = Ingredient("sucre", 0.5, "kg")
        self.assertEqual(str(ingredient), "sucre: 0.5 kg")


class TestBoissons(unittest.TestCase):
    """Tests pour les classes de boissons."""
    
    def setUp(self):
        """Préparation des données de test."""
        self.ingredients_eau = [
            Ingredient("eau", 0.98),
            Ingredient("minéraux", 0.02)
        ]
        
        self.ingredients_jus = [
            Ingredient("fruits_orange", 0.8),
            Ingredient("eau", 0.2)
        ]
        
        self.ingredients_soda = [
            Ingredient("eau", 0.85),
            Ingredient("sucre", 0.12),
            Ingredient("co2", 0.03)
        ]
        
        self.ingredients_energie = [
            Ingredient("eau", 0.4),
            Ingredient("cafeine", 0.001),
            Ingredient("taurine", 0.002)
        ]
    
    def test_creation_eau(self):
        """Test de création d'une eau."""
        eau = Eau("Eau Minérale", 1.0, self.ingredients_eau, est_gazeuse=False)
        self.assertEqual(eau.nom, "Eau Minérale")
        self.assertEqual(eau.volume, 1.0)
        self.assertFalse(eau.est_gazeuse)
        self.assertTrue(eau.valider_ingredients())
    
    def test_cout_production_eau(self):
        """Test du calcul de coût pour l'eau."""
        eau_plate = Eau("Eau Plate", 1.0, self.ingredients_eau, est_gazeuse=False)
        eau_gazeuse = Eau("Eau Gazeuse", 1.0, self.ingredients_eau, est_gazeuse=True)
        
        cout_plate = eau_plate.calculer_cout_production()
        cout_gazeuse = eau_gazeuse.calculer_cout_production()
        
        self.assertGreater(cout_gazeuse, cout_plate)
    
    def test_creation_jus(self):
        """Test de création d'un jus."""
        jus = Jus("Jus d'Orange", 1.0, self.ingredients_jus, pourcentage_fruits=80.0)
        self.assertEqual(jus.nom, "Jus d'Orange")
        self.assertEqual(jus.pourcentage_fruits, 80.0)
        self.assertTrue(jus.valider_ingredients())
    
    def test_creation_soda(self):
        """Test de création d'un soda."""
        soda = Soda("Cola", 1.0, self.ingredients_soda, taux_sucre=120.0)
        self.assertEqual(soda.nom, "Cola")
        self.assertEqual(soda.taux_sucre, 120.0)
        self.assertTrue(soda.valider_ingredients())
    
    def test_creation_boisson_energisante(self):
        """Test de création d'une boisson énergisante."""
        energie = BoissonEnergisante("Energy", 0.5, self.ingredients_energie, taux_cafeine=320.0)
        self.assertEqual(energie.nom, "Energy")
        self.assertEqual(energie.taux_cafeine, 320.0)
        self.assertTrue(energie.valider_ingredients())
    
    def test_definition_lot(self):
        """Test de définition du lot de production."""
        eau = Eau("Eau Test", 1.0, self.ingredients_eau)
        self.assertIsNone(eau.numero_lot)
        self.assertIsNone(eau.date_production)
        
        eau.definir_lot("LOT-001")
        self.assertEqual(eau.numero_lot, "LOT-001")
        self.assertIsInstance(eau.date_production, datetime)


class TestStock(unittest.TestCase):
    """Tests pour la gestion du stock."""
    
    def setUp(self):
        """Préparation du stock de test."""
        self.stock = Stock()
        self.stock.ajouter_ingredient("eau", 100.0, 10.0)
        self.stock.ajouter_ingredient("sucre", 50.0, 5.0)
    
    def test_ajout_ingredient(self):
        """Test d'ajout d'ingrédient au stock."""
        self.stock.ajouter_ingredient("sel", 20.0, 2.0)
        self.assertEqual(self.stock.ingredients["sel"], 20.0)
        self.assertEqual(self.stock.seuils_alerte["sel"], 2.0)
    
    def test_consommation_ingredient(self):
        """Test de consommation d'ingrédient."""
        # Consommation réussie
        resultat = self.stock.consommer_ingredient("eau", 10.0)
        self.assertTrue(resultat)
        self.assertEqual(self.stock.ingredients["eau"], 90.0)
        
        # Consommation échouée (quantité insuffisante)
        resultat = self.stock.consommer_ingredient("eau", 200.0)
        self.assertFalse(resultat)
        self.assertEqual(self.stock.ingredients["eau"], 90.0)
    
    def test_verification_disponibilite(self):
        """Test de vérification de disponibilité des ingrédients."""
        ingredients_ok = [
            Ingredient("eau", 50.0),
            Ingredient("sucre", 20.0)
        ]
        
        ingredients_ko = [
            Ingredient("eau", 200.0),  # Trop
            Ingredient("sucre", 10.0)
        ]
        
        self.assertTrue(self.stock.verifier_disponibilite(ingredients_ok))
        self.assertFalse(self.stock.verifier_disponibilite(ingredients_ko))
    
    def test_alertes_stock(self):
        """Test des alertes de stock faible."""
        # Réduire le stock d'eau en dessous du seuil
        self.stock.consommer_ingredient("eau", 95.0)
        alertes = self.stock.obtenir_alertes()
        
        self.assertGreater(len(alertes), 0)
        self.assertIn("eau", alertes[0])


class TestProcessusProduction(unittest.TestCase):
    """Tests pour les processus de production."""
    
    def setUp(self):
        """Préparation des processus de test."""
        self.etape1 = EtapeProduction("Préparation", 5)
        self.etape2 = EtapeProduction("Mélange", 10)
        self.processus = ProcessusProduction("Test", [self.etape1, self.etape2])
    
    def test_duree_processus(self):
        """Test du calcul de durée du processus."""
        duree = self.processus.calculer_duree_totale()
        self.assertEqual(duree, 15)  # 5 + 10
    
    def test_execution_processus(self):
        """Test d'exécution du processus."""
        eau = Eau("Eau Test", 1.0, [Ingredient("eau", 1.0)])
        resultat = self.processus.executer_processus(eau)
        self.assertTrue(resultat)


class TestLigneProduction(unittest.TestCase):
    """Tests pour les lignes de production."""
    
    def setUp(self):
        """Préparation de la ligne de production."""
        etape = EtapeProduction("Test", 5)
        processus = ProcessusProduction("Test Process", [etape])
        self.ligne = LigneProduction("Ligne Test", 100, processus)
    
    def test_statut_ligne_inactive(self):
        """Test du statut d'une ligne inactive."""
        statut = self.ligne.obtenir_statut()
        self.assertIn("Inactive", statut)
        self.assertFalse(self.ligne.est_active)
    
    def test_demarrage_production(self):
        """Test de démarrage de production."""
        eau = Eau("Eau Test", 1.0, [Ingredient("eau", 1.0)])
        resultat = self.ligne.demarrer_production(eau)
        
        self.assertTrue(resultat)
        self.assertTrue(self.ligne.est_active)
        self.assertEqual(self.ligne.production_actuelle, eau)
        self.assertIsNotNone(eau.numero_lot)
    
    def test_terminer_production(self):
        """Test de fin de production."""
        eau = Eau("Eau Test", 1.0, [Ingredient("eau", 1.0)])
        self.ligne.demarrer_production(eau)
        
        boisson_produite = self.ligne.terminer_production()
        
        self.assertIsNotNone(boisson_produite)
        self.assertFalse(self.ligne.est_active)
        self.assertIsNone(self.ligne.production_actuelle)
        self.assertEqual(len(self.ligne.historique_production), 1)


class TestUsine(unittest.TestCase):
    """Tests pour l'usine de production."""
    
    def setUp(self):
        """Préparation de l'usine de test."""
        self.usine = Usine("Usine Test")
        
        # Créer une ligne de production simple
        etape = EtapeProduction("Test", 5)
        processus = ProcessusProduction("Test Process", [etape])
        ligne = LigneProduction("Ligne Test", 100, processus)
        self.usine.ajouter_ligne_production(ligne)
        
        # Ajouter du stock
        self.usine.stock.ajouter_ingredient("eau", 100.0)
        self.usine.stock.ajouter_ingredient("minéraux", 50.0)
    
    def test_ajout_ligne_production(self):
        """Test d'ajout de ligne de production."""
        nombre_lignes_initial = len(self.usine.lignes_production)
        
        etape = EtapeProduction("Nouvelle Étape", 3)
        processus = ProcessusProduction("Nouveau Process", [etape])
        nouvelle_ligne = LigneProduction("Nouvelle Ligne", 80, processus)
        
        self.usine.ajouter_ligne_production(nouvelle_ligne)
        
        self.assertEqual(len(self.usine.lignes_production), nombre_lignes_initial + 1)
    
    def test_production_boisson_reussie(self):
        """Test de production réussie d'une boisson."""
        eau = Eau("Eau Test", 1.0, [
            Ingredient("eau", 10.0),
            Ingredient("minéraux", 5.0)
        ])
        
        resultat = self.usine.produire_boisson(eau)
        
        self.assertTrue(resultat)
        self.assertEqual(len(self.usine.production_journaliere), 1)
        # Vérifier que le stock a été consommé
        self.assertEqual(self.usine.stock.ingredients["eau"], 90.0)
        self.assertEqual(self.usine.stock.ingredients["minéraux"], 45.0)
    
    def test_production_boisson_stock_insuffisant(self):
        """Test de production échouée par manque de stock."""
        eau = Eau("Eau Test", 1.0, [
            Ingredient("eau", 200.0)  # Plus que disponible
        ])
        
        resultat = self.usine.produire_boisson(eau)
        
        self.assertFalse(resultat)
        self.assertEqual(len(self.usine.production_journaliere), 0)
    
    def test_statistiques_usine(self):
        """Test des statistiques de l'usine."""
        # Produire quelques boissons
        eau1 = Eau("Eau 1", 1.0, [Ingredient("eau", 5.0)])
        eau2 = Eau("Eau 2", 1.0, [Ingredient("eau", 5.0)])
        
        self.usine.produire_boisson(eau1)
        self.usine.produire_boisson(eau2)
        
        stats = self.usine.obtenir_statistiques()
        
        self.assertEqual(stats['total_boissons_produites'], 2)
        self.assertEqual(stats['total_lignes'], 1)
        self.assertIn('Eau', stats['types_boissons'])
        self.assertEqual(stats['types_boissons']['Eau'], 2)


def run_tests():
    """Exécute tous les tests."""
    print("🧪 EXÉCUTION DES TESTS UNITAIRES")
    print("="*50)
    
    # Créer la suite de tests
    test_suite = unittest.TestSuite()
    
    # Ajouter tous les tests
    test_classes = [
        TestIngredient,
        TestBoissons,
        TestStock,
        TestProcessusProduction,
        TestLigneProduction,
        TestUsine
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Résumé
    print(f"\n{'='*50}")
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ Tous les tests sont passés avec succès!")
    else:
        print("❌ Certains tests ont échoué")
        
        if result.failures:
            print("\nÉchecs:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback}")
        
        if result.errors:
            print("\nErreurs:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()