# -*- coding: utf-8 -*-
import oerplib

oerp = oerplib.OERP(port=10000)#
oerp.config['timeout']=4000
db = raw_input('Do you want to create a new database before continuing? [y/N]:')
db_name = 'freight'
demo_data=True

modules = [
#        'freight_partner_assign_precise',
        'freight_zone_mapsgoogle',
        ]

if db == 'y':

    print 'BORRANDO BASE DE DATOS VIEJA'
    oerp.db.drop('admin', db_name)
    
    print 'CREATING A NEW DATABASE'
    oerp.db.create_and_wait('admin', db_name, demo_data)
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
oerp.write_record(user)

"""
stock_config_obj = oerp.get('stock_config_settings')
stock_config = stock_config_obj.search([('login', '=', 'admin')])  
stock_permiso = stock_config_obj.create({'write_uid':user_id[0], 'group_stock_packaging':True,
'decimal_precision':2} )
"""

#oerp.write_record(user)

print 'READY TO USE'
