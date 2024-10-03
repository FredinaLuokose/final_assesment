from odoo import fields, models, api
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = "account.move"

    delivery_count = fields.Integer(string='Delivery Orders', compute='_compute_picking')

    def action_create_picking(self):
        # Get the picking type for delivery orders
        picking_type = self.env.ref('stock.picking_type_out', raise_if_not_found=False)
        if not picking_type:
            raise UserError('Picking type not found')

        # Create the picking record (ensure 'partner_id' and other fields exist)
        picking = self.env["stock.picking"].create({
            "partner_id": self.partner_id.id,
            "scheduled_date": self.invoice_date or fields.Date.today(),  # Use today as fallback
            "date_deadline": self.invoice_date_due or fields.Date.today(),
            "origin": self.name,
            "move_type": "direct",  # Can be changed if needed
            "picking_type_id": picking_type.id,
            "location_id": self.env.ref('stock.stock_location_stock').id,  # Source location
            "location_dest_id": self.partner_id.property_stock_customer.id,  # Destination location
        })

        StockMove = self.env["stock.move"]
        for line in self.invoice_line_ids:
            if not line.product_id:
                raise UserError(f"Product not found in line {line.name}")

            StockMove.create({
                "name": line.name,
                "date": self.invoice_date or fields.Date.today(),
                "product_uom_qty": line.quantity,  # Ensure the right field name for quantity
                "product_uom": line.product_id.uom_id.id,
                "picking_id": picking.id,
                "product_id": line.product_id.id,
                "location_id": self.env.ref('stock.stock_location_stock').id,  # Source location
                "location_dest_id": self.partner_id.property_stock_customer.id,  # Destination location
            })

        # Create vendor bills after creating the stock picking
        self.create_vendor_bills()

        return picking

    @api.depends('invoice_line_ids')  # Updated dependency
    def _compute_picking(self):
        for order in self:
            # Count the related pickings by origin (which matches the move name)
            pickings = self.env['stock.picking'].search([('origin', '=', order.name)])
            order.delivery_count = len(pickings)

    def create_vendor_bills(self):
        # Ensure invoice lines are present
        if not self.invoice_line_ids:
            return

        # Prepare the lines for the vendor bill
        bill_lines = []
        for line in self.invoice_line_ids:
            if not line.product_id:
                raise UserError(f"Product not found for line {line.name}")

            bill_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'quantity': line.quantity,
                'price_unit': line.price_unit,
                'name': line.name,
            }))

        # Create the vendor bill (in_invoice for vendor bills)
        self.env['account.move'].create({
            'move_type': 'in_invoice',  # Vendor bill type
            'partner_id': self.partner_id.id,
            'invoice_line_ids': bill_lines,
            'invoice_date': self.invoice_date or fields.Date.today(),
            'invoice_date_due': self.invoice_date_due or fields.Date.today(),
            'currency_id': self.currency_id.id,
        })

    def action_view_delivery(self):
        # Return an action to view related delivery orders (stock pickings)
        return {
            "name": "Delivery",
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "view_mode": "tree,form",
            "domain": [('origin', '=', self.name)],
        }
