from odoo import models, fields, api

class CreateInvoiceWizard(models.TransientModel):
    _name = 'create.invoice.wizard'
    _description = 'Create Invoice Wizard'

    journal_id = fields.Many2one('account.journal', string='Journal', required=True)
    invoice_date = fields.Date(string='Invoice Date', required=True)

    def action_create_invoice(self):
        invoice_obj = self.env['account.move']
        picking = self.env['stock.picking'].browse(self._context.get('default_picking_id'))

        # Initialize sale_order variable
        sale_order = False
        if picking.sale_id:
            sale_order = picking.sale_id
            customer = sale_order.partner_id
        else:
            customer = picking.partner_id

        # Prepare the invoice lines from the sale order lines if sale_order exists
        invoice_lines = []
        if sale_order:
            for line in sale_order.order_line:
                invoice_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'quantity': line.product_uom_qty,
                    'price_unit': line.price_unit,
                    'tax_ids': [(6, 0, line.tax_id.ids)],
                    'name': line.name,
                    'account_id': line.product_id.categ_id.property_account_income_categ_id.id,
                    # Ensure correct account
                }))

        # Create and post the invoice
        for record in self:
            invoice = invoice_obj.create({
                'journal_id': record.journal_id.id,
                'invoice_date': record.invoice_date,
                'move_type': 'out_invoice',
                'partner_id': customer.id,
                'invoice_line_ids': invoice_lines,  # Add the lines to the invoice
            })

            # Post the invoice to validate it
            invoice.action_post()

        return {'type': 'ir.actions.act_window_close'}  # Close the wizard after posting the invoice


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True)

    def open_invoice_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Invoice',
            'res_model': 'create.invoice.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_picking_id': self.id},  # Pass the current picking id to the wizard
        }
