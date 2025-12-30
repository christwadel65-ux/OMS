# �️ Outil de Maintenance Système

**Version** : 1.0.2  
**Auteur** : C.L (Skill Teams)
**Date de mise à jour** : 15 décembre 2025

## 📋 Description

Application PyQt5 complète pour la gestion et la maintenance des systèmes Windows. Permet de gérer les programmes installés, détecter les dossiers vides, analyser l'espace disque, effectuer des nettoyages système et analyser la sécurité.

## ✨ Fonctionnalités principales

### 📦 Gestion des programmes
- ✅ **Liste des programmes installés** avec nom, version et chemin
- ✅ **Désinstallation de programmes** (NOUVEAU v1.0.2)
  - Vérification de l'existence du désinstalleur
  - Attente de la fin de la désinstallation
  - Rafraîchissement automatique de la liste
  - Masquage des fenêtres PowerShell
- ✅ **Recherche et filtrage** par mot-clé (nom, version, chemin)
- ✅ **Recherche globale** dans tout le disque C:

### 📁 Gestion des dossiers
- ✅ **Détection des dossiers vides**
- ✅ **Affichage de la taille** des dossiers
- ✅ **Suppression sélective** des dossiers vides
- ✅ **Ouverture dans l'explorateur** par double-clic

### 💾 Analyse disque
- ✅ **Informations des partitions** (espace total, utilisé, libre)
- ✅ **Recherche des gros fichiers** (taille personnalisable)
- ✅ **Tri et visualisation** des fichiers volumineux

### 🗑️ Nettoyage système
- ✅ Fichiers temporaires Windows
- ✅ Fichiers temporaires utilisateur
- ✅ Prefetch (nécessite droits admin)
- ✅ Corbeille
- ✅ Cache des navigateurs (Chrome, Edge, Firefox)
- ✅ Rapport détaillé du nettoyage

### 🔐 Analyse de sécurité
- ✅ Programmes au démarrage
- ✅ Détection de programmes obsolètes
- ✅ Services Windows suspects

### 📄 Export de données
- ✅ **Export TXT** des listes
- ✅ **Export PDF** des programmes et dossiers

---

## 📁 Structure du Projet

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
| `src/OutilMaintenance.py` | Application principale (1800+ lignes) |
| `requirements.txt` | Liste des dépendances Python |
| `docs/GUIDE_NOUVELLES_FONCTIONS.md` | Documentation utilisateur complète |
| `build_tools/setup.iss` | Script d'installation Inno Setup |
| `build_tools/build.py` | Script de build automatique |

---

## 🆕 Nouveautés v1.0.2

### Désinstallation de programmes
- ✅ Bouton "Désinstaller le programme sélectionné" dans l'onglet Programmes
- ✅ Message de confirmation avant désinstallation
- ✅ Vérification de l'existence du désinstalleur
- ✅ Attente de la fin réelle du processus de désinstallation
- ✅ Rafraîchissement automatique de la liste après désinstallation
- ✅ Gestion des codes d'erreur (annulation utilisateur, etc.)

### Améliorations techniques
- ✅ Masquage de toutes les fenêtres PowerShell
- ✅ Meilleure gestion des chemins avec espaces
- ✅ Messages d'erreur plus informatifs
- ✅ Support des installations MSI avec désinstallation silencieuse

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

## 🔧 Configuration requise

- **OS** : Windows 10/11 (optimisé pour Windows)
- **Python** : 3.8+ (pour développement)
- **Dépendances** : PyQt5, ReportLab, PyInstaller

---

## 📞 Support

Pour toute question ou suggestion d'amélioration, consultez la documentation dans `docs/GUIDE_NOUVELLES_FONCTIONS.md`.

---

**Structure créée le** : 9 décembre 2025  
**Dernière mise à jour** : 15 décembre 2025  
**Version** : 1.0.2
