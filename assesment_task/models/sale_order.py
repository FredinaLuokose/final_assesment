# # models/sale_order.py
# from odoo import models
#
# class SaleOrder(models.Model):
#     _inherit = 'sale.order'
#
#     def _update_invoiced_quantity(self):
#         for order in self:
#             for line in order.order_line:
#                 line.qty_invoiced = sum(line.invoice_lines.mapped('quantity'))
