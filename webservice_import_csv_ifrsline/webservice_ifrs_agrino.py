import csv
import oerplib

#Reading csv files
ifrs = open('data_ifrs_agrinos.csv') #Se lee el archivo con la data para ifrs
ifrs_line = open('data_ifrsline_agrinos.csv') #Se lee el archivo con la data para las lineas de cada ifrs

ifrs = csv.DictReader(ifrs) #se transforma el csv a un diccionario en python
ifrs_line = csv.DictReader(ifrs_line)#se transforma el csv a un diccionario en python

#Connection Settings
oerp = oerplib.OERP() #instanciar la conexion a la base de datos 
oerp.config['timeout']=4000 #tiempo de espera maximo si no se logra la conexion al servidor



db = raw_input('Deseas crear una base de datos llamada ifrs (sin data demo) donde se instale dicho modulo? [y/N]:')
if db == 'y':                                                                   
    oerp.db.drop('admin','ifrs') #borro bd actual llamada fb                      
    print 'CREATING A NEW DATABASE'                                             
    oerp.db.create_and_wait('admin','ifrs', demo_data=False) #crear base de datos llamada fb con data demo falso
    oerp.login(database='ifrs') #ya el user y passwd por defecto son admin admin  
    module_obj = oerp.get('ir.module.module') #consulto la tabla donde ese guardan los modulos
    module_id = module_obj.search([('name', '=', 'account')])#busco el modulo de fiscal_book
    module_obj.button_immediate_install(module_id) #instalo el modulo           
    fy_id = oerp.execute('account.fiscalyear','create',{
    'name':'2013',                                                              
    'code':'2013',                                                              
    'date_start':'2013-01-01',                                                  
    'date_stop':'2013-12-31',                                                   
    })   
    module_obj = oerp.get('ir.module.module') #consulto la tabla donde ese guardan los modulos
    module_id = module_obj.search([('name', '=', 'ifrs_report')])#busco el modulo de fiscal_book
    module_obj.button_immediate_install(module_id) #instalo el modulo           
else:                                                                           
    oerp.login(database='ifrs')#simplemente entro a la base de datos con user y passwd admin por defecto

ifrs_list = {} 
num = 1


db = raw_input('Deseas cargar informacion adicional en el modulo de ifrs? [y/N]:')

if db == 'y':                                                                   
    for i in ifrs: #Se recorre cada ifrs para agregar a la base de datos
        print "\n %s " % i
        modeli = i.get('model') #modelo donde se creara el registro nuevo (en este caso ifrs.ifrs desde el csv)
        i['do_compute'] = eval(i['do_compute']) #Convierte string en code, ya que el valor False viene como 'False'
        del i['model'] #borro la data del csv que no necesito en el registro a crear
        ifrs_list[num] = oerp.execute(modeli, 'create', i) #Creo el registro en el modelo y guardo el id para usarlo de referencia en las lineas
        num += 1 #numero de control para los ids de los ifrs.ifrs

#se inicializa la lista de lineas para el total
    detail_list = []
    total_of_totals = []
    ifrs_line_list = [] #lista de ids de las lineas para poder borrarlas cuando ya no las necesite
    for l in ifrs_line: #Se recorre las lineas de los ifrs
        modell = l.get('model') #modelo ifrs.lines para este ejemplo (desde el csv)
        nro_ifrs = l.get('nro') #Numero que corresponde al key (en el diccionario ifrs_list) con el valor de id del ifrs que le corresponde a la linea
        
        # varios campos vienen del csv como string, entonces se transforman a codigo
        l['invisible'] = eval( l['invisible'] )
        l['sequence'] = eval( l['sequence'] )
        l['operand_ids'] = eval( l['operand_ids'] )
        l['cons_ids'] = eval( l['cons_ids'] )
        l['analytic_ids'] = eval( l['analytic_ids'] )
        l['inv_sign'] = eval( l['inv_sign'] )
        l['ifrs_id'] = ifrs_list.get(eval(nro_ifrs))
        
        #Si la linea actual es de tipo total, entonces las lineas detail acumuladas se agregar al campo total_ids
        if l.get('type') == 'total' and l.get('id') != '2_18':
            l['total_ids'] = [(6, 0, detail_list)]
            detail_list = []
        elif l.get('type') == 'total' and l.get('id') == '2_18':
            l['total_ids'] = [(6, 0, total_of_totals)]
        else:
            l['total_ids'] = eval( l['total_ids'] )


        #borro la data del csv que no necesito en el registro a crear
        del l['model'] 
        del l['nro']
        
        print l
        ifrs_line_id = oerp.execute(modell, 'create', l )
        # Guardo el id de la linea para poder borrarla mas tarde
        ifrs_line_list.append( ifrs_line_id )
        
        #Si la linea es de tipo detail, entonces la agrego a la lista de details para la linea de total
        if l.get('type') == 'detail':
            detail_list.append(ifrs_line_id)

        if l.get('id') in ('2_1','2_6','2_17'):
            total_of_totals.append(ifrs_line_id)

    db = raw_input('Deseas borrar la informacion adicional que se acaba de cargar en el modulo de ifrs? [y/N]:')
    if db == 'y':
        #Limpieza de los registro que se acaban de crear
        import pdb
        pdb.set_trace()

        for i in ifrs_line_list:
            oerp.unlink(modell, i)

        for i in range(1, len(ifrs_list) + 1):
            oerp.unlink(modeli, ifrs_list.get(i))
            

