from odoo import models,fields

class Resuser(models.Model):
   _inherit = ('product.template')

   alternative_product_ids=fields.many2many('product.template'
                                            'alternative_product'
                                            'product_id'
                                            'alternative_product_id'
                                            string="alternative products"
                                              )