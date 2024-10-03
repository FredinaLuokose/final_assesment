# from odoo import fields, models, api
#
#
# class ProductTemplate(models.Model):
#     _inherit = "product.template"
#
#     invoice_history_ids = fields.One2many(
#         "invoice.history",
#         "product_id",
#         compute="_compute_invoice_history_ids"
#     )
#
#     @api.depends_context('company_id')
#     def _compute_invoice_history_ids(self):
#         for rec in self:
#             invoice_history = []
#             product_lines = self.env["account.move.line"].search(
#                 [("product_id", "=", rec.product_variant_id.id), ("move_id.state", "=", "posted")])
#
#             if product_lines:
#                 for line in product_lines:
#                     invoice_history.append((0, 0, {
#                         "reference": line.move_id.name,
#                         "partner_id": line.move_id.partner_id.id,
#                         "invoice_date": line.move_id.invoice_date,
#                         "product_description": line.name,
#                         "quantity": line.quantity,
#                         "unit_price": line.price_unit,
#                         "discount": line.discount,
#                         "amount_without_taxes": line.price_subtotal,
#                     }))
#             rec.invoice_history_ids = invoice_history or [(0, 0, {})]
