# Vision — Mini-boutique en ligne
Les clients souhaitent acheter des produits simplement depuis leur navigateur.
Le système permet de consulter les produits, gérer un panier, commander, payer et suivre une commande.
Les acteurs sont le client, l'administrateur (évolution) et le prestataire de paiement.
La valeur métier est de rendre les commandes accessibles et de fiabiliser le paiement et les stocks.
Le prototype se concentre sur l'UC4 « Payer une commande » avec un simulateur de paiement uniquement.

## Périmètre et hypothèses
- Paiement simulé : aucune donnée bancaire réelle, aucun prélèvement
- Produit de démonstration et stock dans SQLite
- Le catalogue, le panier graphique, les comptes clients et l'administration restent à développer
- Pour une exploitation réelle : authentification, autorisation, HTTPS, gestion vérifiée des retours du prestataire, journal d'audit et gestion des erreurs réseau
