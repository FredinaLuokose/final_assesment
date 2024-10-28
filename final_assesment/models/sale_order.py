from odoo import models,fields,api

class Saleorderline(models.Model):
   _inherit = 'sale.order.line'

  @api.onchange('product_id')


def alternative_products_ids(self):

    if self.product_id and self.product_uom_quantity:
        alternative_products_ids = self.product_id.alternative_product_ids
        return
        {
        domain='product_id',alternative_products_ids
        }