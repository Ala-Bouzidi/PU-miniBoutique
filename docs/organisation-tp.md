# Organisation du processus unifié

## Inception
Vision (`vision.md`), acteurs, 5 UC (`uc.puml`), priorisation, plan de 3 itérations.

## Élaboration
Dépôt Git/GitHub, issue UC4, branche `feature/uc4-paiement`, diagramme des UC, architecture contrôleur/service/données, CI avec test passant. Tag à créer `v0.1-elaboration` après vérification.

## Construction
Fiche détaillée UC4, diagramme de classes, séquence, implémentation, tests unitaires et test d'intégration. Tag suggéré `v0.2-construction`.

## Transition
Revue croisée par une autre équipe avec preuve, anomalies et corrections, exécution finale CI, démonstration et tag proposé `v1.0-transition`.

## Itérations
1. I1 : vision, UC, architecture, première route HTTP + premier test (élaboration).
2. I2 : paiement simulé, gestion des refus, tests unitaires/intégration (construction).
3. I3 : revue croisée, corrections, démonstration (transition).

## Priorisation des UC (échelle 1–3)
| UC | Valeur métier | Risque | Impact architecture | Priorité |
|---|---:|---:|---:|---|
| UC4 Payer | 3 | 3 | 3 | 1 |
| UC3 Commander | 3 | 2 | 3 | 2 |
| UC2 Panier | 3 | 1 | 2 | 3 |
| UC1 Catalogue | 2 | 1 | 1 | 4 |
| UC5 Suivre | 2 | 1 | 2 | 5 |

Ces scores sont des choix pédagogiques à discuter dans l'équipe.

## Tickets GitHub à créer
- UC1 — Consulter les produits
- UC2 — Gérer le panier
- UC3 — Passer commande
- UC4 — Payer une commande (risque technique)
- UC5 — Suivre une commande

## Milestones GitHub
- Inception
- Élaboration
- Construction
- Transition

Chaque UC a sa branche `feature/ucN-*`; chaque milestone doit être fermé et étiqueté avec un tag lors de son achèvement.
