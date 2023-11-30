# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
import logging
import requests, json, time

_logger = logging.getLogger(__name__)


class SaleOrderAccess(models.Model):
    _inherit = 'sale.order'

    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #
    #
    #
    #     is_admin = self.env.user.has_group('bahmni_sale_order_access.group_admin')
    #     if not is_admin:
    #         print ("args",args)
    #         print(type(self.env.user.id))
    #         args = [('create_uid','=',self.env.user.id)] + args
    #     return super(SaleOrderAccess, self).search(args, offset, limit, order, count)



























