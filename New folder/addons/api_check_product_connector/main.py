from odoo import http
from odoo.http import Controller, request

class ProdcutCheckAvailability(Controller):

    @http.route('/product/availability/check/',auth="public",csrf=False,type='json',methods=['POST'])
    def product_availability_check(self,**kwargs):
        if not kwargs.get('uuid'):
            return {
                'message':'Product UUID Not set into the params',
                'params':"{'uuid':<string value>}"
            }
        product_uuid = str(kwargs.get('uuid'))
        product_id = request.env['product.product'].sudo().search([('uuid','=',product_uuid),
                                                                   ('type','in',['product'])
                                                                   ])
        if product_id.product_tmpl_id.qty_available > 0:
            data = {
                'available':True,
                'message':'Success',
            }
        else:
            data = {
                'available':False,
                'message':'Success',
            }

        return data



