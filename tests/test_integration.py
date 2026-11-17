import json
import threading
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen
from app.db import init_db
from app.server import create_handler

def test_route_complete_controleur_service_donnees(tmp_path):
    db=str(tmp_path/'web.sqlite3');init_db(db)
    server=ThreadingHTTPServer(('127.0.0.1',0),create_handler(db))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base=f'http://127.0.0.1:{server.server_port}'
    def post(path,obj):
        request=Request(base+path,data=json.dumps(obj).encode(),headers={'Content-Type':'application/json'},method='POST')
        with urlopen(request) as response:return response.status,json.loads(response.read())
    try:
        status,order=post('/api/orders',{'product_id':1,'quantity':1})
        assert status==201 and order['status']=='PENDING'
        status,paid=post(f"/api/orders/{order['id']}/pay",{'success':True})
        assert status==200 and paid['status']=='PAID'
        with urlopen(base+f"/api/orders/{order['id']}") as response:
            assert json.loads(response.read())['status']=='PAID'
    finally:
        server.shutdown();server.server_close();thread.join(timeout=2)
