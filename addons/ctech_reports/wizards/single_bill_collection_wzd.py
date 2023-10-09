from odoo import models, api, fields
from datetime import datetime, timedelta

'''
    ctech_reports" is folder name and "single_user_bill_collection_report" is report template id
'''


class WizardProductSale(models.TransientModel):
    _name = 'custom.single.bill.collection'

    start_date = fields.Datetime(string='From Date', default=fields.Datetime.now(), required=True)
    end_date = fields.Datetime(string='End Date', default=fields.Datetime.now(), required=True)
    user_id = fields.Many2one('res.users', string='Billing User')

    @api.multi
    def print_report(self, data):
        # # Retrieving all patients
        # account_invoice_datas = self.env['account.invoice'].search(
        #     [('create_uid', '=', self.user_id.id), ('create_date', '>=', self.start_date),
        #      ('create_date', '<=', self.end_date),
        #      ('state', '=', 'paid'), ('type', '=', 'out_invoice')])
        #
        # # Counting paid patient
        # paidPatient = self.env['account.invoice'].search_count(
        #     [('create_uid', '=', self.user_id.id), ('create_date', '>=', self.start_date),
        #      ('create_date', '<=', self.end_date),
        #      ('state', '=', 'paid'), ('type', '=', 'out_invoice'), ('discount_type', '=', 'none')])
        # paidPatient_datas = self.env['account.invoice'].search(
        #     [('create_uid', '=', self.user_id.id), ('create_date', '>=', self.start_date),
        #      ('create_date', '<=', self.end_date),
        #      ('state', '=', 'paid'), ('type', '=', 'out_invoice'), ('discount_type', '=', 'none')])
        #
        # # Counting free patient
        # freePatient = self.env['account.invoice'].search_count(
        #     [('create_uid', '=', self.user_id.id), ('create_date', '>=', self.start_date),
        #      ('create_date', '<=', self.end_date),
        #      ('state', '=', 'paid'), ('type', '=', 'out_invoice'), ('discount_type', '=', 'percentage')])
        #
        # # Open Bill WISE
        # account_invoice_open = self.env['account.invoice'].search(
        #     [('create_uid', '=', self.user_id.id), ('create_date', '>=', self.start_date),
        #      ('create_date', '<=', self.end_date),
        #      ('state', '=', 'open'), ('type', '=', 'out_invoice')])
        #
        # totalOpenInvoiceAmount = 0
        # for op in account_invoice_open:
        #     totalOpenInvoiceAmount += op.amount_untaxed
        # # CALCULLATE THE TOTAL PAID AMOUNT
        # totalAmount = 0
        # for inv in paidPatient_datas:
        #     totalAmount += inv.amount_untaxed
        #
        # # REFUND
        #
        # account_invoice_refund = self.env['account.invoice'].search(
        #     [('create_date', '>=', self.start_date), ('create_date', '<=', self.end_date),
        #      ('state', '=', 'paid'), ('type', '=', 'out_refund'), ('user_id', '=', self.user_id.id)])
        # # CALCULATE THE TOTAL REFUND AMOUNT
        # totalRefund = 0
        # for refInv in account_invoice_refund:
        #     totalRefund += refInv.amount_untaxed
        #
        # # CALCULATE THE NET AMOUNT
        # netCollection = totalAmount - totalRefund
        #
        # final_list = []
        # dict = {
        #     'userName': self.user_id.partner_id.name,
        #     'freePatient': freePatient,
        #     'paidPatient': paidPatient,
        #     'totalCallection': netCollection,
        #     'totalAmount': totalAmount,
        #     'totalRefund': totalRefund,
        #     'total_patient': len(account_invoice_datas),
        #     'totalOpenInvoiceAmount': totalOpenInvoiceAmount
        # }
        # final_list.append(dict)
        # data = {
        #     'list': final_list,
        # }

        return self.env['report'].get_action(self, 'ctech_reports.single_user_bill_collection_report', data=data)
