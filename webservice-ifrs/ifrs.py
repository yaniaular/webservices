import oerplib

oerp = oerplib.OERP()
oerp.config['timeout']=4000
db = raw_input('Do you want to create a new database before continuing? [y/N]:')
if db == 'y':
    oerp.db.drop('admin','ifrs')
    print 'CREATING A NEW DATABASE'
    oerp.db.create_and_wait('admin','ifrs', demo_data=True)
    oerp.login(database='ifrs')
    module_obj = oerp.get('ir.module.module')
    module_id = module_obj.search([('name', '=', 'ifrs_report')])
    module_obj.button_immediate_install(module_id)
else:
    oerp.login(database='ifrs')
print 'READY TO USE'
