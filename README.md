# RobCo Vault

Refonte propre de la V1 avec objectif de parite fonctionnelle et visuelle progressive.

## Etat actuel

Parite deja reconstruite:

- arborescence dossiers / notes depuis SQLite
- creation, renommage et suppression des dossiers
- creation, lecture, edition, renommage et suppression des notes
- protection des notes par mot de passe
- depliage / repliage de l'arborescence avec persistance locale
- modales de creation et de suppression
- ecran de bienvenue par session
- base visuelle RobCo

Phase actuelle terminee:

- reconstruction fonctionnelle V2 terminee
- rapprochement visuel majeur avec la V1 termine
- RobCo Classic et RobCo Modern disponibles

Suite optionnelle:

- revue visuelle fine ecran par ecran
- nettoyage des donnees locales de test si necessaire
- nouveaux chantiers fonctionnels

## Revue finale optionnelle

Checklist de verification manuelle si tu veux pousser la finition:

- creer, renommer et supprimer un dossier
- creer, lire, editer, renommer et supprimer une note
- creer une note protegee puis verifier mauvais et bon mot de passe
- verifier le repliage / depliage de l'arborescence
- verifier les modales de creation et de suppression
- verifier l'ecran de bienvenue sur nouvelle session
- comparer visuellement la V2 avec la V1 sur le layout global

Donnees locales de test possibles a nettoyer:

- dossiers ou notes de verification crees pendant le developpement
- contenu de `instance/robco.db` si tu veux repartir d'une base propre

## Documentation

- `docs/AGENTS.md`
- `docs/PRODUCT_BRIEF.md`
- `docs/SPEC.md`
- `docs/ARCHITECTURE.md`
- `docs/ROADMAP.md`
- `docs/PARITY_CHECKLIST.md`
- `docs/CONTRIBUTING.md`

## Lancement local

```powershell
.\.venv\Scripts\flask.exe --app run --debug run
```

Puis ouvrir:

- `http://127.0.0.1:5000`
