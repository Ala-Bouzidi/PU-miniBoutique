from .payment import FakePaymentGateway

class OrderService:
    def __init__(self, repository, gateway=None):
        self.repo=repository
        self.gateway=gateway or FakePaymentGateway()

    def checkout(self, product_id, quantity):
        if type(product_id) is not int or type(quantity) is not int or quantity <= 0:
            raise ValueError('Paramètres invalides')
        return self.repo.create_order(product_id,quantity)

    def pay(self, order_id, success=True):
        if type(order_id) is not int or type(success) is not bool:
            raise ValueError('Paramètres invalides')
        order=self.repo.get_order(order_id)
        if not order:
            raise ValueError('Commande inexistante')
        if order['status'] != 'PENDING':
            return order
        result=self.gateway.charge(order_id,order['amount_cents'],success)
        return self.repo.settle(order_id, result['approved'], result['reference'])
