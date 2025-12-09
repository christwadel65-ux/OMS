# 📁 Structure du Projet - Outil de Maintenance Système

```
Dossier_vide_search/
│
├── 📄 README.md                    # Ce fichier - Vue d'ensemble du projet
├── 📄 requirements.txt             # Dépendances Python
├── 📄 .gitignore                   # Fichiers à ignorer par Git
│
├── 📂 src/                         # CODE SOURCE
│   └── OutilMaintenance.py         # Application principale
│
├── 📂 docs/                        # DOCUMENTATION
│   ├── README.txt                  # Guide d'installation (pour installateur)
│   ├── LICENSE.txt                 # Licence MIT
│   ├── GUIDE_NOUVELLES_FONCTIONS.md    # Guide utilisateur complet
│   ├── AMELIORATIONS.md            # Historique des versions
│   ├── BUILD_GUIDE.md              # Guide de build détaillé
│   └── BUILD_README.md             # Résumé build
│
├── 📂 build_tools/                 # OUTILS DE BUILD
│   ├── setup.iss                   # Script Inno Setup (installateur)
│   ├── OutilMaintenance.spec       # Configuration PyInstaller
│   ├── dev.spec                    # Ancienne spec (à supprimer)
│   ├── build.py                    # Script de build automatique
│   ├── build.bat                   # Script batch
│   └── version_info.txt            # Métadonnées Windows
│
├── 📂 assets/                      # RESSOURCES (optionnel)
│   ├── icon.ico                    # Icône de l'application (à créer)
│   ├── installer_banner.bmp        # Banner installateur (à créer)
│   └── installer_small.bmp         # Petite icône (à créer)
│
├── 📂 build/                       # Généré par PyInstaller (ignoré)
├── 📂 dist/                        # Exécutable compilé (ignoré)
├── 📂 installer/                   # Installateur final (ignoré)
└── 📂 venv/                        # Environnement virtuel Python (ignoré)

```

---

## 🎯 Avantages de cette structure

### ✅ **Organisation claire**
- Code source isolé dans `src/`
- Documentation centralisée dans `docs/`
- Outils de build séparés dans `build_tools/`
- Assets graphiques dans `assets/`

### ✅ **Simplicité**
- 4 dossiers principaux seulement
- Fichiers à la racine minimaux
- Navigation intuitive

### ✅ **Maintenabilité**
- Séparation des responsabilités
- Facile de trouver ce qu'on cherche
- Prêt pour versioning Git

---

## 🚀 Démarrage rapide

### Pour développer
```powershell
# 1. Créer l'environnement virtuel
python -m venv venv

# 2. Activer l'environnement
.\venv\Scripts\Activate.ps1

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
python src\OutilMaintenance.py
```

### Pour créer l'installateur
```powershell
# 1. Aller dans build_tools
cd build_tools

# 2. Lancer le build
python build.py

# 3. Compiler avec Inno Setup
# Ouvrir setup.iss et compiler (F9)
```

---

## 📝 Fichiers principaux

| Fichier | Description |
|---------|-------------|
| `src/OutilMaintenance.py` | Application principale |
| `requirements.txt` | Liste des dépendances |
| `docs/GUIDE_NOUVELLES_FONCTIONS.md` | Documentation utilisateur |
| `build_tools/setup.iss` | Script d'installation |
| `build_tools/build.py` | Automatisation du build |

---

## 🔄 Migration depuis l'ancienne structure

Si vous aviez des chemins en dur dans votre code, mettez-les à jour :

```python
# Ancien
"./README.txt"

# Nouveau  
"../docs/README.txt"
```

---

## 🗑️ Dossiers à ignorer (.gitignore)

- `venv/` - Environnement virtuel
- `build/` - Fichiers de build temporaires
- `dist/` - Exécutable compilé
- `installer/` - Installateur généré
- `__pycache__/` - Cache Python
- `*.pyc` - Fichiers compilés Python

---

**Structure créée le** : 9 décembre 2025  
**Version** : 2.1
