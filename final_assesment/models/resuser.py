from odoo import models,fields

class Resuser(models.Model)
   _inherit = 'resusers'

   alternative_products=fields.Boolean(string="Alternative products")
