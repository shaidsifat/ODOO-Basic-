from odoo import models, fields, api
from datetime import datetime, timedelta


class ReportAppointment(models.AbstractModel):
    _name = 'report.purchase_incomplete_report.purchase_template_id'
    def data_for_report(self, start_date, end_date):

        data = self.env['stock.picking'].search(
            [('create_date', '>=', start_date),('create_date','<=',end_date),('state','!=','done'),('location_id.usage','=','supplier')])
        data_list = []
        for purchase_order_id in data:

            purchase_data = {}
            purchase_data['name'] = str(purchase_order_id.partner_id.name)
            purchase_data['origin'] = purchase_order_id.origin
            purchase_data['products'] =  purchase_order_id.pack_operation_product_ids
            purchase_data['order_qty'] = purchase_order_id.pack_operation_product_ids
            purchase_data['partner_id'] = str(purchase_order_id.partner_id.name)
            purchase_data['backorder_id'] = purchase_order_id.backorder_id.id
            purchase_data['backorder_name'] = purchase_order_id.backorder_id.name

            data_list.append(purchase_data)
        return data_list


    @api.model
    def render_html(self,docsid, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('purchase_incomplete_report.purchase_template_id')
        final_data = self.data_for_report(docs.start_date, docs.end_date)
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        sd = datetime.strptime(docs.start_date, DATETIME_FORMAT)
        ed = datetime.strptime(docs.end_date, DATETIME_FORMAT)
        current_date = datetime.now()
        sd_convert = sd + timedelta(hours=6, minutes=00)
        ed_convert = ed + timedelta(hours=6, minutes=00)
        current_date_convert = current_date + timedelta(hours=6, minutes=00)
        cd_convert = current_date_convert.strftime(DATETIME_FORMAT)
        docargs = {
            'final_data': final_data,
            'form_date': docs.start_date,
            'to_date': docs.end_date,
            'start_date': sd_convert,
            'end_date': ed_convert,
            'current_time': cd_convert,
            'username': self.env.user.partner_id.name,
        }
        return self.env['report'].render('purchase_incomplete_report.purchase_template_id', docargs)


