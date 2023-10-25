from odoo import models, api, fields
from datetime import datetime, timedelta

'''
    scrap_product_report" is folder name and "scrap_product_report_pdf" is model name
'''


class WizardProductDeliver(models.TransientModel):
    _name = 'inventory.scrap.product.report'

    start_date = fields.Datetime(string='From Date')
    end_date = fields.Datetime(string='End Date')
    location_id = fields.Many2one('stock.location', string='Location')

    @api.multi
    def print_report(self, data):
        stock_move = self.env['stock.move'].search([('location_dest_id', '=', self.location_id.id),\
                                                    ('create_date', '>=', self.start_date),\
                                                    ('create_date', '<=', self.end_date)])
        product_ids_set = set()
        for products in stock_move:
            product_ids_set.add(products.product_id)
        lisi_of_products = []
        for products in product_ids_set:
            dict_of_products= {}
            stock_moves_ids = self.env['stock.move'].search([('product_id', '=', products.id),\
                                                            ('location_dest_id', '=', self.location_id.id),\
                                                            ('create_date', '>=', self.start_date),\
                                                            ('create_date', '<=', self.end_date)])
            qty = 0
            for stm in stock_moves_ids:
                qty = qty + stm.product_qty
            dict_of_products['name'] = products.product_tmpl_id.name
            dict_of_products['product_id'] = products.id
            dict_of_products['product_qty'] = qty
            lisi_of_products.append(dict_of_products)

        # If return the product form the given location
        return_product_list = []
        products_ids = set()
        stock_move_id = self.env['stock.move'].search([('location_id', '=', self.location_id.id),\
                                                       ('create_date', '>=', self.start_date),\
                                                       ('create_date', '<=', self.end_date)])
        for objects in stock_move_id:
            products_ids.add(objects.product_id)
        for pro_ids in products_ids:
            dict_of_return_products = {}
            stock_moves = self.env['stock.move'].search([('location_id', '=', self.location_id.id), \
                                                         ('product_id', '=', pro_ids.id),\
                                                         ('create_date', '>=', self.start_date), \
                                                         ('create_date', '<=', self.end_date)])
            return_qty = 0
            for stm_id in stock_moves:
                return_qty = return_qty + stm_id.product_qty
            dict_of_return_products['name'] = pro_ids.product_tmpl_id.name
            dict_of_return_products['product_id'] = pro_ids.id
            dict_of_return_products['product_qty'] = return_qty
            return_product_list.append(dict_of_return_products)
        for lst in lisi_of_products:
            for return_lst in return_product_list:
                if lst['product_id'] == return_lst['product_id']:
                    total_qty = lst['product_qty'] - return_lst['product_qty']
                    lst['product_qty']= total_qty

        # passing the data for render
        data = {
            'list': lisi_of_products,
        }

        return self.env['report'].get_action(self, 'scrap_product_report.pdf_view_scrap_product_report', data=data)

