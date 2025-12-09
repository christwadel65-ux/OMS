# 📐 Notes de Restructuration

## ✅ Actions effectuées

### 1. Nettoyage de la racine
- ✅ Déplacé `OutilMaintenance.spec` → `build_tools/dev.spec`
- ✅ Supprimé les dossiers temporaires `build/` et `dist/`
- ✅ Conservé uniquement les fichiers essentiels à la racine

### 2. Mise à jour des fichiers de configuration
- ✅ Mis à jour `.gitignore` (nettoyé et organisé)
- ✅ Créé `.editorconfig` pour la cohérence du code
- ✅ Mis à jour `build_tools/build.py` (référence à dev.spec)

### 3. Documentation
- ✅ Créé `STRUCTURE.md` (architecture complète)
- ✅ Créé ce fichier `STRUCTURE_NOTES.md`

## 📂 Structure finale

```
OMS/
├── src/                    # Code source
├── build_tools/            # Outils de compilation
├── docs/                   # Documentation
├── assets/                 # Ressources
├── installer/              # Sortie installeur
├── .github/                # Configuration GitHub
├── .vscode/                # Configuration VS Code
├── venv/                   # Environnement virtuel
├── README.md               # Vue d'ensemble
├── CONTRIBUTING.md         # Guide de contribution
├── DEMARRAGE_RAPIDE.md    # Démarrage rapide
├── STRUCTURE.md           # [NOUVEAU] Guide de structure
├── requirements.txt        # Dépendances Python
├── .gitignore             # Fichiers ignorés
├── .editorconfig          # [NOUVEAU] Config éditeur
└── start_dev.bat          # Script démarrage
```

## 🔧 Fichiers modifiés

### `.gitignore`
- ✅ Nettoyé et organisé
- ✅ Supprimé les références aux dossiers venv obsolètes
- ✅ Mieux structuré (sections claires)

### `build_tools/build.py`
- ✅ Ligne 87 : `OutilMaintenance.spec` → `dev.spec`

### `build_tools/dev.spec`
- ✅ Contient la configuration PyInstaller correcte
- ✅ Points vers `../src/OutilMaintenance.py`
- ✅ Génère `OutilMaintenance.exe`

## 🎯 Avantages de cette restructuration

1. **Clarté** : Chaque dossier a un rôle clairement défini
2. **Maintenabilité** : Facile de trouver les fichiers
3. **Scalabilité** : Prêt pour l'ajout de nouvelles fonctionnalités
4. **Professionnel** : Structure standard de projet Python
5. **Documentation** : Bien documentée pour les nouveaux contributeurs

## 📋 Checklist avant release

- [ ] Vérifier que `icon.ico` existe dans `assets/`
- [ ] Tester la compilation : `python build_tools/build.py`
- [ ] Vérifier que l'EXE se génère correctement
- [ ] Tester l'installation avec l'MSI
- [ ] Mettre à jour les versions dans les fichiers de config
- [ ] Pousser sur GitHub avec : `git push origin main`

## 🔗 Fichiers de référence

| Fichier | Utilisation |
|---------|------------|
| `src/OutilMaintenance.py` | Application principale |
| `build_tools/dev.spec` | Config PyInstaller |
| `build_tools/setup.iss` | Config Inno Setup |
| `build_tools/build.py` | Automatisation du build |
| `requirements.txt` | Dépendances Python |

## 💡 Conseils pour les contributeurs

1. Ne modifiez jamais les fichiers dans `venv/`, `build/`, ou `dist/`
2. Ajoutez les dépendances dans `requirements.txt`
3. Suivez le guide dans `CONTRIBUTING.md`
4. Documentez les changements dans `docs/AMELIORATIONS.md`

## 📞 Questions fréquentes

**Q: Pourquoi déplacer OutilMaintenance.spec en dev.spec?**
R: Pour avoir un nom standard et clair. `dev` indique que c'est la configuration de développement/build.

**Q: Où trouver les exécutables générés?**
R: Après `python build_tools/build.py`:
   - EXE : `dist/OutilMaintenance/OutilMaintenance.exe`
   - Installeur MSI : `installer/OutilMaintenance_Setup_v*.exe`

**Q: Puis-je modifier les fichiers dans build_tools/?**
R: Oui, mais avec prudence. Ces fichiers sont critiques pour la compilation.

---

**Dernière mise à jour:** 2025-12-09
**Responsable:** GitHub Copilot
