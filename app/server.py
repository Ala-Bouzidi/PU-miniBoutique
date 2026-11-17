import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from .db import init_db
from .repository import Repository
from .service import OrderService

DB='boutique.sqlite3'

def create_handler(db_path):
    service=OrderService(Repository(db_path))
    repo=service.repo
    class Handler(BaseHTTPRequestHandler):
        def reply(self,status,obj):
            data=json.dumps(obj,ensure_ascii=False).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type','application/json; charset=utf-8')
            self.send_header('Content-Length',str(len(data)))
            self.end_headers();self.wfile.write(data)
        def body(self):
            n=int(self.headers.get('Content-Length','0'))
            if n > 4096 or n < 1: raise ValueError('Corps JSON invalide')
            obj=json.loads(self.rfile.read(n))
            if not isinstance(obj,dict):raise ValueError('Objet JSON attendu')
            return obj
        def do_GET(self):
            p=urlsplit(self.path).path
            if p=='/api/products': return self.reply(200,repo.products())
            if p.startswith('/api/orders/'):
                try: oid=int(p.split('/')[-1]);o=repo.get_order(oid)
                except ValueError: o=None
                return self.reply(200,o) if o else self.reply(404,{'error':'Introuvable'})
            if p=='/':
                data=b'Mini-boutique TP - API: GET /api/products; POST /api/orders; POST /api/orders/{id}/pay'
                self.send_response(200);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data);return
            self.reply(404,{'error':'Introuvable'})
        def do_POST(self):
            p=urlsplit(self.path).path
            try:
                obj=self.body()
                if p=='/api/orders':
                    if set(obj)!={'product_id','quantity'}:raise ValueError('Champs attendus: product_id, quantity')
                    return self.reply(201,service.checkout(obj['product_id'],obj['quantity']))
                if p.startswith('/api/orders/') and p.endswith('/pay'):
                    parts=p.split('/')
                    if len(parts)!=5 or not parts[3].isdigit():return self.reply(404,{'error':'Introuvable'})
                    if set(obj)!={'success'}:raise ValueError('Champ attendu: success')
                    return self.reply(200,service.pay(int(parts[3]),obj['success']))
                return self.reply(404,{'error':'Introuvable'})
            except (ValueError,TypeError,KeyError,json.JSONDecodeError) as exc:
                return self.reply(400,{'error':str(exc)})
            except Exception:
                return self.reply(500,{'error':'Erreur interne'})
    return Handler

if __name__=='__main__':
    init_db(DB)
    print('API locale de démonstration sur http://127.0.0.1:8000')
    ThreadingHTTPServer(('127.0.0.1',8000),create_handler(DB)).serve_forever()
