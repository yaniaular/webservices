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


def process():

    partner_obj = oerp.get('res.partner')
    list_name = []
    for hu in user_story_obj.search([]):
        hu = user_story_obj.browse(hu)
        follow_ids = hu.project_id.message_follower_ids
        if hu:
            print "HU Bien ", "Id HU: ", hu.id 
        if hu.project_id:
            print "hu.project_id Bien"
        if hu.project_id.message_follower_ids:
            print "hu.project_id.message_follower_ids Bien"

        pdb.set_trace()
        print follow_ids.ids

        if follow_ids:
            user_story_obj.message_subscribe([hu.id], follow_ids.ids)

       # for i in follow_ids.ids:
       #     if partner_obj.browse(i).name not in list_name:
       #         print partner_obj.browse(i).name
       #         list_name.append(partner_obj.browse(i).name)

        #mail_id = mail_obj.create({
        #    'model': 'user.story',
        #    'res_id': hu.id,
        #    'subject': 'Invitation to follow %s' %
        #                           hu.name,
        #    'body_html': 'You have been invited to follow %s' % hu.name,
        #    'auto_delete': True,
        #                           })
        #mail_obj.send([mail_id], recipient_ids=follow_ids.ids)


if __name__ == '__main__':
    global project_obj
    project_obj = oerp.get('project.project')
    global user_story_obj 
    user_story_obj = oerp.get('user.story')
    mail_obj = oerp.get('mail.mail')
    mail_wizard_obj = oerp.get('mail.wizard.invite')


    process()

