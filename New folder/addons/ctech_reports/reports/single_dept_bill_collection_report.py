from odoo import models, fields, api
from datetime import datetime, timedelta


class AbstractModelReportDeliver(models.AbstractModel):
    _name = 'report.ctech_reports.single_department_bill'

    # def category_wise_report(self,start_date, end_date, user_ids, category_id):
    #     users = user_ids.ids
    #     for user in users:
    #         paid_inv_line = self.env["account.invoice.line"].search([('create_date', '>=', start_date),
    #                                                                  ('create_date', '<=', end_date),
    #                                                                  ('create_uid', '=', user.id),
    #                                                                  ('product_id.categ_id', '=', category_id.id)])

    def data_for_billing_report(self, start_date, end_date, user_ids, categ_id, data):

        userName= []

        for u in user_ids:
            if len(u) > 0:
                user = self.env['res.users'].search([('id', '=', u.id)])
                userName.append(user)

        account_invoice_datas = []
        for u in user_ids:
            if len(u) > 0:
                account_invoice = self.env['account.invoice'].search(
                    [('create_uid', '=', u.id), ('create_date', '>=', start_date), ('create_date', '<=', end_date),
                     ('state', '=', 'paid'), ('type', '=', 'out_invoice')])
                account_invoice_datas.extend(account_invoice)

        # declaring set for containing product_id
        setProductId = set()
        # declearing set for containing invoice_id
        invoiceId = set()

        # for geting the product_id  according to category_id and geting the invoice_id of products

        for inv in account_invoice_datas:
            for line in inv.invoice_line_ids:
                if line.product_id.product_tmpl_id.categ_id.id == categ_id.id:
                    setProductId.add(line.product_id.id)
                    invoiceId.add(inv.id)

        list = []
        # for geting the quantity,total,name of product according category
        inv_list = []
        for i in setProductId:
            account_invoice_line = self.env['account.invoice.line'].search(
                [('product_id', '=', i), ('create_date', '>=', start_date), ('create_date', '<=', end_date)])

            count = 0
            countFree = 0
            name = ""
            total = 0
            dict = {}

            for line in account_invoice_line:

                for invId in invoiceId:
                    # condition for check the invoice id of the particular product from account_invoice_line
                    if line.invoice_id.id == invId and line.invoice_id.discount_type == 'none':
                        count += line.quantity
                        name = line.product_id.product_tmpl_id.name
                        total += line.price_subtotal_signed
                    elif line.invoice_id.id == invId and line.invoice_id.discount_type == 'percentage':
                        if line.invoice_id not in inv_list:
                            countFree += line.quantity
                            name = line.product_id.product_tmpl_id.name
                            inv_list += [line.invoice_id]

            dict['name'] = name
            dict['quantity'] = int(count)
            dict['total'] = int(total)
            dict['countFree'] = int(countFree)
            list.append(dict)

        # for calculating Total Refund collection

        # getting invoice data with refund collection

        account_invoice_refund_datas = []

        for user in user_ids:
            account_invoice_refund = self.env['account.invoice'].search(
                [('user_id', '=', user.id), ('create_date', '>=', start_date), ('create_date', '<=', end_date),
                 ('state', '=', 'paid'), ('type', '=', 'out_refund'), ('discount_type', '=', 'none')])

            account_invoice_refund_datas.extend(account_invoice_refund)

        # declaring set for containing refund product_id
        setRefundProductId = set()

        # declearing set for containing refund invoice_id
        RefundinvoiceId = set()

        # for geting the product_id  according to category_id and geting the invoice_id of products
        for inv in account_invoice_refund_datas:
            for line in inv.invoice_line_ids:
                if line.product_id.product_tmpl_id.categ_id.id == categ_id.id:
                    setRefundProductId.add(line.product_id.id)
                    RefundinvoiceId.add(inv.id)

        Refundlist = []
        # for geting the refund quantity,total,name of product according category
        for i in setRefundProductId:
            account_invoice_line = self.env['account.invoice.line'].search(
                [('product_id', '=', i), ('create_date', '>=', start_date),
                 ('create_date', '<=', end_date)])
            count = 0
            name = ""
            total = 0
            dict = {}
            for line in account_invoice_line:
                for invId in RefundinvoiceId:
                    # condition for check the refund invoice id of the particular product from account_invoice_line
                    if line.invoice_id.id == invId:
                        count += 1
                        name = line.product_id.product_tmpl_id.name
                        total += line.price_subtotal_signed
            dict['name'] = name
            dict['quantity'] = count
            dict['total'] = int(abs(total))
            Refundlist.append(dict)
        return list, Refundlist,userName

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('ctech_reports.single_department_bill')

        final_data, refund_list, username = self.data_for_billing_report(docs.start_date, docs.end_date, docs.user_ids,
                                                               docs.categ_id, data)
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
            'paidData': final_data,
            'refundData': refund_list,
            'billing_user': username,
            'categ_name': docs.categ_id.name,
        }

        return self.env['report'].render('ctech_reports.single_department_bill', docargs)
