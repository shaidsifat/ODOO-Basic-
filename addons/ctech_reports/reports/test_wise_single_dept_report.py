from odoo import models, fields, api
from datetime import datetime, timedelta


class AbstractModelReportDeliver(models.AbstractModel):
    _name = 'report.ctech_reports.test_single_dept_report'

    def data_for_billing_report(self, start_date, end_date, user_ids, categ_id):
        billing_users = []
        for user_id in user_ids:
            if len(user_id) > 0:
                user = self.env['res.users'].search([('id', '=', user_id.id)])
                billing_users.append(user)

        report_data = []
        for user_id in user_ids:
            invoice_ids = self.env["account.invoice"].search([('create_date', '>=', start_date),
                                                              ('create_date', '<=', end_date),
                                                              ('user_id', '=', user_id.id),
                                                              ('type', '=', 'out_invoice'),
                                                              ('state', '=', 'paid')
                                                              ])
            for invoice_id in invoice_ids:
                data_dictionary = {}
                data_dictionary["partner_name"] = invoice_id.partner_id.name
                data_dictionary["partner_age"] = invoice_id.partner_id.age if invoice_id.partner_id.age else ""
                data_dictionary["invoice_number"] = invoice_id.number
                data_dictionary["origin"] = invoice_id.origin
                data_dictionary["invoice_date"] = invoice_id.date_invoice
                data_dictionary["product_name"] = []
                amount_total = 0
                for inv_line_id in invoice_id.invoice_line_ids:
                    if inv_line_id.product_id.product_tmpl_id.categ_id.id == categ_id.id and inv_line_id.product_id.type == 'service':
                        data_dictionary["product_name"].append(inv_line_id.product_id.name)
                        amount_total += inv_line_id.price_subtotal

                if data_dictionary["product_name"]:
                    data_dictionary["amount_total"] = amount_total
                    report_data.append(data_dictionary)

        return report_data, billing_users

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('ctech_reports.test_single_dept_report')

        report_datas, billing_users = self.data_for_billing_report(docs.start_date, docs.end_date, docs.user_ids,
                                                                      docs.categ_id)
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
            'report_data': report_datas,
            'billing_user': billing_users,
            'user_name': self.env.user.partner_id.name,
            'categ_name': docs.categ_id.name,
        }

        return self.env['report'].render('ctech_reports.test_single_dept_report', docargs)
