from odoo import models, fields, api
from datetime import datetime, timedelta


class AbstractModelReportDeliver(models.AbstractModel):
    _name = 'report.scrap_product_report.pdf_view_scrap_product_report'

    def data_for_scrap_report(self, start_date, end_date, locate_id, data):
        locate_id = self.env['stock.location'].search([('id', '=', locate_id)])
        location_name= locate_id.name

        return data, location_name





    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('scrap_product_report.pdf_view_scrap_product_report')

        data_collection, locate_name = self.data_for_scrap_report(docs.start_date, docs.end_date, docs.location_id.id,\
                                                                  data['list'])
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
            'location': locate_name,
            'scrap_data': data_collection,
        }

        return self.env['report'].render('scrap_product_report.pdf_view_scrap_product_report', docargs)
