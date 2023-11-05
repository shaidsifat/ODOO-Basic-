import json
from lxml import etree
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare
from odoo.tools.misc import formatLang

from odoo.exceptions import UserError, RedirectWarning, ValidationError

import odoo.addons.decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)


class AccountRefundCalculationInvoice(models.Model):


    _inherit = ['account.invoice']

    after_refund_invoice_lines_ids   =  fields.One2many('account.invoice.line', 'invoice_id', string='Invoice Lines', copy=True)



    def on_refund_delete(self,item_to_delete):

        for item in self.data:
            if item == item_to_delete:
                self.data.remove(item)

