from odoo import models, fields, api
from datetime import datetime, timedelta


class AbstractModelReportDeliver(models.AbstractModel):
    _name = 'report.inventory_product_report.main_stores_product'

    def data_for_inventory_report(self, start_date, end_date, locate_id, data):
        location_id = self.env['stock.location'].search([('id', '=', locate_id)])
        location_name= location_id.name

        return data, location_name





    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('inventory_product_report.main_stores_product')

        data_collection, locate_name = self.data_for_inventory_report(docs.start_date, docs.end_date, docs.locat_id.id, data['list'])
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
            'user_name': self.env.user.partner_id.name,
            'location': locate_name,
            'inv_data_collection': data_collection,
        }

        return self.env['report'].render('inventory_product_report.main_stores_product', docargs)
