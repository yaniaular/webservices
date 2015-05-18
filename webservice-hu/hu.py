# -*- coding: utf-8 -*-
import oerplib
import unicodedata
import csv
import pdb
import argparse

parser = argparse.ArgumentParser() 
parser.add_argument("-d", "--db", help="DataBase Name", required=True)
parser.add_argument("-r", "--user", help="OpenERP User", required=True)
parser.add_argument("-w", "--passwd", help="OpenERP Password", required=True)
parser.add_argument("-us", "--userstory", help="Name user story csv file", required=True)
parser.add_argument("-proc", "--process", help="Name process csv file")
parser.add_argument("-proj", "--project", help="project ID", required=True)
parser.add_argument("-a", "--assistant", help="Assistant csv", required=True)
parser.add_argument("-su", "--supervisor", help="supervisor csv", required=True)
parser.add_argument("-e", "--execution", help="execution csv", required=True)

parser.add_argument("-s", "--server", help="Server IP, 127.0.0.1 for default", default="127.0.0.1")
parser.add_argument("-p", "--port", type=int, help="Port, 8069 for default", default="8069")
parser.add_argument("-t", "--timeout", type=int, help="Timeout, 4000 for default", default="4000")

args = parser.parse_args()

if( args.db is None or args.user is None or args.passwd is None):
    print "Must be specified DataBase, User and Password"
    quit()
db_name = args.db
user = args.user
passwd = args.passwd

server = args.server
port = args.port
timeout = args.timeout

oerp = oerplib.OERP(server=server, port=port, timeout=timeout)
oerp.login(user=user, passwd=passwd , database=db_name)
#pro_obj = oerp.get("project.project")

pri = csv.DictReader(open("prioridad.csv"))
prioridades = {}
pri_obj = oerp.get("user.story.priority") 

for p in pri:
    pri_id = pri_obj.search( [('name', '=', p.get('name'))] )
    if not pri_id:
        pri_id = pri_obj.create( {
        'name': p.get('name'),
        })
    prioridades[p.get('id')] = pri_id
        
def cargar_hu(file_csv, d_tag, process_csv, project_id, supervisor, execution):
    """
    Solo puede haber un campo id por cada archivo csv (Por ahora)
    """
    procesos_hu = {}
    if process_csv:
        proc_csv = csv.DictReader(open(process_csv))
        for proc in proc_csv:
            procesos_hu[ int(proc.get('HU ID')) ] = proc.get('Procesos')

    model_obj = oerp.get("user.story")
    acc_obj = oerp.get("acceptability.criteria")
    cat_obj = oerp.get("project.category")

    project_obj = oerp.get("project.project")
    account_obj = oerp.get("account.analytic.account")
    res_users_obj = oerp.get("res.users")

    doc_tags = csv.DictReader(open(d_tag))
    dict_yo = {}
    dict_tags = {}

    for ta in doc_tags:
        dict_yo[int(ta.get('id'))] = ta.get('name')
        tag_id = cat_obj.search( [('name', '=', ta.get('rol'))] )
        if not tag_id:
            dict_tags[int(ta.get('id'))] = cat_obj.create( {
            'name': ta.get('rol'),
            })
        else:
            dict_tags[int(ta.get('id'))] = tag_id[0]

    lines = csv.DictReader(open(file_csv))
    ids = {}
    vez_primera = False
    for line in lines:
        if not vez_primera:
            field_names = line.keys()
            if '' in field_names:
                field_names.remove('')
            if None in field_names:
                field_names.remove(None)
            vez_primera = True

        acc_list = []
        categ_ids = []
        element = {}.fromkeys(['user_id','user_execute_id','info','planned_hours','name','description','owner','date','priority_level','code'], '')
        desarrollo_criterio = 'NO'
        criterios = ''
        dificultad_criterio = 'NO APLICA'

        for field_name in field_names:
            if 'ID' in field_name:
                if line[field_name]:
                    element['code'] = int(line[field_name])
            if 'Historias de Usuario' in field_name:
                if line[field_name]:
                    texto = line[field_name]
                    for i in dict_tags.keys():
                        if str(i) in texto:
                            if dict_yo.get(i):
                                categ_ids.append( dict_tags.get(i))
                                texto = texto.replace(str(i), dict_yo.get(i) )
                                if element['owner']:
                                    element['owner'] += ', ' + dict_yo.get(i)
                                else:   
                                    element['owner'] = dict_yo.get(i)

                    element['name'] = texto
                    element['description'] = texto
            if "Estimación (min)" in field_name:
                if line[field_name]:
                    element['planned_hours'] = float(line[field_name])/60.0
            if "Observaciones Técnicas" in field_name:
                if line[field_name]:
                    element['info'] = line[field_name]
            if "Prioridad" in field_name:
                if line[field_name]:
                    if isinstance(prioridades.get(line[field_name]), list):
                        element['priority_level'] = prioridades.get(line[field_name])[0]
                    else:
                        element['priority_level'] = prioridades.get(line[field_name])
            if "date" in field_name:
                if line[field_name] is False or line[field_name] is None or line[field_name] == '':
                    element['date'] = fecha  
                else:
                    fecha = line[field_name]
                    element['date'] = fecha
            if "Criterios de Aceptación" in field_name:
                if line[field_name]:
                    criterios = line[field_name]   
            if "Nivel de Dificultad" in field_name:
                if line[field_name]:
                    dificultad_criterio = line[field_name]
            if "Existe" in field_name:
                if line[field_name]:
                    desarrollo_criterio = line[field_name] 
            #if "Check" in field_name:


        analytic_id = account_obj.search( [('name', '=' ,project_id)]  )

        supervisor_id = res_users_obj.search([('name', '=' ,supervisor)])
        execution_id = res_users_obj.search([('name', '=' ,execution)])

        if not supervisor_id:
            print "\n"*2
            print "NO SE ENCONTRO EL SUPERVISOR ASOCIADO"
            print "\n"*2
            exit()

        if not execution_id:
            print "\n"*2
            print "NO SE ENCONTRO EL RESPONSABLE DE EJECUCION ASOCIADO"
            print "\n"*2
            exit()

        element['user_id'] = supervisor_id[0]
        element['user_execute_id'] = execution_id[0]
        element['categ_ids'] = [(6,0,categ_ids)]
        
        proceso_de_hu = procesos_hu.get( element.get('code')  )
        if proceso_de_hu:
            element['implementation'] =  proceso_de_hu

        #project_id = pro_obj.create({
        #    'name' : project_name,
        #    'privacy_visibility': 'employees',
        #    })
        #element['project_id'] = project_id

        analytic_id = account_obj.search( [('name', '=' ,project_id)]  )
        if not analytic_id:
            print "\n"*2
            print "NO SE ENCONTRO EL PROYECTO ASOCIADO!!"
            print "\n"*2
            exit()

        pro_id = project_obj.search( [('analytic_account_id','=',analytic_id[0])] )
        
        element['project_id'] = pro_id[0]

        dict_search = []
        for k,v in element.iteritems():
            if 'ids' not in k and v:
                if k != 'name' and k != 'owner':
                    dict_search.append( (k, '=', v) )

        
        ele_id = model_obj.search( dict_search )
        if not ele_id:
            element_id = model_obj.create(element)
        else:
            element_id = ele_id[0]

        if isinstance(dificultad_criterio, str):
            dificultad_criterio = dificultad_criterio.split('\n')
        if isinstance(desarrollo_criterio, str):
            desarrollo_criterio = desarrollo_criterio.split('\n')
        i = 0
        for ac in criterios.split('\n'):
            dificultad = 'na'
            desarrollo = False

            if len(dificultad_criterio) > i:
                dificultad = dificultad_criterio[i]
                if dificultad == 'BAJA':
                    dificultad = 'low'
                elif dificultad == 'MEDIA':
                    dificultad = 'medium'
                elif dificultad == 'ALTA':
                    dificultad = 'high'
                else:
                    dificultad = 'na'

            if len(desarrollo_criterio) > i:
                desarrollo = desarrollo_criterio[i]
                if desarrollo == 'YES':
                    desarrollo = True
                else:
                    desarrollo = False


            acc_dict = {
                    'name': ac,
                    'scenario' : ac,
                    'accep_crit_id': element_id,
                    'difficulty' : dificultad,
                    'development' : desarrollo,
                    }
            
            dict_search = []
            for k,v in acc_dict.iteritems():
                if 'ids' not in k and v:
                    if k != 'name':
                        dict_search.append( (k, '=', v) )

            a_id = acc_obj.search( dict_search )
            if not a_id:
                acc_id =  acc_obj.create(acc_dict)
            i+=1

    return ids

print "User Story Document:", args.userstory
print "Project ID:", args.project
print "Process Document:", args.process
print "Assistant Document:", args.assistant
print "Supervisor", args.supervisor
print "Responsable de ejecucion", args.execution

if args.process is None:
    process = False

cargar_hu(args.userstory, args.assistant, args.process, args.project, args.supervisor, args.execution)
