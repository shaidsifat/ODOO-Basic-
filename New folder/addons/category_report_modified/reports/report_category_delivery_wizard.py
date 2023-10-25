from odoo import models, fields, api
from datetime import datetime, timedelta


class AbstractModelReportDeviver(models.AbstractModel):
    _name = 'report.category_report_modified.category_wise_delivery_modified'

    def data_for_delivery_report(self, start_date, end_date, ctg_id):

        act_invoice_id = self.env['account.invoice'].search(
            [('create_date', '>=', start_date), ('create_date', '<=', end_date),
             ('type', '=', 'out_invoice'), ('state', '=', 'paid')])

        data_collection_set = set()
        for rec in act_invoice_id:
            for i in rec.invoice_line_ids:
                data_collection_set.add(i.product_id)

        # for data collection

        cate_data_collection = []
        for i in data_collection_set:
            if i.product_tmpl_id.categ_id.id == ctg_id:
                cate_data_collection_dict = {}
                account_inv_line_ids = self.env['account.invoice.line'].search(
                    [('create_date', '>=', start_date), ('create_date', '<=', end_date),
                     ('product_id', '=', i.id)])

                qty = 0
                for rec in account_inv_line_ids:
                    if rec.invoice_id.type == 'out_invoice':
                        qty = qty + rec.quantity
                        unit_price = rec.price_unit
                        total_price = qty * rec.price_unit

                cate_data_collection_dict['name'] = i.product_tmpl_id.name
                cate_data_collection_dict['quantity'] = qty
                cate_data_collection_dict['id'] = i.id
                cate_data_collection_dict['unit_price'] = unit_price
                cate_data_collection_dict['total_unit_price'] = total_price
                cate_data_collection.append(cate_data_collection_dict)

        # calculating cost price cost benefit
        for i in cate_data_collection:
            product_object = self.env['product.product'].browse([i['id']])
            i['cost_price'] = product_object.product_tmpl_id.standard_price
            i['total_cost_price'] = i['quantity'] * i['cost_price']
            total_benifit = i['total_unit_price'] - i['total_cost_price']
            i['total_benefit'] = total_benifit

        # for refund data

        refund_data_set = set()
        refund_cate_collection = []

        account_invoice = self.env['account.invoice'].search(
            [('create_date', '>=', start_date), ('create_date', '<=', end_date), ('type', '=', 'out_refund'),
             ('state', '=', 'paid')])

        for rec in account_invoice:
            for j in rec.invoice_line_ids:
                if j.product_id.product_tmpl_id.categ_id.id == ctg_id:
                    refund_data_set.add(j.product_id)

        for rec in refund_data_set:
            refund_cate_collection_dict = {}
            refund_inv_line_ids = self.env['account.invoice.line'].search(
                [('create_date', '>=', start_date), ('create_date', '<=', end_date), ('product_id', '=', rec.id)])

            qty = 0
            for pro in refund_inv_line_ids:
                if pro.invoice_id.type == 'out_refund':
                    qty += pro.quantity
                    unit_price = pro.price_unit
                    total_price = qty * pro.price_unit

            refund_cate_collection_dict['name'] = rec.product_tmpl_id.name
            refund_cate_collection_dict['quantity'] = qty
            refund_cate_collection_dict['unit_price'] = unit_price
            refund_cate_collection_dict['id'] = rec.id
            refund_cate_collection_dict['refund_total_unit_price'] = total_price
            refund_cate_collection.append(refund_cate_collection_dict)

        # refund calculating cost price cost benefit
        for i in refund_cate_collection:
            refund_product = self.env['product.product'].browse([i['id']])
            i['refund_cost_price'] = refund_product.product_tmpl_id.standard_price
            i['total_cost_price'] = i['quantity'] * i['refund_cost_price']
            total_benifit = i['refund_total_unit_price'] - i['total_cost_price']
            i['total_profit'] = total_benifit

        # Net Collection

        net_cate_collection = []
        collection_product_set = set()
        for i in cate_data_collection:
            product_collection = self.env['product.product'].browse([i['id']])
            collection_product_set.add(product_collection)

        refund_product_set = set()
        for i in refund_cate_collection:
            product_refund = self.env['product.product'].browse([i['id']])
            refund_product_set.add(product_refund)

        not_refund_products = collection_product_set - refund_product_set

        for i in cate_data_collection:
            for j in refund_cate_collection:
                if j['id'] == i['id']:
                    net_quantity = i['quantity'] - j['quantity']
                    dict_net_quantity = {}
                    dict_net_quantity['name'] = j['name']
                    dict_net_quantity['net_quantity'] = net_quantity
                    dict_net_quantity['id'] = j['id']
                    dict_net_quantity['net_unit_price'] = j['unit_price']
                    dict_net_quantity['net_cost_price'] = j['refund_cost_price']
                    net_cate_collection.append(dict_net_quantity)

        for i in cate_data_collection:
            for j in not_refund_products:
                if j.id == i['id']:
                    dict_net_quantity = {}
                    dict_net_quantity['name'] = i['name']
                    dict_net_quantity['net_quantity'] = i['quantity']
                    dict_net_quantity['net_unit_price'] = i['unit_price']
                    dict_net_quantity['net_cost_price'] = i['cost_price']
                    net_cate_collection.append(dict_net_quantity)

        # net total unit and cost benefit
        for i in net_cate_collection:
            i['net_total_unit_price'] = i['net_quantity'] * i['net_unit_price']
            i['net_total_cost'] = i['net_quantity'] * i['net_cost_price']
            net_total_benifit = i['net_total_unit_price'] - i['net_total_cost']
            i['net_total_benefit'] = net_total_benifit


        return cate_data_collection, refund_cate_collection, net_cate_collection

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('category_report_modified.category_wise_delivery_modified')

        data_collection, refund_cate, net_data = self.data_for_delivery_report(docs.start_date, docs.end_date,
                                                                               docs.ctg_id.id)
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        sd = datetime.strptime(docs.start_date, DATETIME_FORMAT)
        ed = datetime.strptime(docs.end_date, DATETIME_FORMAT)
        current_date = datetime.now()
        sd_convert = sd + timedelta(hours=6, minutes=00)
        ed_convert = ed + timedelta(hours=6, minutes=00)
        current_date_convert = current_date + timedelta(hours=6, minutes=00)
        cd_convert = current_date_convert.strftime(DATETIME_FORMAT)
        docargs = {
            'doc_model': data.get('model'),
            'docs': self,
            'from_date': docs.start_date,
            'to_date': docs.end_date,
            'start_date': sd_convert,
            'end_date': ed_convert,
            'current_time': cd_convert,
            'department_name': docs.ctg_id.name,
            'user_name': self.env.user.partner_id.name,
            'data_collection': data_collection,
            'refund_cate_data': refund_cate,
            'net_data_collection': net_data,
        }

        return self.env['report'].render('category_report_modified.category_wise_delivery_modified', docargs)
