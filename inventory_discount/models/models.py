from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    apply_discount = fields.Boolean("Apply Discount")
    discount_ids = fields.One2many('discount', 'category_id', string="Discounts")

class Discount(models.Model):
    _name = 'discount'
    _description = 'Discounts'

    name = fields.Char("Name")
    minimum_quantity = fields.Integer("Min qty")
    maximum_quantity = fields.Integer("Max Qty")
    discount_percent = fields.Float("Discount (%)")
    discount_value = fields.Float("Discount Value")
    category_id = fields.Many2one('product.category', string="Product Category")
