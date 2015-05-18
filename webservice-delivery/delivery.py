# -*- coding: utf-8 -*-
import oerplib

def _get_image( name):
    fil = open(name, 'rb')
    data = fil.read()
    fil.close()
    binary = data.encode('base64')
    return binary 

def cog_instance(clase, data, field_unique, value):
    class_obj = oerp.get(clase)
    class_id = class_obj.search( [(field_unique, '=', value )] )
    if not class_id:
        class_id = class_obj.create( data )
    else:
        class_id = class_id[0]
    return class_id

oerp = oerplib.OERP()
oerp.config['timeout']=4000
db = raw_input('Do you want to create a new database before continuing? [y/N]:')
db_name = 'delivery'
modules = [
        'sale', 
        'purchase',
        'point_of_sale',
        ]

if db == 'y':

    print 'BORRANDO BASE DE DATOS VIEJA'
    oerp.db.drop('admin', db_name)
    
    print 'CREATING A NEW DATABASE'
    oerp.db.create_and_wait('admin', db_name, demo_data=True)
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

print 'CARGANDO DATA'
pos_category = oerp.get('pos.category')
########################

category_data = { 'name': 'JAPONES', 'image_medium': _get_image('asia.jpg') }
category_id = cog_instance('pos.category', category_data, 'name', 'JAPONES')
son_id =  pos_category.search( [('name', '=', 'Beverages')] )
pos_category.write(son_id, {'parent_id': category_id }  )

########################
category_data = { 'name': 'MEXICANO', 'image_medium': _get_image('mexico.jpg') }
category_id = cog_instance('pos.category', category_data, 'name', 'MEXICANO') 

son_id =  pos_category.search( [('name', '=', 'Food')] )
pos_category.write(son_id, {'parent_id': category_id }  )

son_id =  pos_category.search( [('name', '=', 'Others')] )
pos_category.write(son_id, {'parent_id': category_id }  )

########################
category_data = { 'name': 'POSTRES', 'image_medium': _get_image('postre.jpg') }
category_id = cog_instance('pos.category', category_data, 'name', 'POSTRES') 

son_id =  pos_category.search( [('name', '=', 'Fresh Fruits')] )
pos_category.write(son_id, {'parent_id': category_id }  )

son_id =  pos_category.search( [('name', '=', 'Fresh vegetables')] )
pos_category.write(son_id, {'parent_id': category_id }  )

print 'READY TO USE'
