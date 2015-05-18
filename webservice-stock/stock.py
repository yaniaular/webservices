# -*- coding: utf-8 -*-
import oerplib

oerp = oerplib.OERP()
oerp.config['timeout']=4000
db = raw_input('Do you want to create a new database before continuing? [y/N]:')
db_name = '1082'
modules = [
        ]

if db == 'y':

    print 'BORRANDO BASE DE DATOS VIEJA'
    oerp.db.drop('admin', db_name)
    
    print 'CREATING A NEW DATABASE'
    oerp.db.create_and_wait('admin', db_name, demo_data=False)
    oerp.login(database=db_name)
    
    print 'INSTALANDO MODULOS'
    module_obj = oerp.get('ir.module.module')

    for mod in modules:
        module_id = module_obj.search([('name', '=', mod)])
        module_obj.button_immediate_install(module_id)

else:
    oerp.login(database=db_name)

print 'ESTABLECIENDO PERMISOS'
res_users_obj = oerp.get('res.users')
user_id = res_users_obj.search([('login', '=', 'admin')])  
user = res_users_obj.browse( user_id[0] )
user.groups_id += [6]
#17, 29, 32, 30] #17 para Packs, 29 para Serial Number, 32 para Stock.moves, 
# 30 poder visualizar los packs y serialnumber en los stock.moves 
oerp.write_record(user)

print 'CARGANDO DATA'

"""
#Cargando Productos
product_obj = oerp.get('product.product')
bom_obj = oerp.get('mrp.bom')

dict_data_product = {'name': '', 'type': 'product', 'uom_id': 1, 'categ_id': 1,
'procure_method': 'make_to_stock', 'supply_method': 'buy', 'uom_po_id': 1}

dict_data_product.update(name='Aceituna')
oerp.create('product.product', dict_data_product )

dict_data_product.update(name='Maiz')
oerp.create('product.product', dict_data_product )

dict_data_product.update(name='Pasapalitos de Pizza')
oerp.create('product.product', dict_data_product )

dict_data_product.update(name='Pizza Pequeña')
oerp.create('product.product', dict_data_product )


dict_data_product.update(name='Tocineta')
oerp.create('product.product', dict_data_product )

# Cargando Mas productos y Componentes del BOM

dict_data_product.update(name='Queso')
product_id = oerp.create('product.product', dict_data_product )
dict_data_bom = {'product_id': product_id, 'product_qty': 5, 'product_uom': 1, 'type': 'normal'}
c1 = oerp.create('mrp.bom', dict_data_bom )

dict_data_product.update(name='Base para pizza')
product_id = oerp.create('product.product', dict_data_product )
dict_data_bom.update(product_id=product_id, product_qty=1)
c2 = oerp.create('mrp.bom', dict_data_bom )

dict_data_product.update(name='Jamon')
product_id = oerp.create('product.product', dict_data_product )
dict_data_bom.update(product_id=product_id, product_qty=3)
c3 = oerp.create('mrp.bom', dict_data_bom )

dict_data_product.update(name='Salsa')
product_id = oerp.create('product.product', dict_data_product )
dict_data_bom.update(product_id=product_id, product_qty=2)
c4 = oerp.create('mrp.bom', dict_data_bom )

# Cargando BOM
dict_data_bom = {'product_uom': 1, 'type': 'normal'}

dict_data_product.update(name='Pizza Sencilla')
product_id = oerp.create('product.product', dict_data_product )
dict_data_bom.update(name='Pizza Sencilla', product_id=product_id, product_qty=1, bom_lines= [(6, 0, [c1, c2, c3, c4])],
routing_id=False )
bom_id = oerp.create('mrp.bom', dict_data_bom )
"""

print 'READY TO USE'
