# 📦 Guide de Build et Distribution

## Outil de Maintenance Système v2.1

---

## 🎯 Objectif

Ce guide explique comment créer un installateur Windows professionnel (.exe) pour distribuer l'Outil de Maintenance Système.

---

## 📋 Prérequis

### 1. Python et dépendances
```powershell
# Vérifier Python (3.7 ou supérieur)
python --version

# Installer les dépendances
pip install -r requirements.txt
pip install pyinstaller
```

### 2. Inno Setup
- Télécharger depuis: https://jrsoftware.org/isdl.php
- Installer la version 6.x (recommandé)
- Ajouter au PATH (optionnel)

### 3. Icône de l'application (optionnel)
- Créer ou télécharger un fichier `icon.ico`
- Format: .ico, 256x256 pixels recommandé
- Placer dans le dossier `venv/`

---

## 🔨 Étape 1 : Build de l'exécutable

### Méthode automatique (recommandée)

```powershell
cd c:\Users\c.lecomte\Documents\dev_pyt\Dossier_vide_search\venv
python build.py
```

Le script `build.py` va :
1. ✓ Vérifier les dépendances
2. ✓ Nettoyer les anciens builds
3. ✓ Vérifier l'icône
4. ✓ Compiler avec PyInstaller
5. ✓ Vérifier le résultat

### Méthode manuelle

```powershell
# Nettoyer
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

# Compiler
pyinstaller OutilMaintenance.spec --clean --noconfirm
```

### Résultat attendu

```
dist/
└── OutilMaintenance/
    ├── OutilMaintenance.exe        (exécutable principal)
    ├── PyQt5/                       (bibliothèques)
    ├── reportlab/                   (bibliothèques)
    ├── README.txt
    ├── LICENSE.txt
    ├── GUIDE_NOUVELLES_FONCTIONS.md
    └── AMELIORATIONS.md
```

### Test de l'exécutable

```powershell
# Lancer l'exécutable
.\dist\OutilMaintenance\OutilMaintenance.exe

# Test en tant qu'administrateur
Start-Process .\dist\OutilMaintenance\OutilMaintenance.exe -Verb RunAs
```

---

## 📦 Étape 2 : Création de l'installateur

### Avec Inno Setup Compiler (GUI)

1. Ouvrir **Inno Setup Compiler**
2. File > Open > Sélectionner `setup.iss`
3. Build > Compile (ou F9)
4. Attendre la compilation (30 secondes - 2 minutes)

### Avec la ligne de commande

```powershell
# Si Inno Setup est dans le PATH
ISCC.exe setup.iss

# Sinon, chemin complet
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" setup.iss
```

### Résultat attendu

```
..\installer\
└── OutilMaintenance_Setup_v2.1.exe    (~50-80 Mo)
```

---

## 🧪 Étape 3 : Test de l'installateur

### Tests à effectuer

1. **Installation standard**
   ```powershell
   ..\installer\OutilMaintenance_Setup_v2.1.exe
   ```
   - Vérifier l'assistant d'installation
   - Lire le README.txt
   - Accepter la licence
   - Choisir le dossier d'installation
   - Créer les raccourcis

2. **Test des fonctionnalités**
   - ✓ Lancer l'application
   - ✓ Tester chaque onglet
   - ✓ Vérifier les logs
   - ✓ Tester l'export PDF
   - ✓ Tester le nettoyage (avec précaution)

3. **Désinstallation**
   - Via le Panneau de configuration
   - Via le menu Démarrer
   - Vérifier la suppression complète

---

## 📝 Structure du fichier .iss

### Sections principales

```ini
[Setup]           ; Configuration générale de l'installateur
[Languages]       ; Langues disponibles (français)
[Tasks]           ; Tâches optionnelles (raccourcis)
[Files]           ; Fichiers à installer
[Icons]           ; Raccourcis à créer
[Run]             ; Actions après installation
[Registry]        ; Entrées de registre
[Code]            ; Code Pascal personnalisé
```

### Personnalisation

Éditez `setup.iss` pour modifier :

```ini
#define MyAppVersion "2.1"           ; Version
#define MyAppPublisher "c.Lecomte"   ; Auteur
#define MyAppURL "https://..."       ; Site web

DefaultDirName={autopf}\OutilMaintenance  ; Dossier d'installation
SetupIconFile=icon.ico                     ; Icône de l'installateur
```

---

## 🎨 Personnalisation visuelle (optionnel)

### Créer des images pour l'installateur

1. **Banner principal** (`installer_banner.bmp`)
   - Dimensions: 164 x 314 pixels
   - Format: BMP 24-bit
   - Affiché à gauche de l'assistant

2. **Petite icône** (`installer_small.bmp`)
   - Dimensions: 55 x 58 pixels
   - Format: BMP 24-bit
   - Affiché en haut à droite

Placez ces fichiers dans `venv/` et décommentez dans `setup.iss`:
```ini
WizardImageFile=installer_banner.bmp
WizardSmallImageFile=installer_small.bmp
```

---

## 🚀 Distribution

### Options de distribution

1. **Téléchargement direct**
   - Héberger sur GitHub Releases
   - Héberger sur Google Drive / OneDrive
   - Site web personnel

2. **Checksum (recommandé)**
   ```powershell
   # Générer le checksum SHA256
   Get-FileHash ..\installer\OutilMaintenance_Setup_v2.1.exe -Algorithm SHA256
   ```
   Inclure dans les notes de version

3. **Signature numérique (optionnel, avancé)**
   - Obtenir un certificat de signature de code
   - Signer avec `signtool.exe`
   - Évite les avertissements Windows SmartScreen

---

## ⚙️ Configuration avancée PyInstaller

### Réduire la taille de l'exécutable

Éditez `OutilMaintenance.spec`:

```python
excludes=[
    'matplotlib',  # Non utilisé
    'numpy',       # Non utilisé
    'pandas',      # Non utilisé
    'scipy',       # Non utilisé
    'PIL',         # Non utilisé
    'tkinter',     # Non utilisé
],
```

### Mode console pour debug

```python
console=True,  # Affiche la console (pour debug)
```

### Fichier unique (non recommandé pour cette app)

```python
# Dans OutilMaintenance.spec, remplacer EXE() par:
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,  # ← Ajouter
    a.zipfiles,  # ← Ajouter
    a.datas,     # ← Ajouter
    [],
    name='OutilMaintenance',
    # ... reste identique
)

# Supprimer COLLECT() complètement
```

⚠️ Plus lent au démarrage, mais fichier unique

---

## 🐛 Dépannage

### Erreur: "PyInstaller not found"
```powershell
pip install pyinstaller
```

### Erreur: "Failed to execute script"
- Vérifier les dépendances dans `requirements.txt`
- Tester avec `console=True` pour voir les erreurs
- Vérifier les `hiddenimports` dans `.spec`

### Erreur: "UPX is not available"
```python
# Dans .spec, désactiver UPX:
upx=False,
```

### L'installateur ne se compile pas
- Vérifier que `dist/OutilMaintenance/` existe
- Vérifier les chemins dans `setup.iss`
- Vérifier la syntaxe du fichier .iss

### Avertissement Windows SmartScreen
- Normal pour les applications non signées
- L'utilisateur doit cliquer "Plus d'infos" > "Exécuter quand même"
- Solution: Signer l'application avec un certificat

---

## 📊 Checklist de release

Avant de distribuer :

- [ ] Tester l'exécutable sur Windows 10 et 11
- [ ] Tester l'installation complète
- [ ] Vérifier toutes les fonctionnalités
- [ ] Tester la désinstallation
- [ ] Générer le checksum SHA256
- [ ] Mettre à jour le numéro de version
- [ ] Créer les notes de version
- [ ] Tester sur une machine vierge (si possible)

---

## 📚 Ressources

- **PyInstaller**: https://pyinstaller.org/
- **Inno Setup**: https://jrsoftware.org/isinfo.php
- **Documentation Inno Setup**: https://jrsoftware.org/ishelp/
- **PyInstaller Spec**: https://pyinstaller.org/en/stable/spec-files.html

---

## 🆘 Support

Pour toute question sur le build:
1. Vérifier les logs PyInstaller dans `build/`
2. Vérifier les logs Inno Setup dans la console
3. Consulter la documentation officielle

---

**Auteur**:  C.L (Skill_teams)  
**Version**: 2.1  
**Date**: 9 décembre 2025
