import subprocess
import sys

def install_module(module_name):
    try:
        # Tente d'importer le module pour vérifier s'il est déjà installé
        __import__(module_name)
        print(f"Le module '{module_name}' est déjà installé.")
    except ImportError:
        # Si le module n'est pas trouvé, exécute 'pip install' pour l'installer
        print(f"Installation du module '{module_name}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
        print(f"Le module '{module_name}' a été installé avec succès.")




modules = ["openpyxl", "sqlite3", "tk"]

for module in modules:
    install_module(module)
