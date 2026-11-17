# Architecture de base — UC4

Client HTTP → `app/server.py` (contrôleur) → `app/service.py` (métier) → `app/repository.py` (persistance SQLite).

Le service appelle aussi `app/payment.py` (simulateur externe). Tests : `tests/test_service.py` et `tests/test_integration.py`.

## Endpoints disponibles
- `GET /api/products`
- `POST /api/orders` JSON `{"product_id":1,"quantity":1}`
- `POST /api/orders/{id}/pay` JSON `{"success":true}` (simulation)
- `GET /api/orders/{id}`

La réservation de stock s'effectue dans une transaction `BEGIN IMMEDIATE`. En cas de refus du paiement, le stock est rétabli. Le retour d'un paiement déjà traité ne modifie pas l'état (idempotence locale). Ceci est une démonstration pédagogique et **ne constitue pas un circuit de paiement de production**.
