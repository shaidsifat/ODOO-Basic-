
from odoo import http
from odoo.http import Controller, request
from datetime import datetime, timedelta

class InvoiceController(Controller):

    @http.route('/print/invoice/<model("sale.order"):order_id>', type='http', auth="public", website='True')
    def render_sale_invoice_template(self,order_id,**kwargs):
        print "order id:",order_id
        order_id.write({
            'is_invoice_printed' : True
        })
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        DATETIME_FORMAT_FOR_DELIVERY = "%Y-%m-%d"

        current_date = datetime.now()
        current_date_convert = current_date + timedelta(hours=6, minutes=00)
        cd_convert = current_date_convert.strftime(DATETIME_FORMAT)

        next_date = datetime.now() + timedelta(days=1)
        delivery_date_convert = next_date + timedelta(hours=6, minutes=00)
        dl_convert = delivery_date_convert.strftime(DATETIME_FORMAT_FOR_DELIVERY)
        # print order_id.product_id
        return request.render("bahmni_sale.bahmni_sale_report_invoice",\
               # {'docs': order_id.invoice_ids.filtered(lambda inv : inv.type == 'out_invoice')[0],
              {
                'docs': order_id.invoice_ids.filtered(lambda inv: inv.type == 'out_invoice')[0],
                'order_id': order_id,
                'current_time': cd_convert,
                'delivery_date': dl_convert,
                })

