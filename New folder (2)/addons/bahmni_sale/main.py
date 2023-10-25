import json
from odoo import http
from odoo.http import Controller, request
from werkzeug.wrappers import Response
from datetime import datetime

class GetLabData(Controller):

    @http.route('/get/lab/data/<string:start_date>/<string:end_date>',auth="none", type='http')
    def get_lab_data(self,**kwargs):
        """
            This method is called through the route path for retrieve lab's data from lab.order model
            :return json dumps with Response class
        """
        try:
            headers = {'Content-Type': 'application/json'}
            lab_order_id = request.env['lab.order'].sudo().search([('create_date', '>=', kwargs['start_date']), \
                                                                     ('create_date', '<=', kwargs['end_date'])])
            lab_data = []
            for order in lab_order_id:
                lab_order = {}
                lab_order["patient_identifier"] = order.partner_id.ref
                lab_order["invoice_number"] = order.invoice_id.number
                lab_order["patient_name"] = order.partner_id.name
                lab_order["age"] = order.partner_id.age
                lab_order["sex"] = order.partner_id.gender
                lab_order["is_free_patient"] = order.is_free
                lab_order["is_refund"] = order.is_refund
                lab_order["create_date"] = str(datetime.strptime(str(order.create_date),'%Y-%m-%d %H:%M:%S').date())
                lab_order_lines = []
                for line in order.lab_order_line_ids:
                    lab_order_lines.append({"product_name": line.name,
                                            "uuid" : line.uuid
                                            })
                lab_order["lines"] = lab_order_lines
                lab_data.append(lab_order)
            return Response(json.dumps(lab_data), headers=headers)
        except:
            return "Some Exception Occurred"
