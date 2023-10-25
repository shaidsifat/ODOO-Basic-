from odoo import models, fields, api
from datetime import datetime, timedelta


class AbstractModelReportDeviver(models.AbstractModel):
    _name = 'report.expire_product_report.date_wise_expire_report'

    def data_for_expire_report(self, start_date, end_date, locat_id):

        expire_ids = self.env['stock.production.lot'].search(
            [('life_date', '>=', start_date), ('life_date', '<=', end_date)])

        stock_location_id = self.env['stock.location'].search([])
        print ("...........Stock Location..........", stock_location_id)

        exp_data_set = set()
        for i in expire_ids:
            for j in i.quant_ids:
                if locat_id == j.location_id.id:
                    exp_data_set.add(j.product_id)

        exp_data_collection = []
        for i in exp_data_set:
            data_collection_dict = {}
            stock_product_ids = self.env['stock.production.lot'].search([('life_date', '>=', start_date),\
                                                                         ('life_date', '<=', end_date),\
                                                                         ('product_id', '=', i.id)])

            qty = 0
            for rec in stock_product_ids:
                qty = qty + rec.product_qty

            data_collection_dict['name'] = i.product_tmpl_id.name
            data_collection_dict['quantity'] = qty
            exp_data_collection.append(data_collection_dict)

        return exp_data_collection

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('expire_product_report.date_wise_expire_report')

        data_collection = self.data_for_expire_report(docs.start_date, docs.end_date, docs.locat_id.id)
        # print ":::::::::::::collection data:::::::::::",data_collection
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        sd = datetime.strptime(docs.start_date, DATETIME_FORMAT)
        ed = datetime.strptime(docs.end_date, DATETIME_FORMAT)
        sd_convert = sd + timedelta(hours=6, minutes=00)
        ed_convert = ed + timedelta(hours=6, minutes=00)

        docargs = {
            'doc_model': data.get('model'),
            'docs': self,
            'from_date': docs.start_date,
            'to_date': docs.end_date,
            'start_date': sd_convert,
            'end_date': ed_convert,
            'exp_data_collection': data_collection,
        }

        return self.env['report'].render('expire_product_report.date_wise_expire_report', docargs)
