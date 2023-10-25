
from datetime import datetime, timedelta
from odoo import fields, models, api, _
import logging
import requests


_logger = logging.getLogger(__name__)

class DataCollector(models.Model):
    _name="data.collector"

    department_name=fields.Char(String='Department Name',default='NITOR')

    product_name=fields.Char('Product Name')

    amount=fields.Float(string="Amount" )

    payment_date = fields.Datetime(string="Payment Date", default=fields.Datetime.now(), required=True)

    invoice_id = fields.Integer(string='Invoice Id')

    origin = fields.Char(string="Origin")

    product_id=fields.Integer()

    categ_id = fields.Integer()

    @api.multi
    def collect_data(self,facilityName):
        now = datetime.strftime(fields.Datetime.context_timestamp(self, datetime.now()), "%Y-%m-%d %H:%M:%S")
        print type(now)
        print now
        print facilityName
        before_one_day = datetime.strptime(now,"%Y-%m-%d %H:%M:%S") + timedelta(days=-1)
        previous_date=before_one_day.strftime("%Y-%m-%d %H:%M:%S")

        print "converted before date",type(previous_date)
        print previous_date

        header = {"content-type": "application/json", "accept": "application/json",
                  "catch-control": "no-cache"}

        data_collector=self.env['data.collector'].search([])

        if not data_collector or data_collector :
            account_invoice_line=self.env['account.invoice.line'].search([('write_date','>',previous_date),('write_date','<=',now)],order='id asc')
            print "Datasssssssss",account_invoice_line
            self.env['data.collector'].search([]).unlink()
            self.env['department.wise.collection'].search([]).unlink()
            for data in account_invoice_line:
                vals={
                'payment_date':data.create_date,
                'department_name':data.product_id.product_tmpl_id.categ_id.name,
                'amount':data.price_subtotal_signed,
                'product_id':data.product_id.id,
                'invoice_id':data.invoice_id.id,
                'origin':data.origin,
                'categ_id':data.product_id.product_tmpl_id.categ_id.id,
                'product_name':data.product_id.product_tmpl_id.name
                }
                print vals
                self.create(vals)

            data_category=self.env['product.category'].search([])

            for id in data_category:
                datas=self.env['data.collector'].search([('categ_id','=',id.id)],)
                amount = 0
                department=""
                category_id=0
                create_date=""

                list=set()
                for i in datas:
                    amount+=i.amount
                    department=i.department_name
                    category_id=i.categ_id
                    create_date=i.payment_date
                    print"product_id",i.product_id
                    print"product_name",i.product_name
                    print"product_amount",i.amount
                    list.add(i.product_id)
                if(amount!=0):
                    print amount
                    print department
                    print category_id
                    self.env['department.wise.collection'].create({
                        'name':department,
                        'total_amount':amount,
                        'categ_id':category_id
                    })
                    data_collector_json = self.env['department.wise.collection'].search([])
                    date=create_date
                    date_formating = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
                    date_string = date_formating.strftime("%Y-%m-%d")
                    data = {
                        "facilityInfo": "",
                        "department": "",
                        "date": "",
                        "totalAmount": ""
                    }
                    for dt in data_collector_json:
                        data["facilityInfo"] = facilityName
                        data["department"] = dt.name
                        data["date"] = date_string
                        data["totalAmount"] = dt.total_amount
                    list_of_object=[]
                    for i in list:
                        sum = 0
                        count=0
                        name=""
                        dict={}
                        var=self.env['data.collector'].search([('product_id','=',i)])
                        for j in var:
                            sum=sum+j.amount
                            count +=1
                            name=j.product_name
                        print "sumssssssssss",sum
                        print "countssssssss",count
                        print "namesssssssss",name
                        dict['investigationName']=name
                        dict['quantity']=count
                        dict['amount']=sum
                        dict['localDate']=date_string
                        list_of_object.append(dict)
                    data['billingInfoDetails']=list_of_object
                    print data
                    x = requests.post("http://43.231.78.115:5984/billingInfo", headers=header, json=data)
                    print "status code", x.status_code
            id=self.env['data.collector'].search([],order='id desc',limit=1)
            print "------------",id.id
            self.env['data.collector'].search([('id','!=',id.id)]).unlink()

















