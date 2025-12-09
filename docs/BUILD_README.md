# 📦 FICHIERS DE BUILD - Résumé

## Structure créée pour la distribution

```
venv/
├── Dev.py                              # Code source principal
├── requirements.txt                     # Dépendances Python
│
├── 📦 BUILD & PACKAGING
│   ├── setup.iss                       # Script Inno Setup (INSTALLATEUR)
│   ├── OutilMaintenance.spec           # Configuration PyInstaller
│   ├── version_info.txt                # Informations de version Windows
│   ├── build.py                        # Script de build automatique
│   ├── build.bat                       # Script batch simple
│   └── BUILD_GUIDE.md                  # Guide complet de build
│
├── 📄 DOCUMENTATION
│   ├── README.txt                      # Readme pour l'installateur
│   ├── LICENSE.txt                     # Licence MIT
│   ├── GUIDE_NOUVELLES_FONCTIONS.md    # Guide utilisateur
│   └── AMELIORATIONS.md                # Historique des changements
│
└── 🎨 ASSETS (à créer, optionnel)
    ├── icon.ico                        # Icône de l'application
    ├── installer_banner.bmp            # Banner installateur (164x314)
    └── installer_small.bmp             # Petite icône (55x58)
```

---

## 🚀 COMMANDES RAPIDES

### Build de l'exécutable
```powershell
# Méthode 1 : Script automatique (recommandé)
python build.py

# Méthode 2 : Batch simple
build.bat

# Méthode 3 : Manuel
pyinstaller OutilMaintenance.spec --clean --noconfirm
```

### Création de l'installateur
```powershell
# Avec Inno Setup Compiler (GUI)
# 1. Ouvrir setup.iss
# 2. Build > Compile (F9)

# Avec ligne de commande
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup.iss
```

---

## 📋 CHECKLIST DE BUILD

### Avant le build
- [ ] Mettre à jour le numéro de version dans :
  - [ ] `Dev.py` (ligne version dans docstring)
  - [ ] `setup.iss` (#define MyAppVersion)
  - [ ] `version_info.txt` (filevers et prodvers)
  - [ ] `BUILD_GUIDE.md` (titre)
- [ ] Tester l'application en mode développement
- [ ] Vérifier que toutes les dépendances sont dans requirements.txt

### Après le build
- [ ] Tester l'exécutable dans dist/OutilMaintenance/
- [ ] Vérifier la taille (~50-80 Mo)
- [ ] Tester toutes les fonctionnalités
- [ ] Vérifier les logs

### Après création de l'installateur
- [ ] Tester l'installation complète
- [ ] Vérifier les raccourcis créés
- [ ] Tester la désinstallation
- [ ] Générer le checksum SHA256
- [ ] Créer les notes de version

---

## 🎯 RÉSULTATS ATTENDUS

### Après python build.py
```
dist/OutilMaintenance/
├── OutilMaintenance.exe     (~5-10 Mo)
├── PyQt5/                    (~30-40 Mo)
├── reportlab/                (~5-10 Mo)
├── _internal/                (bibliothèques)
└── documentation .txt/.md

Total: ~50-80 Mo
```

### Après compilation Inno Setup
```
..\installer\
└── OutilMaintenance_Setup_v2.1.exe    (~50-80 Mo compressé)
```

---

## 🔧 PERSONNALISATION

### Changer l'icône
1. Créer/obtenir un fichier .ico (256x256 px)
2. Nommer `icon.ico`
3. Placer dans venv/
4. Rebuild

### Changer les infos de version
Éditer `version_info.txt`:
```python
filevers=(2, 1, 0, 0),     # Version fichier
prodvers=(2, 1, 0, 0),     # Version produit
CompanyName='...',          # Société
FileDescription='...',      # Description
```

### Modifier l'installateur
Éditer `setup.iss`:
- Dossier d'installation par défaut
- Nom de l'application
- Raccourcis créés
- Messages personnalisés
- Exigences système

---

## 📊 VERSIONS

### v2.1 (9 décembre 2025)
- ✅ Analyse de l'espace disque
- ✅ Nettoyage système
- ✅ Analyse de sécurité
- ✅ Scripts de build complets
- ✅ Installateur Inno Setup

### v2.0 (précédent)
- ✅ Refactorisation complète
- ✅ Gestion d'erreurs améliorée
- ✅ Élimination variables globales
- ✅ Logging complet

---

## 🆘 DÉPANNAGE RAPIDE

| Problème | Solution |
|----------|----------|
| PyInstaller not found | `pip install pyinstaller` |
| Imports manquants | Vérifier requirements.txt |
| Exécutable ne démarre pas | Compiler avec `console=True` pour voir les erreurs |
| Installateur ne compile pas | Vérifier que dist/ existe et contient l'exécutable |
| Icône ne s'affiche pas | Vérifier que icon.ico existe en 256x256 |
| Application trop lente | Désactiver UPX dans .spec |

---

## 📚 FICHIERS IMPORTANTS

| Fichier | Usage | Modification |
|---------|-------|--------------|
| `setup.iss` | **Installateur principal** | Fréquente (version, infos) |
| `OutilMaintenance.spec` | Config PyInstaller | Rare (dépendances) |
| `build.py` | Automatisation build | Rare |
| `version_info.txt` | Métadonnées Windows | Fréquente (version) |
| `README.txt` | Info utilisateur | Occasionnelle |

---

## 🎓 POUR ALLER PLUS LOIN

1. **Signature de code**
   - Obtenir un certificat (DigiCert, Sectigo, etc.)
   - Signer avec signtool.exe
   - Évite les avertissements SmartScreen

2. **Auto-update**
   - Implémenter vérification de version
   - Téléchargement automatique
   - API GitHub Releases

3. **Télémétrie (opt-in)**
   - Analytics d'utilisation
   - Rapports d'erreur
   - Statistiques fonctionnalités

4. **Localisation**
   - Support multi-langues
   - Fichiers .po/.mo
   - Détection langue système

---

**Note**: Tous les fichiers de build sont prêts à l'emploi.
Il suffit de lancer `python build.py` pour commencer !

---

**Créé le**: 9 décembre 2025  
**Auteur**:  C.L (Skill_teams)  
**Version**: 2.1
