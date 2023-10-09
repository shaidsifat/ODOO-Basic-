from odoo import models, fields, api
from datetime import datetime, timedelta


class AbstractModelReportDeliver(models.AbstractModel):
    _name = 'report.ctech_reports.test_bill_report'

    def data_for_billing_report(self, start_date, end_date, user_id):

        billing_user = user_id.name

        account_invoice_ids = self.env['account.invoice'].search([('create_date', '>=', start_date),\
                                                                  ('create_date', '<=', end_date), \
                                                                  ('state', '=', 'paid'), \
                                                                  ('user_id', '=', user_id.id),\
                                                                  ('type', '=', 'out_invoice'),\
                                                                  ])

        account_inv_list = []
        for account_invoice_id in account_invoice_ids:
            dict_account_inv = {}
            dict_account_inv['partner_id'] = account_invoice_id.partner_id.name
            dict_account_inv['date'] = account_invoice_id.date_invoice
            dict_account_inv['number'] = account_invoice_id.number
            dict_account_inv['origin'] = account_invoice_id.origin
            dict_account_inv['total_amount'] = account_invoice_id.amount_total
            total_amount = 0.0
            if account_invoice_id.discount_type == 'none':
                total_amount = account_invoice_id.amount_total

            dict_account_inv['total_amount'] = total_amount
            product_id_list = []
            for line in account_invoice_id.invoice_line_ids:
                dict_product_ids = {}
                dict_product_ids['name'] = line.product_id.name
                product_id_list.append(dict_product_ids)

            dict_account_inv["product_id"] = product_id_list
            account_inv_list.append(dict_account_inv)

        for account_invoice in account_inv_list:

            account_invoice_refund_ids = self.env['account.invoice'].search([('create_date', '>=', start_date), \
                                                                  ('create_date', '<=', end_date), \
                                                                  ('state', '=', 'paid'), \
                                                                  ('user_id', '=', user_id.id), \
                                                                  ('type', '=', 'out_refund'), \
                                                                  ('origin','=', account_invoice["number"])
                                                                  ])

            refund_amount = 0
            for refund_invoice_id in account_invoice_refund_ids:
                refund_amount += refund_invoice_id.amount_total

            account_invoice["total_amount"] -= refund_amount

        return account_inv_list, billing_user

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('ctech_reports.test_bill_report')

        data_collection,billing_user = self.data_for_billing_report(docs.start_date, docs.end_date, docs.user_id)
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
            'test_bill_collection': data_collection,
            'billing_user': billing_user,
            'user_name': self.env.user.partner_id.name,
        }

        return self.env['report'].render('ctech_reports.test_bill_report', docargs)
