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
        print "account_invoice_ids", order_id.invoice_ids.filtered(lambda inv: inv.type == 'out_invoice'),len(order_id.invoice_ids.filtered(lambda inv: inv.type == 'out_invoice'))
        account_invoice =  order_id.invoice_ids.filtered(lambda inv: inv.type == 'out_invoice')
        account_invoice_data = request.env['account.invoice'].search([('origin','=',account_invoice.number)])
        refund_account_invoice_lines_id = account_invoice_data.invoice_line_ids


        if account_invoice.has_refund:


            # print "refund_invoice_id",account_invoice_data
            # # print docs_data._fields
            # print docs_data.number
            # print docs_data.refund_invoice_id
            # print docs_data.has_refund
            # print docs_data.name
            # print docs_data.invoice_line_ids
            # print docs_data.origin
            #
            # print "type",type(account_invoice.invoice_line_ids),account_invoice.invoice_line_ids
            # print "type",type(refund_account_invoice_lines_id),refund_account_invoice_lines_id
            #
            # result = [x for x in account_invoice.invoice_line_ids if x not in refund_account_invoice_lines_id]
            #
            # print "result",result

            # post_data=request.env['account.invoice'].search([('origin', '=', order_id.name)]).write(
            #      {'after_refund_invoice_lines_ids':  account_invoice.invoice_line_ids })
            sorting_list = []
            length = len(account_invoice.invoice_line_ids)
            print "-------length--------",length
            for i in range(length):
                if account_invoice.invoice_line_ids[i].product_id:
                    print  account_invoice.invoice_line_ids[i].product_id.name
                    # print account_invoice.invoice_line_ids[i].product_id.name in   refund_account_invoice_lines_id
                    refund_length = len(refund_account_invoice_lines_id)
                    for j in range(refund_length):
                        if  account_invoice.invoice_line_ids[i].product_id.name == refund_account_invoice_lines_id[j].product_id.name:
                             pass
                        else:
                            sorting_list.append(account_invoice.invoice_line_ids[i].product_id.name)


            print "----------------sorting data-----",sorting_list


            send_data = []
            if sorting_list:

                # newlength = len(sorting_list)
                # for i in  range(newlength):
                #     for j in range(length):
                #         if  (account_invoice.invoice_line_ids[j].product_id.name == sorting_list[i]):
                #             target_data = account_invoice.invoice_line_ids[j]
                #             print ("---------target_data----",target_data,type(target_data))
                #             print ("-------account_invoice.invoice_line_ids----------",account_invoice.invoice_line_ids,type(account_invoice.invoice_line_ids))
                #             send_data.append(account_invoice.invoice_line_ids -  target_data)




            print "------------------send data-----------",send_data


            # for j in range(length):

            data =  account_invoice.invoice_line_ids -  refund_account_invoice_lines_id
            print data

            # print "___________", account_invoice.invoice_line_ids
            # print "========", refund_account_invoice_lines_id
            #
            #
            # sale_order_product = []
            # for invoice in  account_invoice.invoice_line_ids:
            #     print"account_invoice",invoice.product_id.name
            #     sale_order_product.append(invoice)
            # refund_product = []
            # for refund_invoice in refund_account_invoice_lines_id:
            #     print "refund_account_invoice_lines_id",refund_invoice.product_id.name
            #     refund_product.append(refund_invoice)

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
                                      {'docs': docs_data,
                                       'order_id': order_id,
                                       # 'after_refund_order_line_data': docs_data.invoice_lines_tuple,
                                       'after_refund_order_line_data':  send_data,
                                       'product_id': order_id.product_id,
                                       'current_time': cd_convert,
                                       'delivery_date': dl_convert,
                                       })

        else:

            return "message"