import requests
import xmlrpclib
import sys

record_url = sys.argv[1]
kinto_user = 'vieuxsinge'
kinto_password = sys.argv[2]

odoo_url = sys.argv[3]
odoo_username = 'contact@vieuxsinge.com'
odoo_password = sys.argv[4]
odoo_db = 'brasserieduvieuxsinge'

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(odoo_url))
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(odoo_url))
uid = common.authenticate(odoo_db, odoo_username, odoo_password, {})
ids = models.execute_kw(odoo_db, uid, odoo_password, 'sale.order', 'search', [[['state', '=', 'sale']]])
product_ids = [p['product_id'][0] for p in models.execute_kw(odoo_db, uid, odoo_password, 'sale.order', 'read', [ids], {'fields': ['product_id']})]

volumes = {
    12: 4,
    13: 4.5,
    14: 18,
    15: 16,
    16: 9,
    17: 8,
    25: 2.25,
    26: 2
}
new_volume = sum([volumes[p] for p in product_ids])

resp = requests.put(record_url, json={'data': {'liters': new_volume}}, auth=(kinto_user, kinto_password))
