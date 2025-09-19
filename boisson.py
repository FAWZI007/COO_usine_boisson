"""
Module pour la modélisation des boissons dans l'usine de production.
Implémente les classes de base et les types de boissons spécifiques.
"""

from abc import ABC, abstractmethod
from typing import List, Dict
from datetime import datetime


class Ingredient:
    """Représente un ingrédient utilisé dans la production de boissons."""
    
    def __init__(self, nom: str, quantite: float, unite: str = "L"):
        self.nom = nom
        self.quantite = quantite
        self.unite = unite
    
    def __str__(self) -> str:
        return f"{self.nom}: {self.quantite} {self.unite}"
    
    def __repr__(self) -> str:
        return f"Ingredient('{self.nom}', {self.quantite}, '{self.unite}')"


class Boisson(ABC):
    """Classe abstraite de base pour tous les types de boissons."""
    
    def __init__(self, nom: str, volume: float, ingredients: List[Ingredient]):
        self.nom = nom
        self.volume = volume  # en litres
        self.ingredients = ingredients
        self.date_production = None
        self.numero_lot = None
    
    @abstractmethod
    def calculer_cout_production(self) -> float:
        """Calcule le coût de production de la boisson."""
        pass
    
    @abstractmethod
    def valider_ingredients(self) -> bool:
        """Valide que les ingrédients sont appropriés pour ce type de boisson."""
        pass
    
    def definir_lot(self, numero_lot: str):
        """Définit le numéro de lot et la date de production."""
        self.numero_lot = numero_lot
        self.date_production = datetime.now()
    
    def obtenir_ingredients(self) -> List[Ingredient]:
        """Retourne la liste des ingrédients."""
        return self.ingredients.copy()
    
    def __str__(self) -> str:
        ingredients_str = ", ".join([str(ing) for ing in self.ingredients])
        return f"{self.nom} ({self.volume}L) - Ingrédients: {ingredients_str}"


class Eau(Boisson):
    """Représente une boisson à base d'eau (eau minérale, eau gazeuse)."""
    
    def __init__(self, nom: str, volume: float, ingredients: List[Ingredient], 
                 est_gazeuse: bool = False):
        super().__init__(nom, volume, ingredients)
        self.est_gazeuse = est_gazeuse
    
    def calculer_cout_production(self) -> float:
        """Calcul simple basé sur le volume et le type d'eau."""
        cout_base = self.volume * 0.5  # 0.5€ par litre
        if self.est_gazeuse:
            cout_base *= 1.2  # Majoration pour gazéification
        return cout_base
    
    def valider_ingredients(self) -> bool:
        """Valide que les ingrédients sont appropriés pour l'eau."""
        ingredients_valides = ["eau", "minéraux", "co2"]
        for ingredient in self.ingredients:
            if ingredient.nom.lower() not in ingredients_valides:
                return False
        return True


class Jus(Boisson):
    """Représente un jus de fruits."""
    
    def __init__(self, nom: str, volume: float, ingredients: List[Ingredient],
                 pourcentage_fruits: float):
        super().__init__(nom, volume, ingredients)
        self.pourcentage_fruits = pourcentage_fruits
    
    def calculer_cout_production(self) -> float:
        """Calcul basé sur le pourcentage de fruits et le volume."""
        cout_base = self.volume * 1.5  # 1.5€ par litre
        majoration_fruits = (self.pourcentage_fruits / 100) * 0.5
        return cout_base * (1 + majoration_fruits)
    
    def valider_ingredients(self) -> bool:
        """Valide que les ingrédients contiennent des fruits."""
        fruits_presents = any("fruit" in ing.nom.lower() or 
                            any(fruit in ing.nom.lower() for fruit in 
                                ["pomme", "orange", "raisin", "ananas", "mangue"])
                            for ing in self.ingredients)
        return fruits_presents


class Soda(Boisson):
    """Représente un soda (boisson gazeuse sucrée)."""
    
    def __init__(self, nom: str, volume: float, ingredients: List[Ingredient],
                 taux_sucre: float):
        super().__init__(nom, volume, ingredients)
        self.taux_sucre = taux_sucre  # grammes par litre
    
    def calculer_cout_production(self) -> float:
        """Calcul basé sur le volume et le taux de sucre."""
        cout_base = self.volume * 1.0  # 1€ par litre
        majoration_sucre = (self.taux_sucre / 100) * 0.1
        return cout_base * (1 + majoration_sucre)
    
    def valider_ingredients(self) -> bool:
        """Valide que les ingrédients contiennent eau, sucre et CO2."""
        ingredients_requis = ["eau", "sucre", "co2"]
        ingredients_presents = [ing.nom.lower() for ing in self.ingredients]
        return all(requis in " ".join(ingredients_presents) for requis in ingredients_requis)


class BoissonEnergisante(Boisson):
    """Représente une boisson énergisante."""
    
    def __init__(self, nom: str, volume: float, ingredients: List[Ingredient],
                 taux_cafeine: float):
        super().__init__(nom, volume, ingredients)
        self.taux_cafeine = taux_cafeine  # mg par litre
    
    def calculer_cout_production(self) -> float:
        """Calcul basé sur le volume et le taux de caféine."""
        cout_base = self.volume * 2.0  # 2€ par litre (plus cher)
        majoration_cafeine = (self.taux_cafeine / 1000) * 0.5
        return cout_base * (1 + majoration_cafeine)
    
    def valider_ingredients(self) -> bool:
        """Valide que les ingrédients contiennent de la caféine."""
        cafeine_presente = any("cafeine" in ing.nom.lower() or 
                              "taurine" in ing.nom.lower() or
                              "guarana" in ing.nom.lower()
                              for ing in self.ingredients)
        return cafeine_presente