# 🚀 Démarrage Rapide

## Pour les développeurs

### Première utilisation

```powershell
# 1. Double-cliquer sur start_dev.bat
# OU en ligne de commande:
.\start_dev.bat

# 2. L'environnement virtuel est créé et activé automatiquement
# 3. Les dépendances sont installées

# 4. Lancer l'application
python src\OutilMaintenance.py
```

### Développement quotidien

```powershell
# Activer l'environnement
.\venv\Scripts\Activate.ps1

# Lancer l'application
python src\OutilMaintenance.py

# Désactiver l'environnement
deactivate
```

---

## Pour créer l'installateur

### Méthode rapide

```powershell
# 1. Aller dans build_tools
cd build_tools

# 2. Lancer le build complet
.\build.bat

# 3. Ouvrir setup.iss avec Inno Setup et compiler (F9)
```

### Méthode détaillée

```powershell
# 1. Build de l'exécutable
cd build_tools
python build.py

# 2. Tester l'exécutable
..\dist\OutilMaintenance\OutilMaintenance.exe

# 3. Compiler l'installateur
# Ouvrir setup.iss avec Inno Setup Compiler
# Build > Compile (F9)

# 4. L'installateur est dans ..\installer\
```

---

## Structure du projet

```
Dossier_vide_search/
├── src/                    # Code source
│   └── OutilMaintenance.py
├── docs/                   # Documentation
├── build_tools/            # Outils de build
├── assets/                 # Ressources (icônes)
├── requirements.txt        # Dépendances
├── start_dev.bat          # Démarrage rapide développeur
└── README.md              # Ce fichier
```

---

## Commandes utiles

```powershell
# Mettre à jour les dépendances
pip install --upgrade -r requirements.txt

# Lister les packages installés
pip list

# Nettoyer les builds
Remove-Item -Recurse -Force build, dist

# Vérifier le code (optionnel)
pylint src\OutilMaintenance.py
```

---

## Prochaines étapes

1. ✅ Configurer l'environnement → `start_dev.bat`
2. ✅ Développer → `src\OutilMaintenance.py`
3. ✅ Tester → `python src\OutilMaintenance.py`
4. ✅ Builder → `build_tools\build.py`
5. ✅ Distribuer → Inno Setup

---

**Version**: 2.1  
**Date**: 9 décembre 2025
