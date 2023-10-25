from odoo import models, fields, api
from datetime import datetime, timedelta


class AbstractModelReportDeliver(models.AbstractModel):
    _name = 'report.ctech_reports.test_bill_report'

    def data_for_billing_report(self, start_date, end_date, user_id, data):
        user = self.env['res.users'].search([('id', '=', user_id.id)])
        billing_user = user_id.name

        collection = "out_invoice"
        refund = "out_refund"
        free = 'percentage'
        paid = 'none'

        sale_collection = self.env['account.invoice'].search(
            [('state', '=', 'paid'), ('create_date', '>=', start_date), ('create_date', '<=', end_date)])

        result_dict = []

        filter_by_user = list(filter(lambda x: x.create_uid == user, sale_collection))
        filter_by_type = list(filter(lambda x: x.type == collection, filter_by_user))
        filtered_by_date = list(
            filter(lambda x: x.create_date >= start_date and x.create_date <= end_date, filter_by_type))

        filter_by_without_refund = []
        filter_by_with_refund = []
        for fd in filtered_by_date:
            refund_invoice = self.env['account.invoice'].search([('origin', '=', fd.move_name)])

            if len(refund_invoice) == 0:
                filter_by_without_refund.append(fd)
            else:
                for ref in refund_invoice:
                    if fd.amount_total != ref.amount_total:
                        filter_by_with_refund.append(ref)

        # for fd in filtered_by_date:
        for fd in filter_by_without_refund:
            main_invoice = self.env['account.invoice'].search([('move_name', '=', fd.move_name)])
            main_line = self.env['account.invoice.line'].search([('invoice_id', '=', main_invoice.id)])
            refund_invoice = self.env['account.invoice'].search([('origin', '=', main_invoice.move_name)])
            ref_line = self.env['account.invoice.line'].search([('invoice_id', '=', refund_invoice.id)])
            serviceList = []

            len(refund_invoice)

            if len(refund_invoice) > 0:
                for m in main_line:
                    serviceListAdd = []
                    serviceListAdd.append(main_invoice.partner_id.name)
                    serviceListAdd.append(main_invoice.date_invoice)
                    serviceListAdd.append(main_invoice.number)
                    serviceListAdd.append(main_invoice.origin)
                    serviceListAdd.append(main_invoice.amount_total)
                    sn = []
                    for r in ref_line:
                        if m.product_id != r.product_id:
                            sn.append(m.name)
                            serviceListAdd.append(sn)
                        serviceList.append(serviceListAdd)
                result_dict.append(serviceList)

            else:
                serviceListAdd = []
                serviceListAdd.append(main_invoice.partner_id.name)
                serviceListAdd.append(main_invoice.date_invoice)
                serviceListAdd.append(main_invoice.number)
                serviceListAdd.append(main_invoice.origin)
                if main_invoice.discount_type == free:
                    serviceListAdd.append(0.0)
                else:
                    serviceListAdd.append(main_invoice.amount_total)
                sn = []
                for m in main_line:
                    sn.append(m.name)
                    serviceListAdd.append(sn)
                serviceListAdd.append(main_invoice.discount_type)
                serviceList.append(serviceListAdd)
            result_dict.append(serviceList)

        for fd in filter_by_with_refund:
            main_invoice = self.env['account.invoice'].search([('move_name', '=', fd.origin)])
            main_line = self.env['account.invoice.line'].search([('invoice_id', '=', main_invoice.id)])
            ref_line = self.env['account.invoice.line'].search([('invoice_id', '=', fd.id)])
            after_refund_total = 0.0
            after_refund_sn = []
            serviceList = []

            for r in ref_line:
                sn = []
                net_total = 0.0
                for m in main_line:
                    if m.product_id != r.product_id:
                        sn.append(m.name)
                        net_total += m.price_subtotal
                if len(sn) > 0:
                    after_refund_total = net_total
                    after_refund_sn = sn

            serviceListAdd = []
            serviceListAdd.append(main_invoice.partner_id.name)
            serviceListAdd.append(main_invoice.date_invoice)
            serviceListAdd.append(main_invoice.number)
            serviceListAdd.append(main_invoice.origin)
            serviceListAdd.append(after_refund_total)
            serviceListAdd.append(after_refund_sn)
            serviceListAdd.append(main_invoice.discount_type)
            serviceList.append(serviceListAdd)
            result_dict.append(serviceList)
        return result_dict, billing_user

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('ctech_reports.test_bill_report')

        data_collection,billing_user = self.data_for_billing_report(docs.start_date, docs.end_date, docs.user_id, data)
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
