from odoo import models, fields, api
from datetime import datetime, timedelta


class AbstractModelReportDeliver(models.AbstractModel):
    _name = 'report.ctech_reports.multiple_user_bill_collection_report'

    def data_for_billing_report(self, start_date, end_date, data):

        users = self.env['res.users'].search([('active', '=', 'true')])
        final_data = []

        for user in users:

            # RETRIVE PAID INVOICE DATA USER WISE
            account_invoice_datas = self.env['account.invoice'].search(
                [('create_uid', '=', user.id), ('create_date', '>=', start_date), ('create_date', '<=', end_date),
                 ('state', '=', 'paid'), ('type', '=', 'out_invoice')])

            account_invoice_open = self.env['account.invoice'].search(
                [('create_uid', '=', user.id), ('create_date', '>=', start_date), ('create_date', '<=', end_date),
                 ('state', '=', 'open'), ('type', '=', 'out_invoice')])

            totalOpenInvoiceAmount = 0
            for op in account_invoice_open:
                totalOpenInvoiceAmount += op.amount_untaxed

            # CALCULATE TOTAL PAID AMOUNT USER WISE
            totalAmount = 0
            for inv in account_invoice_datas:
                # totalAmount += inv.amount_total_signed
                if inv.discount_type == 'none':

                    totalAmount += inv.amount_untaxed

            # COUNT THE FREE PATIENT
            freePatient = self.env['account.invoice'].search_count(
                [('create_uid', '=', user.id), ('create_date', '>=', start_date), ('create_date', '<=', end_date),
                 ('state', '=', 'paid'), ('type', '=', 'out_invoice'), ('discount_type', '=', 'percentage')])
            # RETRIVE THE REFUND DATA USER WISE
            account_invoice_refund = self.env['account.invoice'].search(
                [('user_id', '=', user.id), ('create_date', '>=', start_date), ('create_date', '<=', end_date),
                 ('state', '=', 'paid'), ('type', '=', 'out_refund')])
            # CALCULATE TOTAL REFUND USER WISE
            totalRefund = 0
            for refInv in account_invoice_refund:
                totalRefund += refInv.amount_untaxed
            # CALCULATE THE NET AMONT USER WISE
            netCollection = totalAmount - totalRefund

            dict = {
                'user_name': user.partner_id.name,
                'free_patient': freePatient,
                'total_patient': len(account_invoice_datas),
                'total_collection': netCollection,
                'total_Refund': totalRefund,
                'totalOpenInvoiceAmount': totalOpenInvoiceAmount
            }

            # CONDITION FOR CHECKS WHEATHER USER HAS ANY COLLECTION OR NOT
            if len(account_invoice_datas) != 0:
                final_data.append(dict)

        return final_data

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('ctech_reports.multiple_user_bill_collection_report')

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
            'multiple_bill_collection': final_data,
            # 'billing_user': billing_user,
            'user_name': self.env.user.partner_id.name,
        }

        return self.env['report'].render('ctech_reports.multiple_user_bill_collection_report', docargs)
