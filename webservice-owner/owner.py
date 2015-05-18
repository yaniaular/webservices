# -*- coding: utf-8 -*-
import oerplib
import unicodedata
import argparse
import pdb

parser = argparse.ArgumentParser() 
parser.add_argument("-d", "--db", help="DataBase Name")
parser.add_argument("-r", "--user", help="OpenERP User")
parser.add_argument("-w", "--passwd", help="OpenERP Password")

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


def create_dict_users():
    for u in res_users_obj.browse(user_ids):
        s = unicode(u.name)
        s = unicodedata.normalize("NFKD", s)
        user_name = "".join(c for c in s if ord(c) < 127)
        user_name = " ".join((str(user_name)).lower().split())

        if user_dict.get(user_name, False):
            user_dict[user_name]+=[u.id]
        else:
            user_dict[user_name] = [u.id]


def search_user_by_name(user_name, us_brw):
    user_id = False

    for i in user_dict:
        if user_name in i:
            if (("vauxoo" in i.lower() or "SI" in i) and user_id) or (not user_id): 
                user_id = user_dict[i]
    if not user_id:
        user_id = user_dict.get(user_name, [])


    if not user_id:
        if not us_brw.project_id:
            print "\nNo se puede crear el usuario (%s), porque la historia de usuario (%s) no tiene"\
            "proyecto asignado\n" % (us_brw.owner, us_brw.name)
       # elif not us_brw.project_id.partner_id:
       #     print "\nNo se puede crear el usuario (%s), porque el proyecto (%s) asignado a la historia de"\
       #     " usuario (%s) no tiene partner_id asignado\n" % (us_brw.owner,us_brw.project_id.name,
       #             us_brw.name)
       # elif not us_brw.project_id.partner_id.company_id:
       #     print "\nNo se puede crear el usuario (%s), porque el proyecto (%s) asignado a la historia de"\
       #     " usuario (%s) tiene un partner_id (%s) que no posee company_id\n" % (us_brw.owner,
       #             us_brw.project_id.name,
       #             us_brw.name, us_brw.project_id.partner_id.name)
       # elif us_brw.project_id.partner_id.company_id:
        else:
            permisos = [25]
            if us_brw.project_id.partner_id and not us_brw.project_id.partner_id.customer:
                permisos = [9]

            partner_id = res_partner_obj.search([('name','=',user_name.title())])
            if partner_id:
                partner_id = partner_id[0]
            else:
                partner_id = False

            login = user_name.replace(' ','')

            user_id = res_users_obj.search([('login','=',login)])

            
            if not user_id:
                if us_brw.project_id.partner_id and us_brw.project_id.partner_id.company_id:
                    com_id = us_brw.project_id.partner_id.company_id.id
                else:
                    com_id = us_brw.project_id.company_id.id

                user_id = res_users_obj.create({
                              'name':user_name.title(),
                              'login':login,
                              'company_ids': [com_id],
                              'notification_email_send':'comment',
                              'active': True,
                              'groups_id': [(6,0,permisos)], 
                              'password': '1234',
                              'email': 'temporal@correo.com', 
                              'partner_id' : partner_id,
                            })
    if isinstance(user_id,int):
        user_id = [user_id]
    return user_id

def assing_owner():
    for us in user_storys:
        us_brw = user_story_obj.browse(us)
        s = unicode(us_brw.owner)
        s = unicodedata.normalize("NFKD", s)
        user_name = "".join(c for c in s if ord(c) < 127)
        user_name =  " ".join((str(user_name)).lower().split())
        user_name = user_name.replace('alvares','alvarez')#Abelardo Alvarez con Z
        lista_name = user_name.split(',')
        user_name = lista_name[0].strip()

        user_id = search_user_by_name(user_name, us_brw) 

        print "\n\nHistoria de Usuario " + str(us_brw.id)
        print us_brw.name

        if lista_name:
            print "- Agregar seguidores %s" % lista_name
            for follow in lista_name:
                follow = follow.strip()
                follow_id = search_user_by_name(follow, us_brw)
                user_story_obj.message_subscribe_users([us_brw.id], follow_id)
        
        if user_id:
            if isinstance(user_id, list):
                us_brw.owner_id = user_id[0]
            else:
                us_brw.owner_id = user_id
            print "- El owner_id es " + res_users_obj.browse(us_brw.owner_id.id).name 
            oerp.write_record(us_brw)
            

if __name__ == '__main__':
    print "Aqui Empezamos"

    #Global Variable
    global res_users_obj,user_story_obj,user_storys,user_ids,user_dict

    res_users_obj = oerp.get('res.users')
    user_story_obj = oerp.get('user.story')
    res_partner_obj = oerp.get('res.partner')
    user_storys = user_story_obj.search([])
    user_ids = res_users_obj.search([])
    user_dict = {}

    #Crear diccionario de usuarios, con id y name
    create_dict_users()

    #Asignar owner a las historias de usuario
    assing_owner()    

