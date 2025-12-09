# 🚀 Outil de Maintenance Système

![Version](https://img.shields.io/badge/version-2.1-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-blue.svg)

## 📋 Description

**Outil de Maintenance Système** est une application Windows complète pour gérer, nettoyer et analyser votre système. Elle combine plusieurs fonctionnalités essentielles dans une interface moderne et intuitive.

### ✨ Fonctionnalités principales

- **📊 Analyse de l'espace disque** : Vue d'ensemble des partitions, détection des gros fichiers
- **🗑️ Nettoyage système** : Suppression des fichiers temporaires, cache navigateurs, Prefetch
- **🔐 Analyse de sécurité** : Programmes au démarrage, logiciels obsolètes, services suspects
- **📋 Gestion des programmes** : Liste complète, filtrage avancé, export PDF
- **📁 Gestion des dossiers** : Détection et suppression des dossiers vides

## 🎯 Caractéristiques

- ✅ **Interface moderne** : Design dark mode professionnel
- ✅ **Multi-threading** : Opérations asynchrones pour ne pas bloquer l'interface
- ✅ **Export avancé** : PDF et TXT pour tous les rapports
- ✅ **Logging complet** : Traçabilité de toutes les opérations
- ✅ **Sécurité** : Confirmations obligatoires pour les opérations critiques
- ✅ **Multi-plateforme** : Support Windows 7/8/10/11 (32 et 64 bits)

## 📦 Installation

### Depuis l'installateur (recommandé)

1. Télécharger `OutilMaintenance_Setup_v2.1.exe`
2. Exécuter l'installateur
3. Suivre les instructions
4. Lancer depuis le menu Démarrage

### Depuis le code source

```bash
# 1. Cloner le dépôt
git clone https://github.com/votrecompte/outil-maintenance.git
cd outil-maintenance

# 2. Créer l'environnement virtuel
python -m venv venv

# 3. Activer l'environnement
.\venv\Scripts\Activate.ps1

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Lancer l'application
python src/OutilMaintenance.py
```

## 🚀 Démarrage rapide

### Pour les utilisateurs

```powershell
# Double-cliquer sur OutilMaintenance_Setup_v2.1.exe
# Ou lancer depuis le menu Démarrer
```

### Pour les développeurs

```powershell
# Script automatique (Windows)
.\start_dev.bat

# Ou manuellement
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/OutilMaintenance.py
```

## 📚 Documentation

- **[Guide d'utilisation](docs/GUIDE_NOUVELLES_FONCTIONS.md)** - Tous les détails des fonctionnalités
- **[Guide de build](docs/BUILD_GUIDE.md)** - Comment créer l'installateur
- **[Améliorations v2.1](docs/AMELIORATIONS.md)** - Historique des versions
- **[Démarrage rapide](DEMARRAGE_RAPIDE.md)** - Pour développeurs
- **[Restructuration](RESTRUCTURATION.md)** - Structure du projet

## 🏗️ Structure du projet

```
outil-maintenance/
├── src/                    # Code source principal
│   └── OutilMaintenance.py # Application PyQt5
├── docs/                   # Documentation complète
├── build_tools/            # Scripts de build et Inno Setup
├── assets/                 # Ressources (icônes, images)
├── requirements.txt        # Dépendances Python
└── README.md              # Ce fichier
```

## 💻 Configuration requise

| Élément | Requirement |
|---------|-------------|
| **OS** | Windows 7, 8, 10, 11 (32/64 bits) |
| **Python** | 3.7 ou supérieur (pour développeurs) |
| **Espace disque** | 100 Mo minimum |
| **RAM** | 256 Mo minimum |
| **Droits** | Administrateur (pour certaines fonctionnalités) |

## 🔧 Dépendances

### Runtime
- **PyQt5** ≥5.15.0 - Interface graphique
- **ReportLab** ≥3.6.0 - Génération PDF

### Build
- **PyInstaller** ≥4.5 - Compilation en exécutable
- **Inno Setup** 6.x - Création de l'installateur

## 📊 Fonctionnalités détaillées

### 📊 Analyse de l'espace disque
- Vue d'ensemble de toutes les partitions
- Indicateurs colorés (🟢 < 75% | 🟡 75-90% | 🔴 > 90%)
- Détection des fichiers > 100 Mo
- Tri par taille, nom, date de modification

### 🗑️ Nettoyage système
- Fichiers temporaires Windows
- Cache utilisateur
- Prefetch (avec droits admin)
- Corbeille
- Cache des navigateurs (Chrome, Edge, Firefox)

### 🔐 Analyse de sécurité
- Programmes au démarrage Windows
- Détection de logiciels obsolètes
- Services Windows suspects
- Recommandations de sécurité

### 📋 Gestion des programmes
- Liste complète des logiciels installés
- Filtrage par nom, version, chemin
- Recherche globale sur disque C:
- Export en PDF et TXT

## 🐛 Signalement de bugs

Trouvé un bug ? Créez une [issue GitHub](https://github.com/votrecompte/outil-maintenance/issues)

Merci d'inclure :
- Version de Windows
- Version de l'application
- Description du problème
- Étapes pour reproduire

## 🤝 Contributions

Les contributions sont bienvenues ! Pour contribuer :

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 License

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](docs/LICENSE.txt) pour les détails.

## 👨‍💻 Auteur

**c.Lecomte** - Développeur et mainteneur principal

## 🙏 Remerciements

- PyQt5 - Framework d'interface graphique
- ReportLab - Génération de PDF
- Inno Setup - Création d'installateurs
- La communauté Python

## 📞 Support

### Besoin d'aide ?

1. Consulter la [documentation complète](docs/)
2. Vérifier les [issues existantes](https://github.com/votrecompte/outil-maintenance/issues)
3. Créer une nouvelle issue si le problème persiste

### Signaler un problème de sécurité

⚠️ Pour les failles de sécurité, **ne pas utiliser les issues publiques**. 
Contactez directement l'auteur via email.

## 🔮 Feuille de route

### ✅ Version 2.1 (Actuelle)
- Analyse de l'espace disque
- Nettoyage du système
- Analyse de sécurité
- Installateur Windows
- Structure professionnelle

### 🚀 Version 2.2 (Planifiée)
- [ ] Recherche de fichiers dupliqués
- [ ] Planificateur de tâches
- [ ] Interface de paramètres avancés
- [ ] Thème clair / sombre switchable

### 🎯 Version 3.0 (Long terme)
- [ ] Support Linux et macOS
- [ ] Application portable (sans installateur)
- [ ] Synchronisation cloud
- [ ] Interface web

## 📊 Statistiques

![GitHub stars](https://img.shields.io/github/stars/votrecompte/outil-maintenance?style=social)
![GitHub forks](https://img.shields.io/github/forks/votrecompte/outil-maintenance?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/votrecompte/outil-maintenance?style=social)

---

**Dernière mise à jour** : 9 décembre 2025  
**Version** : 2.1.0  
**Status** : ✅ Production

