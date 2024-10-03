# from odoo import fields, models
#
#
# class InvoiceHistory(models.Model):
#     _name = "invoice.history"
#     _description = "Invoice Histories"
#
#     product_id = fields.Many2one("product.template", string="Product", ondelete="cascade")
#     product_product_id = fields.Many2one("product.product", string="Product", ondelete="cascade")
#     reference = fields.Char(string="Invoice Reference")
#     partner_id = fields.Many2one("res.partner", string="Partner")
#     invoice_date = fields.Date(string="Invoice Date")
#     product_description = fields.Char(string="Description")
#     quantity = fields.Float(string="Quantity")
#     unit_price = fields.Float(string="Unit Price")
#     discount = fields.Float(string="Discount (%)")
#     amount_without_taxes = fields.Float(string="Amount (without Taxes)")