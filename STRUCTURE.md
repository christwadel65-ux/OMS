# 📁 Structure du Projet - OMS (Outil de Maintenance Système)

## Arborescence Propre

```
OMS/
│
├── 📄 README.md                    # Vue d'ensemble + guide rapide
├── 📄 CONTRIBUTING.md              # Guide de contribution
├── 📄 DEMARRAGE_RAPIDE.md         # Instructions de démarrage
├── 📄 requirements.txt             # Dépendances Python
├── 📄 .gitignore                   # Fichiers ignorés par Git
├── 📄 start_dev.bat               # Démarrage rapide (Windows)
│
├── 📂 src/                        # 🔧 CODE SOURCE
│   └── OutilMaintenance.py        # Application principale (PyQt5)
│
├── 📂 build_tools/                # 🛠️ OUTILS DE BUILD
│   ├── dev.spec                   # Configuration PyInstaller
│   ├── setup.iss                  # Script Inno Setup (installateur)
│   ├── build.py                   # Automatisation du build
│   ├── build.bat                  # Batch pour Windows
│   └── OutilMaintenance.spec      # [DEPRECATED - utiliser dev.spec]
│
├── 📂 docs/                       # 📚 DOCUMENTATION
│   ├── README.txt                 # Guide pour utilisateurs finaux
│   ├── LICENSE.txt                # Licence du projet
│   ├── BUILD_GUIDE.md             # Guide de compilation détaillé
│   ├── BUILD_README.md            # Résumé des étapes de build
│   ├── GUIDE_NOUVELLES_FONCTIONS.md   # Documentation des fonctionnalités
│   ├── AMELIORATIONS.md           # Historique des versions
│   └── version_info.txt           # Métadonnées de version
│
├── 📂 assets/                     # 🎨 RESSOURCES
│   ├── icon.ico                   # Icône 256x256 de l'application
│   └── app_icon.png               # Version PNG de l'icône
│
├── 📂 installer/                  # 📦 SORTIE INSTALLEUR (généré)
│   └── OutilMaintenance_Setup_v*.exe   # Installateur Windows (créé par Inno Setup)
│
├── 📂 .github/                    # 🔧 CONFIG GITHUB
│   └── workflows/                 # Workflows automatisés
│
├── 📂 .vscode/                    # 💻 CONFIG VS CODE
│   └── settings.json              # Paramètres VS Code
│
├── 📂 venv/                       # 🐍 ENVIRONNEMENT VIRTUEL
│   └── [dossiers Python - IGNORÉ PAR GIT]
│
└── 📂 dist/ & build/              # ⚙️ ARTEFACTS DE BUILD (IGNORÉS)
    └── [générés par PyInstaller - IGNORÉ PAR GIT]
```

## 🎯 Description des dossiers principaux

### `/src`
- Contient tout le code source Python
- **Fichier principal** : `OutilMaintenance.py`
- Utilise PyQt5 pour l'interface graphique
- Génère des rapports PDF via ReportLab

### `/build_tools`
- Scripts et fichiers pour créer les exécutables et installateurs
- `dev.spec` : Configuration PyInstaller pour générer l'EXE
- `setup.iss` : Configuration Inno Setup pour l'installateur MSI
- `build.py` : Orchestre tout le processus de build

### `/docs`
- Documentation utilisateur et technique
- Guide d'installation pour l'installateur MSI
- Historique des versions et améliorations
- Informations de licence

### `/assets`
- Ressources graphiques (icônes)
- Utilisées dans l'EXE et l'installateur

### `/installer`
- Répertoire de sortie pour l'installateur Windows
- Créé lors de la compilation de `setup.iss`

## 📋 Fichiers à la racine

| Fichier | Rôle |
|---------|------|
| `README.md` | Vue d'ensemble du projet |
| `requirements.txt` | Dépendances Python (`pip install -r requirements.txt`) |
| `.gitignore` | Fichiers ignorés par Git (venv/, build/, dist/, etc.) |
| `start_dev.bat` | Script rapide pour démarrer l'env virtuel |

## 🔄 Processus de Build

```
1. Développement
   └─ Modifier src/OutilMaintenance.py

2. Créer l'exécutable
   └─ python build_tools/build.py
   └─ Génère: dist/OutilMaintenance/OutilMaintenance.exe

3. Créer l'installateur
   └─ Ouvrir build_tools/setup.iss avec Inno Setup
   └─ Compiler (Build > Compile)
   └─ Génère: installer/OutilMaintenance_Setup_v*.exe
```

## .gitignore - Fichiers ignorés

```
venv/           # Environnement virtuel
build/          # Cache de compilation PyInstaller
dist/           # Exécutables compilés
__pycache__/    # Cache Python
*.pyc           # Fichiers compilés Python
.vscode/        # Config VS Code (local)
.idea/          # Config IDE (local)
```

## 📝 Notes importantes

✅ **Bonnes pratiques respectées:**
- Séparation claire code/docs/outils
- Environnement virtuel isolé
- Artefacts de build ignorés par Git
- Documentation exhaustive
- Scripts d'automatisation fournis

⚠️ **À faire avant de compiler:**
1. Vérifier que `icon.ico` existe dans `assets/`
2. Vérifier les chemins dans `dev.spec`
3. Vérifier la version dans les fichiers de config

## 🚀 Commandes rapides

```bash
# Activer l'environnement virtuel
.\start_dev.bat

# Installer les dépendances
pip install -r requirements.txt

# Compiler l'exécutable
cd build_tools
python build.py

# Compiler l'installateur
# → Ouvrir build_tools/setup.iss avec Inno Setup Compiler
# → Cliquer Build > Compile
```
