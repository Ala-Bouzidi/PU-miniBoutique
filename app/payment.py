class FakePaymentGateway:
    """Simulation locale, jamais un prestataire de paiement réel."""
    def charge(self, order_id, amount_cents, success=True):
        if amount_cents <= 0:
            raise ValueError('Montant incorrect')
        return {'approved': bool(success), 'reference': f'SIM-{order_id}'}
