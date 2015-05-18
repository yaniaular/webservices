import oerplib

oerp = oerplib.OERP(port=10000)
oerp.db.drop('admin','master')
print 'CREANDO BASE DE DATOS MASTER'
oerp.db.create_and_wait('admin','master', demo_data=True)
oerp.login(database='master')
module_obj = oerp.get('ir.module.module')
module_id = module_obj.search([('name', '=', 'base_synchro')])
print 'INSTALANDO BASE SYNCHRO IN MASTER'
module_obj.button_immediate_install(module_id)
print 'CREATING PARTNER IN MASTER'
oerp.create('res.partner',{'name':'Humberto Arocha', 'vat':'VEV149253153'})

oerp2 = oerplib.OERP(port=20000)
oerp2.db.drop('admin','slave')
print 'CREANDO BASE DE DATOS SLAVE'
oerp2.db.create_and_wait('admin','slave', demo_data=False)
oerp2.login(database='slave')
module_obj2 = oerp2.get('ir.module.module')
module_id2 = module_obj2.search([('name', '=', 'base_synchro')])
print 'INSTALANDO BASE SYNCHRO IN SLAVE'
module_obj2.button_immediate_install(module_id2)
print 'CREATING PARTNER IN SLAVE'
oerp2.create('res.partner',{'name':'Jose Morales', 'vat':'VEV220007773'})


print 'CREATING SETTING PROFILE IN SLAVE'
sync_server_id = oerp2.create('base.synchro.server',{'name':'Master Server\
    Sync', 'login':'admin', 'password':'admin', 'server_url':'localhost',
    'server_port':10000, 'server_db':'master'})
model_id = oerp.search('ir.model',[('model','=','res.partner')])[0]
obj_sync_id = oerp2.create('base.synchro.obj',{'name':'Partner Syncing',
    'active':True, 'server_id':sync_server_id, 'model_id':model_id,
    'action':'u','sequence':200, 'domain':'[]'})

print 'SYNCING PARTNERS IN BOTH DIRECTIONS'
base_sync_obj = oerp2.get('base.synchro')
base_sync_id = base_sync_obj.create({'server_url':sync_server_id, 'user_id':1})
base_sync_obj.upload_download_multi_thread([base_sync_id])
print 'YA \'TA'
