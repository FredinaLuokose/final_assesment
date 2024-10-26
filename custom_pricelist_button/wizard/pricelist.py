from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLineSelectPricelist(models.TransientModel):
    _name = 'sale.order.line.select.pricelist'
    _description = 'Wizard to Select Price List from Sale Order Line'

    order_line_id = fields.Many2one('sale.order.line', string='Sale Order Line', required=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    price_list_ids = fields.One2many('sale.order.line.select.pricelist.line', 'line_id', string='Pricelists')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            pricelist_items = self.env['product.pricelist.item'].search([
                ('product_tmpl_id', '=', self.product_id.product_tmpl_id.id)
            ])

            pricelist_lines = []
            for item in pricelist_items:
                pricelist_lines.append((0, 0, {
                    'pricelist_id': item.pricelist_id.id,
                    'select': False,
                }))
            self.price_list_ids = pricelist_lines

    @api.model
    def default_get(self, fields_list):
        res = super(SaleOrderLineSelectPricelist, self).default_get(fields_list)
        order_line_id = self._context.get('default_order_line_id')
        product_id = self._context.get('default_product_id')

        res.update({
            'order_line_id': order_line_id,
            'product_id': product_id,
        })
        return res

    def action_select_pricelist(self):
        selected_lines = self.price_list_ids.filtered('select')

        if len(selected_lines) == 1:
            raise ValidationError("You must select only one price list.")

        if len(selected_lines) == 0:
            raise ValidationError("No price list selected. Please select a price list.")

        current_date = datetime.now().date()
        price_list = selected_lines.pricelist_id

        active_items = price_list.item_ids.filtered(
            lambda item: (not item.date_start or current_date >= item.date_start.date()) and
                         (not item.date_end or current_date <= item.date_end.date())
        )

        if not active_items:
            raise (ValidationError
                (
                f"The selected price list '{price_list.name}' is not active or has expired. Please select a valid price list."
            ))

        sale_order = self.order_line_id.order_id
        sale_order.write({'pricelist_id': price_list.id})
        sale_order.action_update_prices()
        return {'type': 'ir.actions.act_window_close'}


class SaleOrderLineSelectPricelistLine(models.TransientModel):
    _name = 'sale.order.line.select.pricelist.line'
    _description = 'Wizard Line for Selecting Pricelist'

    line_id = fields.Many2one('sale.order.line.select.pricelist', string='Wizard')
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist')
    select = fields.Boolean(string='Select')
