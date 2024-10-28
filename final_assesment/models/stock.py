from odoo import models,fields,api

class Stockmove(models.Model):
   _inherit = 'stock.move'

  @api.model
  def check_product(self,product_id):
    product=self.env(product.product_id)
    return {
        'type': 'ir.actions.act_window',
        'name': 'check_product,
        'view_mode': 'form',
        'target': 'new',
        'context': [product.product_id
    }
