from odoo import models,fields
class stockwizard(models.TransientModel):
  _name = 'stock_wizard'
  product_id =Many2one('product.product',string='product')
  alternative_product_ids(self):