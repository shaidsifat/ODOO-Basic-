from odoo import models, api, fields
from datetime import datetime, timedelta


class WizardProductDeliver(models.TransientModel):
    _name = 'product.transfer.report'

    start_date = fields.Datetime(string='From Date')
    end_date = fields.Datetime(string='End Date')
    locate_id = fields.Many2one('stock.location', string='Location')

    @api.multi
    def print_report(self, data):

        # Issued/ transfer balance calculation

        list = []

        issued_product_id_set = set()

        stock_moves_issued = self.env['stock.move'].search([('location_id', '=', self.locate_id.id), \
                                                            ('state', '=', (['done', 'assigned'])), \
                                                            ('create_date', '>=', self.start_date),\
                                                            ('create_date', '<=', self.end_date)])
        for object_id in stock_moves_issued:
            issued_product_id_set.add(object_id.product_id)

        for pro_id in issued_product_id_set:
            dict_stock_move = {}
            stock_moves = self.env['stock.move'].search([('location_id', '=', self.locate_id.id), \
                                                         ('state', '=', (['done', 'assigned'])), \
                                                         ('create_date', '>=', self.start_date),\
                                                         ('create_date', '<=', self.end_date),\
                                                         ('product_id', '=', pro_id.id)])
            qty = 0
            for mv in stock_moves:
                qty += mv.product_qty

            dict_stock_move['name'] = pro_id.product_tmpl_id.name
            dict_stock_move['product_id'] = pro_id.id
            dict_stock_move['issued_balance'] = qty
            list.append(dict_stock_move)

        # sale orders refund calculation in receipt
        stock_moves = self.env['stock.move'].search([('location_id', '=', self.locate_id.id), \
                                                     ('state', '=', (['done', 'assigned'])),\
                                                     ('create_date', '>=', self.start_date), \
                                                     ('create_date', '<=', self.end_date)])

        for pro_id in stock_moves:
            account_invoice_line = self.env['account.invoice.line'].search([('create_date', '>=', self.start_date), \
                                                                            ('create_date', '<=', self.end_date), \
                                                                            ('product_id', '=', pro_id.product_id.id),
                                                                            ('origin', '=', pro_id.origin),\
                                                                            ('price_subtotal_signed', '<=', 0)])
            line_qty = 0
            for line in account_invoice_line:

                if line.invoice_id.type== 'out_refund' and line.invoice_id.state== 'paid':
                    line_qty = line_qty+ line.quantity
                for lst in list:
                    if lst['product_id'] == pro_id.product_id.id:
                        lst['refund_qty'] = line_qty

        # non receipt and issued balance calculation

        for dictionary in list:
            if not dictionary.get('issued_balance'):
                dictionary['issued_balance'] = 0
                if not dictionary.get('refund_qty'):
                    dictionary['refund_qty'] = 0

        for dictionary in list:
            dictionary['total_qty'] = dictionary['issued_balance'] - dictionary['refund_qty']

        # passing the data for render

        data = {
            'list': list,
        }

        return self.env['report'].get_action(self, 'locations_product_transfer.product_transfer', data=data)

