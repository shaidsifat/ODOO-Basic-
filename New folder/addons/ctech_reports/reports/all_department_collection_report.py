from odoo import models, fields, api
from datetime import datetime, timedelta


class AbstractModelReportDeliver(models.AbstractModel):
    _name = 'report.ctech_reports.all_department_bill_collection'

    def data_for_billing_report(self, start_date, end_date, data):

        # SERVICES = 5
        # LAB = 6
        # RADIOLOGY = 9
        # PATHOLOGY = 39
        SERVICES = self.env['product.category'].search([('name', '=', 'Services')])
        LAB = self.env['product.category'].search([('name', '=', 'Lab')])
        RADIOLOGY = self.env['product.category'].search([('name', '=', 'Radiology')])
        PATHOLOGY = self.env['product.category'].search([('name', '=', 'PATHOLOGY DEPARTMENT')])

        final_data = []

        department_list = self.env['product.category'].search(
            ['|', '|', '|', ('parent_id', '=', SERVICES.id), ('parent_id', '=', LAB.id), ('parent_id', '=', RADIOLOGY.id),
             ('parent_id', '=', PATHOLOGY.id)])

        for cat in department_list:
            account_invoice_line = self.env['account.invoice.line'].search(
                [('product_id.product_tmpl_id.categ_id.id', '=', cat.id), ('create_date', '>=', start_date),
                 ('create_date', '<=', end_date),('product_id.type', '=', 'service'),
                 ('invoice_id.state', '=', 'paid'), '|', ('invoice_id.type', '=', 'out_invoice'),
                 ('invoice_id.type', '=', 'out_refund')])

            countPaid = 0
            countRefund = 0
            countFree = 0
            totalPaidAmount = 0
            totalRefundAmount = 0
            dict = {}

            for line in account_invoice_line:
                if line.invoice_id.discount_type == 'none' and line.invoice_id.type == 'out_invoice':
                    countPaid += line.quantity
                    totalPaidAmount += line.price_subtotal
                elif line.invoice_id.discount_type == 'none' and line.invoice_id.type == 'out_refund':
                    countRefund += line.quantity
                    totalRefundAmount += line.price_subtotal
                elif line.invoice_id.discount_type == 'percentage':
                    countFree += line.quantity

            if bool(account_invoice_line):
                dict['depName'] = cat.name
                dict['countPaid'] = int(countPaid)
                dict['countFree'] = int(countFree)
                dict['totalPaidAmount'] = int(totalPaidAmount)
                dict['totalRefundAmount'] = int(totalRefundAmount)
                dict['countRefund'] = int(countRefund)
                final_data.append(dict)

        return final_data

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('ctech_reports.all_department_bill_collection')

        final_data = self.data_for_billing_report(docs.start_date, docs.end_date, data)
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
            'finalData': final_data,
            'user_name': self.env.user.partner_id.name,
        }
        return self.env['report'].render('ctech_reports.all_department_bill_collection', docargs)
