# -*- coding: utf-8 -*-
import oerplib

oerp = oerplib.OERP(port=8000)#
oerp.config['timeout']=4000
db = raw_input('Do you want to create a new database before continuing? [y/N]:')
db_name = 'cicsa_demo'
demo_data=True

modules = [
        'account_analytic_plans',
#        'cicsa_purchase_requisition_webkit_report',
#         'cicsa_data',
#        'bdp_purchase_requisition',
#        'cicsa_purchase_requisition_workflow',
#        'purchase_requisition_line_analytic',
#        'purchase_requisition_line_description',
#        'purchase_order_change_management',
#        'cicsa_data',
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

#~print 'DESINSTALANDO MODULOS'
#~module_obj = oerp.get('ir.module.module')
#~
#~for mod in modules:
#~    module_id = module_obj.search([('name', '=', mod)])
#~    module_obj.button_immediate_uninstall(module_id)
#~
#~print 'INSTALANDO MODULOS'
#~module_obj = oerp.get('ir.module.module')
#~
#~for mod in modules:
#~    module_id = module_obj.search([('name', '=', mod)])
#~    module_obj.button_immediate_install(module_id)

print 'ESTABLECIENDO PERMISOS'
res_users_obj = oerp.get('res.users')
user_id = res_users_obj.search([('login', '=', 'admin')])  
user = res_users_obj.browse( user_id[0] )
user.groups_id += [6]
#~user.groups_id += [37]
oerp.write_record(user)

"""
employee_obj = oerp.get('hr.employee')
employee_id = employee_obj.search([('name', '=', 'Administrator')])  
employee = employee_obj.browse( employee_id[0] )
employee.category_ids = [(6, 0, range(6,18))]
oerp.write_record(employee)
"""

"""
stock_config_obj = oerp.get('stock_config_settings')
stock_config = stock_config_obj.search([('login', '=', 'admin')])  
stock_permiso = stock_config_obj.create({'write_uid':user_id[0], 'group_stock_packaging':True,
'decimal_precision':2} )
"""

#oerp.write_record(user)

print 'READY TO USE'
