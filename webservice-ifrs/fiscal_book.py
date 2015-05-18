import oerplib
from random import *

oerp = oerplib.OERP()
oerp.config['timeout']=4000
db = raw_input('Do you want to create a new database before continuing? [y/N]:')
if db == 'y':
    oerp.db.drop('admin','ifrs')
    print 'CREATING A NEW DATABASE'
    oerp.db.create_and_wait('admin','ifrs', demo_data=False)
    oerp.login(database='ifrs')
    module_obj = oerp.get('ir.module.module')
    module_id = module_obj.search([('name', '=', 'l10n_ve_fiscal_book')])
    module_obj.button_immediate_install(module_id)
else:
    oerp.login(database='ifrs')

#Enabling printer fiscal in company & Setting VE
oerp.execute('res.company','write',[1],{
    'printer_fiscal':True,
    'vat_check_vies':True,
    })

#Creating Purchase Journal
purchase_journal_id = oerp.execute('account.journal','create',{
    'name':'Purchase Journal',
    'type':'purchase',
    'code':'purchase',
    })

purchase_wh_journal_id = oerp.execute('account.journal','search',[('type','=','iva_purchase')])
purchase_wh_journal_id = purchase_wh_journal_id and purchase_wh_journal_id[0] or False   


#Creating Sale Journal
journal_id = oerp.execute('account.journal','create',{
    'name':'Sale Journal',
    'type':'sale',
    'code':'sale',
    })

wh_journal_id = oerp.execute('account.journal','search',[('type','=','iva_sale')])
wh_journal_id = wh_journal_id and wh_journal_id[0] or False   


#Searching Receivable & Payable Account Type
rec = oerp.execute('account.account.type','search',[('code','=','receivable')])
rec = rec and rec[0] or False

pay = oerp.execute('account.account.type','search',[('code','=','payable')])
pay = pay and pay[0] or False

exp = oerp.execute('account.account.type','search',[('code','=','expense')])
exp = exp and exp[0] or False

inc = oerp.execute('account.account.type','search',[('code','=','income')])
inc = inc and inc[0] or False

tax = oerp.execute('account.account.type','search',[('code','=','tax')])
tax = tax and tax[0] or False

#Creating Receivable & Payable Account 
rec_id = oerp.execute('account.account','create',{
    'user_type':rec,
    'name': 'Receivable',
    'type': 'receivable',
    'code': '1001'
    })

pay_id = oerp.execute('account.account','create',{
    'user_type':pay,
    'name': 'Payable',
    'type': 'payable',
    'code': '2001'
    })

purchase_prod_acc_id = oerp.execute('account.account','create',{
    'user_type':exp,
    'name': 'Expense',
    'type': 'other',
    'code': '5001'
    })

prod_acc_id = oerp.execute('account.account','create',{
    'user_type':inc,
    'name': 'Income',
    'type': 'other',
    'code': '4001'
    })

purchase_tax_id = oerp.execute('account.account','create',{
    'user_type': tax,
    'name': 'PURCHASE VAT',
    'type': 'other',
    'code': '1501'
    })

tax_id = oerp.execute('account.account','create',{
    'user_type': tax,
    'name': 'VAT',
    'type': 'other',
    'code': '2501'
    })

purchase_wh_tax_id = oerp.execute('account.account','create',{
    'user_type': tax,
    'name': 'PURCHASE VAT WH',
    'type': 'other',
    'code': '1502'
    })

wh_tax_id = oerp.execute('account.account','create',{
    'user_type': tax,
    'name': 'VAT WH',
    'type': 'other',
    'code': '2502'
    })

#Creating Purchase Taxes
purchase_tax_ids = []
for tt in [('exento',0),('reducido',8),('general',12),('adicional',22)]:
    purchase_tax_ids.append(oerp.execute('account.tax','create',{
        'name':'%s PERC - PURCHASE'%tt[1],
        'type_tax_use':'purchase',
        'active':True,
        'appl_type':tt[0],
        'ret':bool(tt[1]),
        'type':'percent',
        'amount':tt[1]/100.0,
        'sequence':tt[1],
        'account_collected_id':purchase_tax_id,
        'account_paid_id':purchase_tax_id,
        'wh_vat_collected_account_id':purchase_wh_tax_id,
        'wh_vat_paid_account_id':purchase_wh_tax_id,
    }))

#Creating Sale Taxes
tax_ids = []
for tt in [('exento',0),('reducido',8),('general',12),('adicional',22)]:
    tax_ids.append(oerp.execute('account.tax','create',{
        'name':'%s PERC'%tt[1],
        'type_tax_use':'sale',
        'active':True,
        'appl_type':tt[0],
        'ret':bool(tt[1]),
        'type':'percent',
        'amount':tt[1]/100.0,
        'sequence':tt[1],
        'account_collected_id':tax_id,
        'account_paid_id':tax_id,
        'wh_vat_collected_account_id':wh_tax_id,
        'wh_vat_paid_account_id':wh_tax_id,
    }))

#Creating Partners
customers=[]
customers.append(oerp.execute('res.partner','create',{
    'name':'Tax Payer',
    'property_account_payable':pay_id,
    'property_account_receivable':rec_id,
    'vat_subjected': True,
    'vat':'VEJ317520882'
    }))

customers.append(oerp.execute('res.partner','create',{
    'name':'Non Tax Payer',
    'property_account_payable':pay_id,
    'property_account_receivable':rec_id,
    'vat_subjected': False,
    'vat':'VEV14925315'
    }))

customers.append(oerp.execute('res.partner','create',{
    'name':'Non Tax Payer',
    'property_account_payable':pay_id,
    'property_account_receivable':rec_id,
    'vat_subjected': False,
    'vat':'VEJ308754102'
    }))

for customer in customers:
    oerp.execute('res.partner','button_check_vat',[customer])

#Creating FiscalYear & Periods
fy_id = oerp.execute('account.fiscalyear','create',{
    'name':'2013',
    'code':'2013',
    'date_start':'2013-01-01',
    'date_stop':'2013-12-31',
    })

oerp.execute('account.fiscalyear','create_period',[fy_id])

period_id = oerp.execute('account.period','search',[('date_start','<=','2013-06-20')])

period_id = period_id and period_id[-1] or []

#Instantiating Invoice Object
inv_obj = oerp.get('account.invoice')

#Creating Purchase Invoices for each date of month
purchase_inv_list = []
purchase_dates = map(lambda x:'2013-06-%s'%(x+1),range(30)) 
purchase_dates = sample(purchase_dates,randint(1,len(purchase_dates))) 
purchase_dates.sort()
emission_dates = map(lambda x:'2013-03-%s'%(x+1),range(31))+ \
                 map(lambda x:'2013-05-%s'%(x+1),range(31))+ \
                 map(lambda x:'2013-06-%s'%(x+1),range(30))
purchase_oper = lambda a=None: randint(0,10)
qty = lambda a=None: randint(1,10)
nro_ctrl = lambda a=None:randint(100000000,999999999)
purchase_stax = lambda a=None: sample(purchase_tax_ids,1)
for each_date in purchase_dates:
    while True:
        date_document = sample(emission_dates,1)[0]
        if date_document<=each_date: break 
    for op in range(purchase_oper()):
        customer = sample(customers,1)[0]
        purchase_inv_list.append({
            'type':'in_invoice',
            'partner_id':customer,
            'date_invoice':each_date,
            'date_document':date_document,
            'journal_id':purchase_journal_id,
            'account_id':pay_id,
            'nro_ctrl': nro_ctrl(),
            'invoice_line':[(0,0,{
                'name':'PRODUCTO',
                'account_id':purchase_prod_acc_id,
                'quantity':qty(),
                'price_unit':70,
                'invoice_line_tax_id':[(4,purchase_stax()[0])],
                })]
            })


purchase_inv_ids=[]
print 'CREATING %s INVOICES'%len(purchase_inv_list)
i=0
for inv in purchase_inv_list:
    i+=1
    print 'CREATING INVOICE %s/%s'%(i,len(purchase_inv_list))
    purchase_inv_ids.append(inv_obj.create(inv))

i=0
for inv in purchase_inv_ids:
    i+=1
    print 'VALIDATING INVOICE %s/%s'%(i,len(purchase_inv_list))
    oerp.exec_workflow('account.invoice','invoice_open',inv)

#Creating Invoices for each date of month
inv_list = []
dates = map(lambda x:'2013-06-%s'%(x+1),range(30))
dates = sample(dates,randint(1,len(dates)))
printers = [False, 'MHXNY', 'JHPQT', 'KJVAF']    
oper = lambda a=None: randint(0,10)
qty = lambda a=None: randint(1,10)
stax = lambda a=None: sample(tax_ids,1)
series_by_printer = {}.fromkeys(printers,0)
z_by_printer = {}.fromkeys(printers,10000)
z_flags = {}.fromkeys(printers,False)
nro_ctrl = 0
for each_date in dates:
    for op in range(oper()):
        printer = sample(printers,1)[0]
        if not z_flags[printer]:
            z_flags[printer]= True
            z_by_printer[printer] += 1
        customer = sample(customers,1)[0]
        series_by_printer[printer]+=1
        nro_ctrl = not printer and nro_ctrl+1 or nro_ctrl
        inv_list.append({
            'type':'out_invoice',
            'partner_id':customer,
            'date_invoice':each_date,
            'date_document':each_date,
            'journal_id':journal_id,
            'account_id':rec_id,
            'invoice_printer':printer and series_by_printer[printer] or False,
            'fiscal_printer':printer or False,
            'z_report':printer and z_by_printer[printer] or False,
            'nro_ctrl': not printer and nro_ctrl or series_by_printer[printer],
            'invoice_line':[(0,0,{
                'name':'PRODUCTO',
                'account_id':prod_acc_id,
                'quantity':qty(),
                'price_unit':100,
                'invoice_line_tax_id':[(4,stax()[0])],
                })]
            })
    z_flags = {}.fromkeys(printers,False)
inv_ids=[]
print 'CREATING %s INVOICES'%len(inv_list)
i=0
for inv in inv_list:
    i+=1
    print 'CREATING INVOICE %s/%s'%(i,len(inv_list))
    inv_ids.append(inv_obj.create(inv))

for inv in inv_ids:
    print 'VALIDATING INVOICE %s/%s'%(inv,len(inv_list))
    oerp.exec_workflow('account.invoice','invoice_open',inv)

#CREATING IVA WITHHOLDING FOR CUSTOMERS
wh_partner_id = oerp.execute('res.partner','search',[
    ('wh_iva_agent','=',True),
    ('customer','=',True),
    ])
wh_partner_id = wh_partner_id and wh_partner_id[0] or False 
wh_ochg_pid = wh_partner_id and oerp.execute('account.wh.iva',\
    'onchange_partner_id',[],'out_invoice',wh_partner_id).get('value') 

wh = all(wh_ochg_pid.values())
if wh:
    wh_lines = map(lambda x:(0,0,x),sample(
            wh_ochg_pid['wh_lines'],
            randint(1, len(wh_ochg_pid['wh_lines'])>10 and 10 \
                    or len(wh_ochg_pid['wh_lines']))))
    account_id = wh_ochg_pid['account_id']

iva_wh_doc_id = wh and oerp.execute('account.wh.iva','create',{
    'journal_id':wh_journal_id, 
    'type':'out_invoice', 
    'partner_id':wh_partner_id,
    'company_id':1, 
    'currency_id':1, 
    'name':'VAT WH FOR PARTNER %s'%wh_partner_id,
    'number':'2013-05-00007646',
    'account_id':account_id, 
    'wh_lines':wh_lines, 
    })

oerp.execute('account.wh.iva','compute_amount_wh',[iva_wh_doc_id])
oerp.exec_workflow('account.wh.iva','wh_iva_confirmed',iva_wh_doc_id)
oerp.exec_workflow('account.wh.iva','wh_iva_done',iva_wh_doc_id)


#CREATING SALE FISCAL BOOK
print 'CREATING FISCAL BOOK'
fb_id = oerp.execute('fiscal.book','create',{
    'name':'Fiscal Book (TEST)',
    'period_id': period_id,
    'type':'sale',
    })
print 'GENERATING BOOK'
try:
    oerp.execute('fiscal.book','update_book',[fb_id])
except:
    print 'HOUSTON WE\'VE GOT A PROBLEM'
