from odoo import models, api, fields
from datetime import datetime, timedelta

'''
    inventory_product_report" is folder name and "main_store_product" is model name
'''


class WizardProductDeliver(models.TransientModel):
    _name = 'inventory.main_store_product.report'

    start_date = fields.Datetime(string='From Date')
    end_date = fields.Datetime(string='End Date')
    locat_id = fields.Many2one('stock.location', string='Location')
    opening_balance_date = fields.Datetime(string='Date of Opening Balance')
    quantity = fields.Integer(string='Quantity')
    product_ids = fields.Integer(string='product_ids')

    @api.multi
    def print_report(self, data):
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
        start_dates = start_date.strftime("%Y-%m-%d")

        stock_move = self.env['stock.move'].search([],limit =1 ,order ='id asc')
        most_starting_date = stock_move.create_date
        most_start_date = datetime.strptime(most_starting_date, "%Y-%m-%d %H:%M:%S")
        most_start_dates = most_start_date.strftime("%Y-%m-%d")

        # previous balance calculation
        if most_start_dates == start_dates:
            before_most_starting_date = datetime.strptime(most_starting_date, "%Y-%m-%d %H:%M:%S") + timedelta(days=-1)
            before_most_starting_dates = before_most_starting_date.strftime("%Y-%m-%d")
            after_most_starting_date = datetime.strptime(most_starting_date, "%Y-%m-%d %H:%M:%S") + timedelta(days=1)
            after_most_starting_dates = after_most_starting_date.strftime("%Y-%m-%d")
            stock_moves = self.env['stock.move'].search([('location_dest_id', '=', self.locat_id.id), \
                                                        ('create_date', '>',before_most_starting_dates), \
                                                         ('create_date', '<',after_most_starting_dates)])
            product_ids = set()
            for products in stock_moves:
                product_ids.add(products.product_id)

            list = []
            for product in product_ids:
                if product.product_tmpl_id.active == True:
                    stock_move = self.env['stock.move'].search([('location_dest_id', '=', self.locat_id.id), \
                                                                ('create_date', '>', before_most_starting_dates),\
                                                                ('create_date', '<', after_most_starting_dates), \
                                                                ('state', '=', 'done'), \
                                                                ('product_id', '=', product.id)])
                    dicts = {}
                    qty = 0
                    for mv in stock_move:
                        qty += mv.product_qty

                    dicts['name'] = product.product_tmpl_id.name
                    dicts['product_id'] = product.id
                    dicts['previous_balance'] = qty
                    list.append(dicts)

            purchase_list = []
            for product in product_ids:
                if product.product_tmpl_id.active == True:
                    stock_move = self.env['stock.move'].search([('location_dest_id', '=', self.locat_id.id), \
                                                                ('create_date', '>', before_most_starting_dates),\
                                                                ('create_date', '<', after_most_starting_dates), \
                                                                ('product_id', '=', product.id), \
                                                                ('state', '=', 'done')])

                    purchase_dict = {}

                    quantity = 0
                    for mv in stock_move:
                        quantity += mv.product_qty
                    purchase_dict['product_id'] = product.id
                    purchase_dict['previous_balance'] = quantity
                    purchase_list.append(purchase_dict)

            for datas in list:
                for purchase_data in purchase_list:
                    if datas['product_id'] == purchase_data['product_id']:
                        datas['previous_balance'] = datas['previous_balance'] - purchase_data['previous_balance']

        else:
            product_ids = set()
            stock_move = self.env['stock.move'].search([('location_dest_id', '=', self.locat_id.id), \
                                                        ('state', '=', 'done'), \
                                                        ('create_date', '>=', most_starting_date),\
                                                        ('create_date', '<', self.start_date)])

            for mv in stock_move:
                product_ids.add(mv.product_id)

            list = []

            for product in product_ids:
                if product.product_tmpl_id.active == True:
                    stock_move = self.env['stock.move'].search([('location_dest_id', '=', self.locat_id.id), \
                                                                ('create_date', '>=', most_starting_date),\
                                                                ('create_date', '<', self.start_date), \
                                                                ('state', '=', 'done'), \
                                                                ('product_id', '=', product.id)])

                    dicts = {}
                    qty = 0
                    for mv in stock_move:
                        qty += mv.product_qty

                    dicts['name'] = product.product_tmpl_id.name
                    dicts['product_id'] = product.id
                    dicts['previous_balance'] = qty
                    list.append(dicts)

            list_internal_transfer = []
            for product in product_ids:
                stock_moves = self.env['stock.move'].search([('location_id', '=', self.locat_id.id), \
                                                             ('state', '=', 'done'), \
                                                             ('create_date', '>=', most_starting_date),\
                                                             ('create_date', '<', self.start_date), \
                                                             ('product_id', '=', product.id)])
                dict_internal_transfer = {}
                quantity = 0
                for mv in stock_moves:
                    quantity += mv.product_qty
                dict_internal_transfer['product_id'] = product.id
                dict_internal_transfer['previous_balance'] = quantity
                list_internal_transfer.append(dict_internal_transfer)

            for data in list:
                for internal_data in list_internal_transfer:
                    if data['product_id'] == internal_data['product_id']:
                        data['previous_balance'] = data['previous_balance'] - internal_data['previous_balance']

        # non previous balance products calculation

        set_of_product = set()

        stock_moves_ids = self.env['stock.move'].search([('location_dest_id', '=', self.locat_id.id), \
                                                         ('state', '=', 'done'), \
                                                         ('create_date', '>=', self.start_date),\
                                                         ('create_date', '<=', self.end_date)])

        for product in stock_moves_ids:
            set_of_product.add(product.product_id)

        non_opening_balance_ids = set_of_product - product_ids
        for products_id in non_opening_balance_ids:
            if products_id.product_tmpl_id.active == True:
                product_dict = {}
                product_dict['name'] = products_id.product_tmpl_id.name
                product_dict['product_id'] = products_id.id
                product_dict['previous_balance'] = 0
                list.append(product_dict)

        # receipt/purchase balance calculation

        receipt_product_id_set = set()
        stock_moves_receipt = self.env['stock.move'].search([
                                                             ('location_dest_id', '=', self.locat_id.id), \
                                                             ('state', '=', 'done'), \
                                                             ('create_date', '>=', self.start_date),\
                                                             ('create_date', '<=', self.end_date)])

        for objects in stock_moves_receipt:
            receipt_product_id_set.add(objects.product_id)

        for product_id in receipt_product_id_set:
            stock_moves = self.env['stock.move'].search([
                                                         ('location_dest_id', '=', self.locat_id.id), \
                                                         ('create_date', '>=', self.start_date),\
                                                         ('create_date', '<=', self.end_date), \
                                                         ('state', '=', 'done'), \
                                                         ('product_id', '=', product_id.id)])
            qty = 0
            for mv in stock_moves:
                qty += mv.product_qty

            for dt in list:
                if dt['product_id'] == product_id.id:
                    dt['receipt_qty'] = qty

      # Issued/ transfer balance calculation

        issued_product_id_set = set()

        stock_moves_issued = self.env['stock.move'].search([('location_id', '=', self.locat_id.id), \
                                                            ('state', '=', (['done', 'assigned'])), \
                                                            ('create_date', '>=', self.start_date),\
                                                            ('create_date', '<=', self.end_date)])

        for object_id in stock_moves_issued:
            issued_product_id_set.add(object_id.product_id)

        for pro_id in issued_product_id_set:
            stock_moves = self.env['stock.move'].search([('location_id', '=', self.locat_id.id),\
                                                         ('state', '=', (['done', 'assigned'])), \
                                                         ('create_date', '>=', self.start_date),\
                                                         ('create_date', '<=', self.end_date),\
                                                         ('product_id', '=', pro_id.id)])

            qty = 0
            for mv in stock_moves:
                qty += mv.product_qty

            for issued_list in list:
                if issued_list['product_id'] == pro_id.id:
                    issued_list['issued_balance'] = qty

        # non receipt and issued balance calculation

        for dictionary in list:
            if not dictionary.get('issued_balance'):
                dictionary['issued_balance'] = 0

            if not dictionary.get('receipt_qty'):
                dictionary['receipt_qty'] = 0

        # Present and Closing balance calculation

        for dictionary in list:
            dictionary['present_balance'] = dictionary['previous_balance'] + dictionary['receipt_qty']
            dictionary['closing_balance'] = dictionary['present_balance'] - dictionary['issued_balance']

        # passing the data for render

        data = {
            'list': list,
        }

        return self.env['report'].get_action(self, 'inventory_product_report.main_stores_product', data=data)

