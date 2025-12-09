# Contribuer à Outil de Maintenance Système

Nous accueillons les contributions de la communauté ! Voici comment vous pouvez nous aider.

## 🤝 Processus de contribution

### 1. Fork et Clone

```bash
# Fork le projet sur GitHub
# Puis cloner votre fork
git clone https://github.com/VOTRE_USERNAME/outil-maintenance.git
cd outil-maintenance
```

### 2. Créer une branche

```bash
# Créer une branche pour votre fonctionnalité
git checkout -b feature/ma-super-fonctionnalite

# Ou pour un bug fix
git checkout -b fix/mon-bug-a-fixer
```

### 3. Développer et tester

```bash
# Créer l'environnement de développement
.\start_dev.bat

# Tester votre code
python src\OutilMaintenance.py
```

### 4. Commit et Push

```bash
# Commit avec un message clair
git commit -m "Add ma super fonctionnalité"

# Push vers votre fork
git push origin feature/ma-super-fonctionnalite
```

### 5. Créer une Pull Request

1. Aller sur GitHub
2. Cliquer sur "New Pull Request"
3. Remplir la description
4. Attendre la revue

## 📋 Guide de style

### Code Python

```python
# ✅ Bon
def scanner_disque(chemin: str) -> dict:
    """Scanne le disque et retourne l'analyse."""
    resultats = {}
    # ...
    return resultats

# ❌ Mauvais
def scan(p):
    r = {}
    # ...
    return r
```

### Commits

```
✅ Bon:
"Add analyse disque avec graphiques"
"Fix bug affichage des dossiers vides"
"Update documentation pour v2.2"

❌ Mauvais:
"Fix"
"Update"
"asdfghjk"
```

## 🔍 Tests

Avant de soumettre une Pull Request, assurez-vous que :

- [ ] Le code compile sans erreur
- [ ] Toutes les fonctionnalités testées fonctionnent
- [ ] Aucun message d'erreur dans les logs
- [ ] Le code suit le guide de style
- [ ] La documentation est à jour

## 🐛 Signaler un bug

Utilisez le template [Bug Report](.github/ISSUE_TEMPLATE/bug_report.yml) pour signaler les bugs.

Incluez :
- Version de Windows
- Version de l'application
- Étapes pour reproduire
- Message d'erreur complet

## 💡 Suggérer une fonctionnalité

Utilisez le template [Feature Request](.github/ISSUE_TEMPLATE/feature_request.yml).

Décrivez :
- La fonctionnalité souhaitée
- Pourquoi ce serait utile
- Votre implémentation proposée

## 📚 Documentation

Si vous modifiez des fonctionnalités, mettez à jour la documentation :

- `docs/GUIDE_NOUVELLES_FONCTIONS.md` - Guide utilisateur
- `docs/BUILD_GUIDE.md` - Guide de build
- Code comments - Commentaires dans le code

## ✅ Checklist avant Pull Request

- [ ] Code testé et fonctionnel
- [ ] Commits avec bons messages
- [ ] Documentation mise à jour
- [ ] Pas de fichiers de debug
- [ ] .gitignore respecté
- [ ] Tests réussis
- [ ] Code suit le guide de style

## 🚫 Ce que nous n'accepterons pas

- ❌ Code non fonctionnel ou buggé
- ❌ Commits squashés ou history sale
- ❌ Code qui casse les fonctionnalités existantes
- ❌ Modifications importantes sans discussion
- ❌ Documentation incomplète

## 🎯 Domaines d'aide utiles

1. **Code** - Nouvelles fonctionnalités, optimisations
2. **Tests** - Vérification et rapport de bugs
3. **Documentation** - Amélioration des guides
4. **Traduction** - Support multi-langues
5. **Design** - Icônes, thèmes, interface

## 💬 Questions ?

- Ouvrir une issue pour les discussions
- Consulter la documentation existante
- Regarder les issues fermées pour voir comment ont été résolus les problèmes

## 📞 Code of Conduct

- Respectueux et inclusif
- Pas de harcèlement
- Critique constructive
- Bienvenue à tous

---

Merci de contribuer ! 🙏

