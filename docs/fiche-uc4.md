# Fiche UC4 — Payer une commande
**Acteur principal :** Client. **Acteur secondaire :** prestataire de paiement (simulé).

**Préconditions :** commande existante, statut `PENDING`, stock réservé.

**Scénario nominal :**
1. Le client lance le paiement d'une commande.
2. Le contrôleur transmet l'identifiant au service métier.
3. Le service vérifie l'existence et le statut de la commande.
4. Le prestataire simulé approuve le paiement.
5. Le système enregistre `PAID` et une référence de paiement.
6. Le client reçoit la confirmation.

**Alternatives :** paiement refusé → `FAILED` et restitution du stock ; commande déjà traitée → renvoi du statut existant, sans double débit simulé ; commande introuvable → erreur.

**Postcondition nominale :** statut `PAID` enregistré et stock réservé conservé.

**Critères d'acceptation :** tests nominal, refus, idempotence, stock insuffisant, route HTTP bout en bout.
