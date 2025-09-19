#!/usr/bin/env python3
"""
Point d'entrée principal pour le système d'usine de boissons.
Permet de choisir entre la démonstration et l'exécution des tests.
"""

import sys
from demonstration import main as demo_main
from tests import run_tests


def afficher_menu():
    """Affiche le menu principal."""
    print("🏭 SYSTÈME D'USINE DE PRODUCTION DE BOISSONS")
    print("=" * 50)
    print("Choisissez une option:")
    print("1. 🎮 Lancer la démonstration")
    print("2. 🧪 Exécuter les tests")
    print("3. ❌ Quitter")
    print("=" * 50)


def main():
    """Fonction principale avec menu interactif."""
    while True:
        afficher_menu()
        
        try:
            choix = input("Votre choix (1-3): ").strip()
            
            if choix == "1":
                print("\n🎮 Lancement de la démonstration...")
                print("-" * 50)
                demo_main()
                
            elif choix == "2":
                print("\n🧪 Exécution des tests...")
                print("-" * 50)
                success = run_tests()
                if not success:
                    print("\n⚠️  Certains tests ont échoué. Vérifiez le code.")
                
            elif choix == "3":
                print("\n👋 Au revoir!")
                sys.exit(0)
                
            else:
                print("\n❌ Choix invalide. Veuillez choisir 1, 2 ou 3.")
            
            # Attendre avant de revenir au menu
            input("\nAppuyez sur Entrée pour continuer...")
            print("\n" * 2)  # Espacement
            
        except KeyboardInterrupt:
            print("\n\n👋 Au revoir!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Erreur inattendue: {e}")
            input("Appuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()