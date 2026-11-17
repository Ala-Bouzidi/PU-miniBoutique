import pytest
from app.db import init_db
from app.repository import Repository
from app.service import OrderService

@pytest.fixture
def ctx(tmp_path):
    db=str(tmp_path/'test.sqlite3');init_db(db)
    repo=Repository(db)
    return repo,OrderService(repo)

def test_paiement_nominal(ctx):
    repo,svc=ctx
    order=svc.checkout(1,2)
    assert order['amount_cents']==2400
    paid=svc.pay(order['id'])
    assert paid['status']=='PAID'
    assert paid['payment_reference']=='SIM-'+str(order['id'])
    assert next(p for p in repo.products() if p['id']==1)['stock']==3

def test_refus_paiement_restitue_stock(ctx):
    repo,svc=ctx
    order=svc.checkout(1,2)
    failed=svc.pay(order['id'],False)
    assert failed['status']=='FAILED'
    assert next(p for p in repo.products() if p['id']==1)['stock']==5

def test_stock_insuffisant(ctx):
    _,svc=ctx
    with pytest.raises(ValueError,match='Stock insuffisant'):
        svc.checkout(1,6)

def test_paiement_idempotent(ctx):
    repo,svc=ctx
    order=svc.checkout(1,1)
    assert svc.pay(order['id'])==svc.pay(order['id'])
    assert next(p for p in repo.products() if p['id']==1)['stock']==4

def test_quantite_invalide(ctx):
    _,svc=ctx
    with pytest.raises(ValueError): svc.checkout(1,0)
