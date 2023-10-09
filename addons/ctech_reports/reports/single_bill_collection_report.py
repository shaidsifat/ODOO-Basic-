from odoo import models, fields, api
from datetime import datetime, timedelta


class AbstractModelReportDeliver(models.AbstractModel):
    _name = 'report.ctech_reports.single_user_bill_collection_report'

    def data_for_billing_report(self, start_date, end_date, user_id, data):

        # RETRIVE PAID INVOICE DATA USER WISE
        account_invoice_datas = self.env['account.invoice'].search(
            [('create_uid', '=', user_id.id), ('create_date', '>=', start_date), ('create_date', '<=', end_date),
             ('state', '=', 'paid'), ('type', '=', 'out_invoice')])

        # COUNT PAID PATIENT USER WISE
        paidPatient = self.env['account.invoice'].search_count(
            [('create_uid', '=', user_id.id), ('create_date', '>=', start_date), ('create_date', '<=', end_date),
             ('state', '=', 'paid'), ('type', '=', 'out_invoice'), ('discount_type', '=', 'none')])
        paidPatient_datas = self.env['account.invoice'].search(
            [('create_uid', '=', user_id.id), ('create_date', '>=', start_date), ('create_date', '<=', end_date),
             ('state', '=', 'paid'), ('type', '=', 'out_invoice'), ('discount_type', '=', 'none')])

        # Counting free patient
        freePatient = self.env['account.invoice'].search_count(
            [('create_uid', '=', user_id.id), ('create_date', '>=', start_date), ('create_date', '<=', end_date),
             ('state', '=', 'paid'), ('type', '=', 'out_invoice'), ('discount_type', '=', 'percentage')])

        # Open Bill WISE
        account_invoice_open = self.env['account.invoice'].search(
            [('create_uid', '=', user_id.id), ('create_date', '>=', start_date), ('create_date', '<=', end_date),
             ('state', '=', 'open'), ('type', '=', 'out_invoice')])

        totalOpenInvoiceAmount = 0
        for op in account_invoice_open:
            totalOpenInvoiceAmount += op.amount_untaxed
        # CALCULLATE THE TOTAL PAID AMOUNT
        totalAmount = 0
        for inv in paidPatient_datas:
            totalAmount += inv.amount_untaxed

        account_invoice_refund = self.env['account.invoice'].search(
            [('create_date', '>=', start_date), ('create_date', '<=', end_date),
             ('state', '=', 'paid'), ('type', '=', 'out_refund'),('user_id', '=', user_id.id)])
        # CALCULATE THE TOTAL REFUND AMOUNT
        totalRefund = 0
        for refInv in account_invoice_refund:
            totalRefund += refInv.amount_untaxed

        # CALCULATE THE NET AMOUNT
        netCollection = totalAmount - totalRefund

        final_list = []
        dict = {
            'userName': user_id.partner_id.name,
            'freePatient': freePatient,
            'paidPatient': paidPatient,
            'totalCallection': netCollection,
            'totalAmount': totalAmount,
            'totalRefund': totalRefund,
            'total_patient': len(account_invoice_datas),
            'totalOpenInvoiceAmount': totalOpenInvoiceAmount
        }
        final_list.append(dict)
        return final_list

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('ctech_reports.single_user_bill_collection_report')

        data_collection = self.data_for_billing_report(docs.start_date, docs.end_date, docs.user_id, data)
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
            'single_bill_collection': data_collection,
            'billing_user': docs.user_id.name,
            'user_name': self.env.user.partner_id.name,
        }

        return self.env['report'].render('ctech_reports.single_user_bill_collection_report', docargs)
