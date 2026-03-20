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

Reste a finaliser:

- ajustements visuels fins pour coller encore davantage a la V1
- revue manuelle de parite comportementale
- nettoyage des donnees de test locales si necessaire

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
