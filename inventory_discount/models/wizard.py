from odoo import models, fields, api


class CategoryDiscountWizard(models.TransientModel):
    _name = 'category.discount.wizard'
    _description = 'Category Discount Wizard'

    category_id = fields.Many2one('product.category', string='Category', required=True)
    quantity = fields.Float(string='Quantity', required=True)
    name = fields.Many2one('product.product', string='Product', required=True)
    discount = fields.Float(string='Discount (%)', readonly=True)

    @api.onchange('category_id', 'quantity')
    def _onchange_discount(self):
        if self.category_id:
            # Find a discount that matches the given quantity range
            discount = self.env['discount'].search([
                ('category_id', '=', self.category_id.id),
                ('minimum_quantity', '<=', self.quantity),
                ('maximum_quantity', '>=', self.quantity)
            ], limit=1)

            # Set the discount percentage if a discount is found
            if discount:
                self.discount = discount.discount_percent
            else:
                self.discount = 0.0

    def action_apply_discount(self):
        # Find the active sale order
        sale_order = self.env['sale.order'].browse(self.env.context.get('active_id'))

        if sale_order:
            # Apply discount to the sale order lines matching the product selected
            for line in sale_order.order_line:
                if line.product_id.id == self.name.id:
                    line.discount = self.discount
from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    net_total = fields.Float(string="Net Total", compute="_compute_net_total")

    @api.depends('order_line.price_total')
    def _compute_net_total(self):
        for order in self:
            total = sum(line.price_subtotal for line in order.order_line)
            # You can apply any additional logic here, like discounts or taxes
            order.net_total = total

    def action_check_discount(self):
        return {
            'name': 'Category Discount Wizard',
            'type': 'ir.actions.act_window',
            'res_model': 'category.discount.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('inventory_discount.view_category_discount_wizard').id,
            'target': 'new',
            'context': {
                'default_category_id': self.order_line[0].product_id.categ_id.id if self.order_line else False,
            }
        }

import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'product_uom_qty')
    def _onchange_product_id(self):
        if self.product_id:
            # Fetch the product's category
            category = self.product_id.categ_id

            # Search for the applicable discount record based on category and quantity
            Discount = self.env['discount']
            discount_records = Discount.search([
                ('category_id', '=', category.id),
                ('minimum_quantity', '<=', self.product_uom_qty),
                ('maximum_quantity', '>=', self.product_uom_qty)
            ], order='discount_percent desc')

            # Log details for debugging
            _logger.info(f"Product ID: {self.product_id.id}, Category: {category.id}, Quantity: {self.product_uom_qty}")
            _logger.info(f"Discount Records Found: {[record.id for record in discount_records]}")

            if discount_records:
                # Apply the highest discount if available
                best_discount = discount_records[0]
                self.discount = best_discount.discount_percent
                _logger.info(f"Discount Applied: {self.discount} for Discount Record ID: {best_discount.id}")
            else:
                # No discount if none found
                self.discount = 0.0
                _logger.info("No Discount Applied")
