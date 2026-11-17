# Mini-boutique en ligne — TP Processus unifiés / 2TUP

Projet pédagogique indépendant, organisé selon `app/`, `docs/`, `tests/`, `.github/workflows/`.

**UC à risque : UC4 — Payer une commande.** Le prestataire de paiement est **simulé**. Aucun paiement réel et aucune carte bancaire.

## Installation et exécution

Python 3.11+ requis.

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python -m app.server
```

Ouvrir `http://127.0.0.1:8000/api/products`.

Avec curl :

```bash
curl -X POST http://127.0.0.1:8000/api/orders -H "Content-Type: application/json" -d '{"product_id":1,"quantity":1}'
# Remplacer 1 par l'identifiant de commande retourné
curl -X POST http://127.0.0.1:8000/api/orders/1/pay -H "Content-Type: application/json" -d '{"success":true}'
```

Sous Windows PowerShell, utiliser `Invoke-RestMethod` ou Postman au lieu des commandes curl ci-dessus.

## Livrables
- `docs/vision.md` — vision
- `docs/uc.puml` — diagramme UC
- `docs/y.puml` — modèle en Y
- `docs/architecture.md` — architecture
- `docs/fiche-uc4.md` — fiche UC4
- `docs/classes.puml` — classes
- `docs/sequence.puml` — séquence
- `tests/` — tests unitaires et d'intégration
- `docs/revue-croisee.md` — trame de revue (à faire réellement)
- `docs/organisation-tp.md` — itérations, tickets, jalons

## Publier sur GitHub et gérer les jalons

```bash
git init
git add .
git commit -m "Initialiser projet et livrables du TP"
git branch -M main
# Créer d'abord un dépôt GitHub vide nommé mini-boutique-tp
git remote add origin https://github.com/VOTRE_COMPTE/mini-boutique-tp.git
git push -u origin main
# Poser ce tag uniquement après validation du jalon élaboration
git tag v0.1-elaboration
git push origin v0.1-elaboration
```

Pour tracer l'UC4 en branche dédiée : créer `feature/uc4-paiement` depuis l'état d'élaboration, effectuer les commits de construction puis une pull request avec les tests et la revue. Le ZIP donne une **version consolidée** pour démarrer : si la traçabilité historique par itération est exigée, la reconstruire honnêtement dans Git sans prétendre à des commits antérieurs.
