"""
Module pour la modélisation de l'usine de production de boissons.
Gère les lignes de production, les stocks et les processus de fabrication.
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import uuid
from boisson import Boisson, Ingredient


class Stock:
    """Gère le stock des ingrédients de l'usine."""
    
    def __init__(self):
        self.ingredients: Dict[str, float] = {}  # nom -> quantité disponible
        self.seuils_alerte: Dict[str, float] = {}  # nom -> seuil minimum
    
    def ajouter_ingredient(self, nom: str, quantite: float, seuil_alerte: float = 10.0):
        """Ajoute ou met à jour un ingrédient dans le stock."""
        if nom in self.ingredients:
            self.ingredients[nom] += quantite
        else:
            self.ingredients[nom] = quantite
            self.seuils_alerte[nom] = seuil_alerte
    
    def consommer_ingredient(self, nom: str, quantite: float) -> bool:
        """Consomme une quantité d'ingrédient. Retourne True si possible."""
        if nom not in self.ingredients:
            return False
        
        if self.ingredients[nom] >= quantite:
            self.ingredients[nom] -= quantite
            return True
        return False
    
    def verifier_disponibilite(self, ingredients_requis: List[Ingredient]) -> bool:
        """Vérifie si tous les ingrédients requis sont disponibles."""
        for ingredient in ingredients_requis:
            if ingredient.nom not in self.ingredients:
                return False
            if self.ingredients[ingredient.nom] < ingredient.quantite:
                return False
        return True
    
    def obtenir_alertes(self) -> List[str]:
        """Retourne la liste des ingrédients en dessous du seuil d'alerte."""
        alertes = []
        for nom, quantite in self.ingredients.items():
            if quantite <= self.seuils_alerte.get(nom, 0):
                alertes.append(f"Stock faible: {nom} ({quantite} unités restantes)")
        return alertes
    
    def __str__(self) -> str:
        return "\n".join([f"{nom}: {quantite}" for nom, quantite in self.ingredients.items()])


class EtapeProduction:
    """Représente une étape dans le processus de production."""
    
    def __init__(self, nom: str, duree_minutes: int, description: str = ""):
        self.nom = nom
        self.duree_minutes = duree_minutes
        self.description = description
    
    def executer(self, boisson: Boisson) -> bool:
        """Exécute l'étape de production. À surcharger dans les sous-classes."""
        print(f"Exécution de l'étape: {self.nom} pour {boisson.nom}")
        return True
    
    def __str__(self) -> str:
        return f"{self.nom} ({self.duree_minutes}min)"


class ProcessusProduction:
    """Définit un processus de production complet avec ses étapes."""
    
    def __init__(self, nom: str, etapes: List[EtapeProduction]):
        self.nom = nom
        self.etapes = etapes
    
    def calculer_duree_totale(self) -> int:
        """Calcule la durée totale du processus en minutes."""
        return sum(etape.duree_minutes for etape in self.etapes)
    
    def executer_processus(self, boisson: Boisson) -> bool:
        """Exécute toutes les étapes du processus."""
        print(f"Démarrage du processus {self.nom} pour {boisson.nom}")
        
        for i, etape in enumerate(self.etapes, 1):
            print(f"Étape {i}/{len(self.etapes)}: {etape.nom}")
            if not etape.executer(boisson):
                print(f"Échec à l'étape {etape.nom}")
                return False
        
        print(f"Processus {self.nom} terminé avec succès")
        return True


class LigneProduction:
    """Représente une ligne de production dans l'usine."""
    
    def __init__(self, nom: str, capacite_horaire: int, processus: ProcessusProduction):
        self.nom = nom
        self.capacite_horaire = capacite_horaire  # unités par heure
        self.processus = processus
        self.est_active = False
        self.production_actuelle: Optional[Boisson] = None
        self.heure_debut_production: Optional[datetime] = None
        self.historique_production: List[Dict] = []
    
    def demarrer_production(self, boisson: Boisson) -> bool:
        """Démarre la production d'une boisson."""
        if self.est_active:
            print(f"Ligne {self.nom} déjà en production")
            return False
        
        self.est_active = True
        self.production_actuelle = boisson
        self.heure_debut_production = datetime.now()
        
        # Générer un numéro de lot unique
        numero_lot = f"{self.nom}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        boisson.definir_lot(numero_lot)
        
        print(f"Production démarrée sur {self.nom} - Lot: {numero_lot}")
        return self.processus.executer_processus(boisson)
    
    def terminer_production(self) -> Optional[Boisson]:
        """Termine la production et retourne la boisson produite."""
        if not self.est_active:
            return None
        
        boisson_produite = self.production_actuelle
        
        # Enregistrer dans l'historique
        self.historique_production.append({
            'boisson': boisson_produite.nom,
            'lot': boisson_produite.numero_lot,
            'debut': self.heure_debut_production,
            'fin': datetime.now(),
            'volume': boisson_produite.volume
        })
        
        # Réinitialiser la ligne
        self.est_active = False
        self.production_actuelle = None
        self.heure_debut_production = None
        
        print(f"Production terminée sur {self.nom}")
        return boisson_produite
    
    def obtenir_statut(self) -> str:
        """Retourne le statut actuel de la ligne."""
        if not self.est_active:
            return f"Ligne {self.nom}: Inactive"
        
        temps_production = datetime.now() - self.heure_debut_production
        return f"Ligne {self.nom}: En production - {self.production_actuelle.nom} (depuis {temps_production})"


class Usine:
    """Classe principale représentant l'usine de production de boissons."""
    
    def __init__(self, nom: str):
        self.nom = nom
        self.lignes_production: List[LigneProduction] = []
        self.stock = Stock()
        self.production_journaliere: List[Boisson] = []
        self.objectifs_production: Dict[str, int] = {}  # type_boisson -> quantité cible
    
    def ajouter_ligne_production(self, ligne: LigneProduction):
        """Ajoute une ligne de production à l'usine."""
        self.lignes_production.append(ligne)
        print(f"Ligne {ligne.nom} ajoutée à l'usine {self.nom}")
    
    def definir_objectif_production(self, type_boisson: str, quantite: int):
        """Définit un objectif de production pour un type de boisson."""
        self.objectifs_production[type_boisson] = quantite
    
    def produire_boisson(self, boisson: Boisson) -> bool:
        """Produit une boisson en utilisant une ligne disponible."""
        # Vérifier la disponibilité des ingrédients
        if not self.stock.verifier_disponibilite(boisson.ingredients):
            print("Stock insuffisant pour produire cette boisson")
            return False
        
        # Trouver une ligne disponible
        ligne_disponible = None
        for ligne in self.lignes_production:
            if not ligne.est_active:
                ligne_disponible = ligne
                break
        
        if ligne_disponible is None:
            print("Aucune ligne de production disponible")
            return False
        
        # Consommer les ingrédients
        for ingredient in boisson.ingredients:
            if not self.stock.consommer_ingredient(ingredient.nom, ingredient.quantite):
                print(f"Impossible de consommer {ingredient.nom}")
                return False
        
        # Démarrer la production
        if ligne_disponible.demarrer_production(boisson):
            boisson_produite = ligne_disponible.terminer_production()
            if boisson_produite:
                self.production_journaliere.append(boisson_produite)
                print(f"Boisson {boisson_produite.nom} produite avec succès")
                return True
        
        return False
    
    def obtenir_rapport_production(self) -> str:
        """Génère un rapport de production de l'usine."""
        rapport = [f"=== Rapport de production - {self.nom} ==="]
        rapport.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        rapport.append("")
        
        # Statut des lignes
        rapport.append("Statut des lignes de production:")
        for ligne in self.lignes_production:
            rapport.append(f"  {ligne.obtenir_statut()}")
        rapport.append("")
        
        # Production journalière
        rapport.append(f"Production journalière: {len(self.production_journaliere)} boissons")
        for boisson in self.production_journaliere:
            rapport.append(f"  - {boisson.nom} (Lot: {boisson.numero_lot})")
        rapport.append("")
        
        # Alertes stock
        alertes = self.stock.obtenir_alertes()
        if alertes:
            rapport.append("Alertes stock:")
            for alerte in alertes:
                rapport.append(f"  ⚠️  {alerte}")
        else:
            rapport.append("Stock: Tous les ingrédients sont disponibles")
        
        return "\n".join(rapport)
    
    def obtenir_statistiques(self) -> Dict:
        """Retourne les statistiques de production."""
        stats = {
            'total_boissons_produites': len(self.production_journaliere),
            'lignes_actives': sum(1 for ligne in self.lignes_production if ligne.est_active),
            'total_lignes': len(self.lignes_production),
            'types_boissons': {}
        }
        
        # Compter par type de boisson
        for boisson in self.production_journaliere:
            type_boisson = boisson.__class__.__name__
            stats['types_boissons'][type_boisson] = stats['types_boissons'].get(type_boisson, 0) + 1
        
        return stats