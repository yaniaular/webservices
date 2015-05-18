# -*- coding: utf-8 -*-
import oerplib

port = 10000
server = '127.0.0.1'
oerp = oerplib.OERP(server=server, port=port)
oerp.config['timeout']=4000
db = raw_input('Do you want to create a new database before continuing? [y/N]:')
db_name = 'ara-debit'
demo_data=True

modules = [
        'account_reconcile_advance',
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
user.groups_id += [6, 22] #6: Technical Features, 22: financial manager
oerp.write_record(user)

ai_obj = oerp.get('account.invoice')
ail_obj = oerp.get('account.invoice.line')
ara_obj = oerp.get('account.reconcile.advance')

av_obj = oerp.get('account.voucher')
avl_obj = oerp.get('account.voucher.line')



#####FC_1
inv_id = ai_obj.create({'type': 'out_invoice', 
                        'partner_id':17, 
                        'journal_id':1, 
                        'account_id':9,
                        'date_invoice': '2013-01-15'
                        }) #17 es Axelor, 1 diario de ventas, 9 cuenta debtors
ail_obj.create({'account_id':25, 
                'quantity':2.0, 
                'price_unit':250, 
                'invoice_id':inv_id, 
                'name': 'Producto 1' 
                })
ail_obj.create({'account_id':25, 
                'quantity':1.0, 
                'price_unit':550, 
                'invoice_id':inv_id, 
                'name': 'Producto 2' 
                })
oerp.exec_workflow('account.invoice','invoice_open',inv_id)
#Fin

#####FC_2
inv_id = ai_obj.create({'type': 'out_invoice', 
                        'partner_id':17, 
                        'journal_id':1, 
                        'account_id':9,
                        'date_invoice': '2013-01-28'
                        })
ail_obj.create({'account_id':25, 
                'quantity':1.0, 
                'price_unit':300, 
                'invoice_id':inv_id, 
                'name': 'Producto 4' 
                })
oerp.exec_workflow('account.invoice','invoice_open',inv_id)
#Fin

#Anticipo_1
ant_id = av_obj.create({'type': 'receipt', 
                        'partner_id':17, 
                        'is_multicurrency': False,
                        'payment_rate_currency_id': 1,
                        'state':'draft',
                        'payment_option':'without_writeoff',
                        'account_id':11,
                        'journal_id':5, 
                        'date':'2013-01-08',
                        'amount':1000.00,
                        'line_cr_ids': [],
                        })
#Fin


#A1
#a cliente 
ara_id = ara_obj.create({'name': 'Ara 1',
                        'type': 'rec',
                        'partner_id':17, 
                        'journal_id':8, 
                        'date': '2013-03-15',
                        'date_post': '2013-03-15'
                        }) # date : fecha creacion documento, date_post: fecha del account.move
#Fin

#A2
ara_id = ara_obj.create({'name': 'Ara 2',
                        'type': 'pay',
                        'partner_id':8, 
                        'journal_id':8, 
                        'date': '2013-05-18',
                        'date_post': '2013-03-15'
                        })
#Fin

######FP1
#inv_id = ai_obj.create({'type': 'in_invoice', 
#                        'partner_id':8, 
#                        'journal_id':3, 
#                        'account_id':17, 
#                        'date_invoice': '2013-01-30'
#                        })# 8 Delta PC, 
#
#ail_obj.create({'account_id':12, 
#                'quantity':1.0, 
#                'price_unit':180, 
#                'invoice_id':inv_id, 
#                'name': 'Producto 3' })
#ail_obj.create({'account_id':12, 
#                'quantity':2.0, 
#                'price_unit':34, 
#                'invoice_id':inv_id, 
#                'name': 'Producto 4' })
#oerp.exec_workflow('account.invoice','invoice_open',inv_id)
#Fin

print 'READY TO USE'
