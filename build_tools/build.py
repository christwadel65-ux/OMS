# Script de build complet pour Outil de Maintenance Système
# Auteur: c.Lecomte
# Version: 2.1
# Usage: python build.py

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Aller à la racine du projet
project_root = Path(__file__).parent.parent
os.chdir(project_root)

print("=" * 70)
print("  BUILD - Outil de Maintenance Système v2.1")
print("  Auteur: c.Lecomte")
print("=" * 70)
print(f"Répertoire de travail: {os.getcwd()}")
print()

# 1. Vérifier les dépendances
print("[1/5] Vérification des dépendances...")
try:
    import PyQt5
    import reportlab
    print("✓ PyQt5 trouvé")
    print("✓ ReportLab trouvé")
except ImportError as e:
    print(f"✗ Erreur: {e}")
    print("\nInstallez les dépendances avec:")
    print("  pip install -r requirements.txt")
    print(f"  (depuis {project_root})")
    sys.exit(1)

# Vérifier PyInstaller
try:
    import PyInstaller
    print("✓ PyInstaller trouvé")
except ImportError:
    print("✗ PyInstaller non trouvé")
    print("\nInstallation de PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip",
                   "install", "pyinstaller"], check=True)
    print("✓ PyInstaller installé")

print()

# 2. Nettoyer les anciens builds
print("[2/5] Nettoyage des anciens builds...")
dirs_to_clean = ['build', 'dist', '__pycache__']
for dir_name in dirs_to_clean:
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name)
        print(f"✓ Supprimé: {dir_name}/")

# Nettoyer les fichiers .pyc
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.pyc'):
            os.remove(os.path.join(root, file))

print()

# 3. Créer l'icône si elle n'existe pas
print("[3/5] Vérification de l'icône...")
icon_path = 'assets/icon.ico'
if not os.path.exists(icon_path):
    print("⚠ Avertissement: assets/icon.ico non trouvé")
    print("  L'exécutable sera créé sans icône personnalisée")
    print("  Vous pouvez ajouter un fichier icon.ico dans assets/ (format .ico, 256x256)")
else:
    print(f"✓ {icon_path} trouvé")

print()

# 4. Build avec PyInstaller
print("[4/5] Compilation avec PyInstaller...")
print("  (Cela peut prendre plusieurs minutes...)")
try:
    subprocess.run([
        sys.executable,
        "-m",
        "PyInstaller",
        "build_tools/OutilMaintenance.spec",
        "--clean",
        "--noconfirm"
    ], check=True)
    print("✓ Compilation réussie")
except subprocess.CalledProcessError:
    print("✗ Erreur lors de la compilation")
    sys.exit(1)

print()

# 5. Vérification finale
print("[5/5] Vérification du build...")
exe_path = Path("dist/OutilMaintenance/OutilMaintenance.exe")
if exe_path.exists():
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"✓ Exécutable créé: {exe_path}")
    print(f"  Taille: {size_mb:.2f} Mo")

    # Vérifier les fichiers de documentation
    dist_dir = Path("dist/OutilMaintenance")
    docs = ['README.txt', 'LICENSE.txt',
            'GUIDE_NOUVELLES_FONCTIONS.md', 'AMELIORATIONS.md']
    for doc in docs:
        if (dist_dir / doc).exists():
            print(f"  ✓ {doc}")
        else:
            print(f"  ⚠ {doc} manquant")
else:
    print("✗ Exécutable non trouvé")
    sys.exit(1)

print()
print("=" * 70)
print("  BUILD TERMINÉ AVEC SUCCÈS!")
print("=" * 70)
print()
print("Prochaines étapes:")
print("  1. Testez l'exécutable: dist\\OutilMaintenance\\OutilMaintenance.exe")
print("  2. Créez l'installateur avec Inno Setup:")
print("     - Ouvrez build_tools\\setup.iss avec Inno Setup Compiler")
print("     - Compilez (Build > Compile)")
print("  3. L'installateur sera dans: installer\\")
print()
print("Note: Pour créer l'installateur, vous devez avoir Inno Setup installé:")
print("      https://jrsoftware.org/isdl.php")
print()
