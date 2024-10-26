from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    pricelist_id = fields.Many2one(
        'product.pricelist',
        string='Pricelist',
        related='order_id.pricelist_id',
        readonly=True,
    )

    def action_select_pricelist(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Select Price List',
            'res_model': 'sale.order.line.select.pricelist',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_order_line_id': self.id,
                'default_product_id': self.product_id.id,

            },
        }