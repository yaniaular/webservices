import oerplib
oerp = oerplib.OERP()
oerp.db.drop('admin','alucasa')
print 'CREATING A NEW DATABASE'
oerp.db.create_and_wait('admin','alucasa', demo_data=False)
oerp.login(database='alucasa')
module_obj = oerp.get('ir.module.module')
module_id = module_obj.search([('name', '=', 'alucasa')])

print 'GIVING ADMINISTRATOR TECHNICAL FEATURES PRIVILEGES'
oerp.write('res.users',1,{'in_group_6':True})

print 'INSTALLING MODULE ISO MANAGEMENT'
module_obj.button_immediate_install(module_id)
module_id = module_obj.search([('name', '=', 'iso_management')])
module_obj.button_immediate_install(module_id)

for i in range(3):
    print 10*'*'
n=1

print 'CREATING A NEW INDICATOR TREE'
imi_obj = oerp.get('iso.management.indicator')
imi_id = imi_obj.create({'name':'Indicator Tree %s'%n, 'start_date':'2013-05-01'})
print 'INDICATOR STATE', imi_obj.browse(imi_id).state
for i in range(3):
    print 10*'*'

print 'PRESSING BUTTON ON WORKFLOW FOR INDICATOR TREE RECORD'
oerp.exec_workflow('iso.management.indicator','confirm',imi_id)
print 'INDICATOR STATE', imi_obj.browse(imi_id).state
for i in range(3):
    print 10*'*'

print 'CREATING A NEW CARD FROM WIZARD - FIRST STEP'
imii_obj = oerp.get('iso.management.indicator.id')
imii_id = imii_obj.create({'indicator_id':imi_id})
imii_res = imii_obj.next([imii_id])

print 'INDICATOR STATE', imi_obj.browse(imi_id).state
print 'CREATING A NEW CARD FROM WIZARD - SECOND STEP - START'
imciw_obj = oerp.get('iso.management.card.indicator.wizard')
imciw_id = imciw_obj.create({'indicator_objective':'Indicator Objetive%s'%n,
    'start_date':'2013-05-03', 'simple_indicator':'7', 'indicator_id':imi_id},
    context=imii_res['context'])
print 'INDICATOR STATE', imi_obj.browse(imi_id).state

print 'CREATING A NEW CARD FROM WIZARD - SECOND STEP - END'
oerp.execute('iso.management.card.indicator.wizard','save',[imciw_id],imii_res['context'])
print 'INDICATOR STATE', imi_obj.browse(imi_id).state
for i in range(3):
    print 10*'*'

imci_obj = oerp.get('iso.management.card.indicator')
print 'CARD INDICATOR STATE ', imci_obj.browse(n).state

print 'PRESSING CONFIRM BOTON ON INDICATOR CARD'
oerp.exec_workflow('iso.management.card.indicator','confirm',n)


print 'INDICATOR STATE', imi_obj.browse(imi_id).state
for i in range(10):
    print 10*'*'
print 'PRESSING ANNUL BOTON ON INDICATOR CARD'
oerp.exec_workflow('iso.management.card.indicator','annul',n)


print 'INDICATOR STATE', imi_obj.browse(imi_id).state
