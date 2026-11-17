from .db import connect

class Repository:
    def __init__(self, db_path):
        self.db_path = db_path

    def products(self):
        with connect(self.db_path) as con:
            return [dict(r) for r in con.execute('SELECT * FROM products ORDER BY id')]

    def get_order(self, order_id):
        with connect(self.db_path) as con:
            r = con.execute('SELECT * FROM orders WHERE id=?', (order_id,)).fetchone()
            return dict(r) if r else None

    def create_order(self, product_id, quantity):
        # Transaction atomique: empêche les achats concurrents du dernier exemplaire.
        with connect(self.db_path) as con:
            con.execute('BEGIN IMMEDIATE')
            row=con.execute('SELECT price_cents, stock FROM products WHERE id=?',(product_id,)).fetchone()
            if not row:
                con.rollback();raise ValueError('Produit inexistant')
            if quantity <= 0 or row['stock'] < quantity:
                con.rollback();raise ValueError('Stock insuffisant ou quantité invalide')
            con.execute('UPDATE products SET stock=stock-? WHERE id=?',(quantity, product_id))
            cur=con.execute('INSERT INTO orders(product_id,quantity,amount_cents,status) VALUES (?,?,?,?)',
                            (product_id,quantity,quantity*row['price_cents'],'PENDING'))
            order_id=cur.lastrowid
            con.commit()
            return self.get_order(order_id)

    def settle(self, order_id, approved, reference):
        with connect(self.db_path) as con:
            con.execute('BEGIN IMMEDIATE')
            order=con.execute('SELECT * FROM orders WHERE id=?',(order_id,)).fetchone()
            if not order:
                con.rollback();raise ValueError('Commande inexistante')
            if order['status'] != 'PENDING':
                con.rollback();return dict(order) # idempotence
            if approved:
                con.execute('UPDATE orders SET status=?, payment_reference=? WHERE id=?',('PAID',reference,order_id))
            else:
                con.execute('UPDATE orders SET status=? WHERE id=?',('FAILED',order_id))
                con.execute('UPDATE products SET stock=stock+? WHERE id=?',(order['quantity'],order['product_id']))
            con.commit()
            return self.get_order(order_id)
