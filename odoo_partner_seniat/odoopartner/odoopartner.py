#!/usr/bin/python
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import argparse
import argcomplete
import os
import csv
import oerplib

class OdooPartner(object):

    """
    This object pretend to search and create partners in odoo. The creation
    will return a csv file with the partner.
    """

    epilog = """
    Developed and Planned by Vauxoo
    Odoo Developer Comunity Tool
    Coded by Katherine Zaoral <kathy@vauxoo.com>.
    Coded by Yanina Aular <yani@vauxoo.com>."""

    def __init__(self):
        """
        Initialization of the class.
        @return: None
        """
        self.args = self.argument_parser()
        self.db = self.args['db']
        self.model = self.args['model']
        self.value = self.args['value']
        self.field = self.args['field']
        self.defaults = self.args['defaults']
        self.verbose = self.args['verbose']
        self.confirm_run(self.args)
        return None

    def argument_parser(self, args_list=None):
        """
        This function create the help command line, manage and filter the
        parameters of this script (default values, choices values).
        @return dictionary of the arguments.
        """
        parser = argparse.ArgumentParser(
            prog='odoopartner',
            description='Search/Create res partners in Odoo.',
            epilog=self.epilog,
            formatter_class=argparse.RawTextHelpFormatter)

        query_group = parser.add_argument_group('Query Options',
            'Options needed to make the query the search or the create.')
        server_config_group = parser.add_argument_group('Server Options',
            'Configuration of the odoo instance, server, ports, etc')

        server_config_group.add_argument(
            '-d', '--db',
            metavar='DATABASE',
            type=str,
            required=True,
            help='the name of the data base to be use.')

        query_group.add_argument(
            '-m', '--model',
            metavar='MODEL',
            type=str,
            required=True,
            help='the name of the model that will be consult.')

        query_group.add_argument(
            '-f', '--field',
            metavar='FIELD',
            type=str,
            required=True,
            help='the name of field to do the search.')

        query_group.add_argument(
            '-v', '--value',
            metavar='VALUE',
            # TODO: add this functionality nargs='+',
            type=str,
            required=True,
            help='the value to search.')

        query_group.add_argument(
            '--defaults',
            metavar='DEFAULTS',
            type=str,
            help='the default to create the record if it do not exists.')

        query_group.add_argument(
            '-co', '--company',
            metavar='COMPANY',
            type=str,
            default='mycompany',
            help='the company name. An optional field to be use when creating'
                'the new csv file and the id of the new record'
                ' (default: %(default)s)')

        parser.add_argument(
            '--verbose', action='store_true', 
            help='verbose the run')

        server_config_group.add_argument(
            '-s', '--server',
            metavar='SERVER',
            type=str,
            default='localhost',
            help='the direction of the odoo instance (default: %(default)s)')

        server_config_group.add_argument(
            '--protocol',
            metavar='PROTOCOL',
            type=str,
            default='xmlrpc',
            help='the name of the protocol (default: %(default)s)')

        server_config_group.add_argument(
            '-p', '--port',
            metavar='PORT',
            type=str,
            default='8069',
            help='the name of the data base to be use (default: %(default)s)')

        argcomplete.autocomplete(parser)
        return parser.parse_args(args=args_list).__dict__

    def confirm_run(self, args):
        """
        Manual confirmation before runing the script. Very usefull.
        @param args: dictionary of arguments.
        @return True or exit the program in the confirm is no.
        """
        print'\n... Configuration of Parameters Set'
        for (parameter, value) in args.iteritems():
            print '%s = %s' % (parameter, value)

        confirm_flag = False
        while confirm_flag not in ['y', 'n']:
            confirm_flag = raw_input(
                'Confirm the run with the above parameters? [y/n]: ')
            if confirm_flag == 'y':
                if self.verbose: print 'The script parameters were confirmed by the user'
            elif confirm_flag == 'n':
                if self.verbose: print 'The user cancel the operation'
                exit()
            else:
                print 'The entry is not valid, please enter y or n.'
        return True

    def run(self):
        """
        run the given command in the command line.
        @return True
        """
        oerp = self.server_connection()
        if self.verbose: print 'Login into the data base \'{db}\''.format(**self.args)
        try:
            oerp.login(database=self.db,
		    user='admin',
		    passwd='4dm1n',
		)
        except:
            print 'The sever configuration given is not valid, please check.'
            exit()

        model_obj = oerp.get(self.model)
        imd_obj = oerp.get('ir.model.data')
            #'ir.model.data' model: (id, name, module, model, res_id)
        lines = []
        if self.value[-4:] == '.csv':
            lines = csv.reader(open(self.value))
        else:
            lines.append([self.value])
        #print ' the result of consult the record_id is ', record_id

        value_list = list()
        partner_list = list()
        vat_created = list()
        vat_not_created = list()
        i = 0
        for line in lines:
            i+=1
            line = line[0]
            record_id = model_obj.search([(self.field, '=', line)])

            if record_id or line in vat_created:
                if record_id:
                    record_id = record_id[0]
                    imd_id = imd_obj.search(
                        [('model', '=', self.model), ('res_id', '=', record_id)])
                    imd_id = imd_id and imd_id[0] or False
                    imd_brw = oerp.browse('ir.model.data', imd_id)
                    print i, line, 'exists xml_id  ', imd_brw.name
                else:
                    print i, line, 'exists xml_id  ', 'mycompany_res_partner_', line
            else:
                #if self.verbose: print ' The record do not exist, will be created'
                if self.verbose: print '\nCreating %s' % line

                su_obj = oerp.get('seniat.url')
                if self.field == 'vat':
                    if line in vat_not_created:
                        record_values = False
                    else:
                        try:
                            record_values = su_obj.check_rif(line)
                        except:
                            record_values = False
                    if record_values:
                        # create a new partner with the record_values + defaults
                        csv_lines = self.get_csv_lines(record_values)

                        #Create partner in life (Development temporal)
                        fd = list(csv_lines[0].keys())
                        dt = list(csv_lines[0].values())
                        dt = map(lambda x:x if x!=True else '1',dt)
                        dt = map(lambda x:x if x!=False else '0',dt)
                        mo = fd.index('model')
                        fd.pop(mo)
                        dt.pop(mo)
                        co = fd.index('country_id')
                        #fd.pop(co)
                        fd[co] = 'country_id:id'
                        dt[co] = 'base.ve'

                        result, rows, warning_msg, dummy = model_obj.import_data(
                            fd, [dt], mode='init', current_module='__export__')

                        if result == -1:
                            error_file_name = '{company}_seniat_errors.csv'.format(**self.args)
                            fieldnames = ['value']
                            if line not in vat_not_created:
                                value_list.append({'value': line})
                                vat_not_created.append(line)
                            #if self.verbose: print ' record can not be created, please review', error_file_name
                            if self.verbose: print i, line, ' record can not be created'
                        else:
                            csv_lines[0]['name'] = u''.join(( csv_lines[0].get('name') )).encode('utf-8').strip()
                            partner_list.append( csv_lines[0] )
                            vat_created.append( line )
                            print ' --- CREATED', csv_lines, '\n'
                        #End create

                    else:
                        error_file_name = '{company}_seniat_errors.csv'.format(**self.args)
                        fieldnames = ['value']
                        if line not in vat_not_created:
                            value_list.append({'value': line})
                            vat_not_created.append(line)
                        #if self.verbose: print ' record can not be created, please review', error_file_name
                        if self.verbose: print i, line, ' record can not be created'
        if value_list:
            self.write_csv_file(
                error_file_name, fieldnames, value_list)

        self.write_csv_file(
            '{model2}_seniat.csv'.format(
                model2=self.model.replace('.', '_')),
            self.get_model_fields(),
            partner_list)
        return True

    def write_csv_file(self, filename, fieldnames, csv_lines):
        """
        open/create a csv file and add some csv lines.
        @param filename: the name of the csv file to write.
        @param fieldnames: a list of the csv heades columns.
        @param csv_lines: the csv lines to write.
        """
        with open(filename, 'w') as csvfile:
            wout = csv.DictWriter(csvfile, fieldnames, delimiter=',')
            wout.writerow(dict((fn,fn) for fn in fieldnames))
            for row in csv_lines:
                 wout.writerow(row)
        return True

    def get_csv_lines(self, values):
        """
        return a list of dictionary with the values to fill the
        csv file.
        """
        fieldnames = self.get_model_fields()
        defaults = self.defaults or {}
        res = list()
        # TODO: add this for multiple values for value in self.value:
        line = dict()
        line.update(values)
        line.update(eval(defaults))
        line.update(
            id='{company}_{model2}_{value}'.format(company=self.args.get('company'),model2=self.model.replace('.', '_'), value=values.get('vat')),
            model=self.model,
            country_id='VE',
            active=True,
        )
        line[self.field] = values.get('vat')
        res.append(line)
        return res

    def get_model_fields(self):
        fieldnames = [
            'id', 'model', 'name', 'street', 'street2', 'city',
            'zip', 'country_id', 'state_id', 'vat', 'phone',
            'mobile', 'title', 'function', 'fax', 'website',
            'email', 'lang', 'active', 'ref',
            'property_product_pricelist_purchase',
            'property_product_pricelist', 'property_payment_term',
            'property_supplier_payment_term', 'supplier',
            'customer', 'property_account_receivable',
            'property_account_payable', 'company_id', 'image',
            'islr_withholding_agent', 'spn',
            'property_wh_munici_payable',
            'property_wh_munici_receivable']
        fieldnames.extend(['wh_iva_agent', 'vat_subjected', 'wh_iva_rate'])
        return fieldnames

    def server_connection(self):
        """
        Initialize de odoo server conextion.
        """
        SERVER = self.args['server']
        PROTOCOL = self.args['protocol']
        PORT = self.args['port']

        oerp = oerplib.OERP(
            server=SERVER,
            protocol=PROTOCOL,
            port=PORT)

        oerp.config['timeout'] = 4000
        return oerp

def main():
    obj = OdooPartner()
    obj.run()
    return True

if __name__ == '__main__':
    main()
