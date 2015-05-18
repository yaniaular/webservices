# -*- coding: utf-8 -*-
import oerplib

oerp = oerplib.OERP()
oerp.config['timeout']=4000
db = raw_input('Do you want to create a new database before continuing? [y/N]:')
if db == 'y':

    print 'BORRANDO BASE DE DATOS VIEJA'
    oerp.db.drop('admin','mrp_cluster_database')
    
    print 'CREATING A NEW DATABASE'
    oerp.db.create_and_wait('admin','mrp_cluster_database', demo_data=False)
    oerp.login(database='mrp_cluster_database')
    
    print 'INSTALANDO MODULOS'
    module_obj = oerp.get('ir.module.module')

    module_id = module_obj.search([('name', '=', 'mrp')])
    module_obj.button_immediate_install(module_id)

    module_id = module_obj.search([('name', '=', 'mrp_operations')])
    module_obj.button_immediate_install(module_id)

    module_id = module_obj.search([('name', '=', 'mrp_consume_produce')])
    module_obj.button_immediate_install(module_id)
    
    module_id = module_obj.search([('name', '=', 'mrp_byproduct')])
    module_obj.button_immediate_install(module_id)


else:
    oerp.login(database='mrp_cluster_database')

print 'ESTABLECIENDO PERMISOS'
res_users_obj = oerp.get('res.users')
user_id = res_users_obj.search([('login', '=', 'admin')])  
user = res_users_obj.browse( user_id[0] )
user.groups_id += [2, 1, 6, 3, 19, 20, 25, 28, 27, 34, 33, 37, 36, 6, 32, 38, 15, 16, 42] 
oerp.write_record(user)

print 'CARGANDO DATA'

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

print 'READY TO USE'
