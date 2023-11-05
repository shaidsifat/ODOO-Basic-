from odoo import http
from odoo.http import Controller, request
from datetime import datetime, timedelta



class InvoiceController(Controller):

    @http.route('/print/refund_invoice/<model("sale.order"):order_id>', type='http', auth="public", website='True')
    def render_refund_sale_invoice_template(self, order_id, osv=None, **kwargs):

        order_id.write({
            'is_invoice_printed': True
        })
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        DATETIME_FORMAT_FOR_DELIVERY = "%Y-%m-%d"

        current_date = datetime.now()
        current_date_convert = current_date + timedelta(hours=6, minutes=00)
        cd_convert = current_date_convert.strftime(DATETIME_FORMAT)

        next_date = datetime.now() + timedelta(days=1)
        delivery_date_convert = next_date + timedelta(hours=6, minutes=00)
        dl_convert = delivery_date_convert.strftime(DATETIME_FORMAT_FOR_DELIVERY)



        sale_product_data = order_id.invoice_ids.filtered(lambda inv: inv.type == 'out_invoice')

        # filter = order_id.invoice_ids.filtered
        refund_product = order_id.product_id.name
        # print "refund_product:",refund_product
        # print "order product:",sale_product_data


        # for product_data in  sale_product_data.invoice_line_ids:
        #     print product_data.name
        #     print order_id.product_id.name
        #     if product_data.name == order_id.product_id.name:
        #
        #        pass
        #
        #        # product_data.unlink()
        #     else:
        #         print type(product_data)
        #         data = product_data
        #         env = http.request.env
        #         post_list =request.env['account.invoice'].search([('origin', '=', order_id.name)]).write({'after_refund_invoice_lines_ids':data})
        #         # print request.env['account.invoice'].search([('origin', '=', order_id.name)]).after_refund_invoice_lines_ids
        #         print post_list
                # order_id.invoice_ids.filtered(lambda inv: inv.type == 'out_invoice')[0].write(
                #     {'after_refund_invoice_lines_ids': data})
        # print list
        # invoice_lines_tuple = tuple(line.id for line in list)

        docs_data = order_id.invoice_ids.filtered(lambda inv: inv.type == 'out_invoice')[0]

        # print "invoice_line_ids",docs_data.invoice_line_ids
        # print "account_invoice", docs_data.after_refund_invoice_lines_ids
        data=docs_data.invoice_line_ids - docs_data.invoice_line_ids[0]
        # print "len_data",len(data)
        if len(data) == 0:

            message = "No data for Refund Invoice."
            # # request.render("sale_report_refund_invoice_document", {'message': request.session.get('message')})
            return message

        else:
            # post_list = request.env['account.invoice'].search([('origin', '=', order_id.name)]).write({'after_refund_invoice_lines_ids': data})
            # print "account_invoice", data
            # print  invoice_lines_tuple
            # print self.env['account.invoice'].search( [ ('origin','=',order_id.name ) ] )
            return request.render("bahmni_sale.bahmni_sale_refund_report_invoice", \
                                  # {'docs': order_id.invoice_ids.filtered(lambda inv: inv.type == 'out_invoice')[0],
                                   {  'docs':  docs_data,
                                      'order_id': order_id,
                                      # 'after_refund_order_line_data': docs_data.invoice_lines_tuple,
                                      'after_refund_order_line_data': data,
                                      'product_id' : order_id.product_id,
                                      'current_time': cd_convert,
                                      'delivery_date': dl_convert,
                                   })


