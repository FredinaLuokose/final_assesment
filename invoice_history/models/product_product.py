import io
import base64
import xlwt
from odoo import models, fields, api
from odoo.exceptions import UserError

class InvoiceHistory(models.Model):
    _name = "invoice.history"
    _description = "Invoice Histories"

    product_id = fields.Many2one("product.template", string="Product", ondelete="cascade")
    product_product_id = fields.Many2one("product.product", string="Product", ondelete="cascade")
    reference = fields.Char(string="Invoice Reference")
    partner_id = fields.Many2one("res.partner", string="Partner")
    invoice_date = fields.Date(string="Invoice Date")
    product_description = fields.Char(string="Description")
    quantity = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit Price")
    discount = fields.Float(string="Discount (%)")
    amount_without_taxes = fields.Float(string="Amount (without Taxes)")

class ProductTemplate(models.Model):
    _inherit = "product.template"

    invoice_history_ids = fields.One2many(
        'invoice.history',  # Adjusting the model to reference the InvoiceHistory model
        'product_id',
        string='Invoice History',
        readonly=True,
        compute="_compute_invoice_history_ids",  # Setting the compute method
    )

    @api.depends('product_variant_ids')  # Recompute when product variants change
    def _compute_invoice_history_ids(self):
        for rec in self:
            invoice_history = []
            product_lines = self.env["account.move.line"].search(
                [("product_id.product_tmpl_id", "=", rec.id), ("move_id.state", "=", "posted")]  # Filter by product template
            )

            if product_lines:
                for line in product_lines:
                    invoice_history.append((0, 0, {
                        "product_product_id": line.product_id.id,  # Capture the product variant
                        "reference": line.move_id.name,
                        "partner_id": line.move_id.partner_id.id,
                        "invoice_date": line.move_id.invoice_date,
                        "product_description": line.name,
                        "quantity": line.quantity,
                        "unit_price": line.price_unit,
                        "discount": line.discount,
                        "amount_without_taxes": line.price_subtotal,
                    }))
            rec.invoice_history_ids = invoice_history or [(0, 0, {})]

class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.model
    def action_product_invoice_history_xls(self):
        # Create an in-memory output file for the XLS
        output = io.BytesIO()

        # Create the workbook and worksheet
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet('Invoice History')

        # Define the headers based on your Invoice History fields
        headers = [
            'Invoice Reference', 'Partner', 'Invoice Date', 'Product Description',
            'Quantity', 'Unit Price', 'Discount (%)', 'Amount (without Taxes)'
        ]

        # Write the header row
        for col, header in enumerate(headers):
            sheet.write(0, col, header)

        # Fetch the active product ID from the context
        product_id = self.env.context.get('active_id')
        product = self.env['product.product'].browse(product_id)

        # Check if there are invoice history records
        if not product.invoice_history_ids:
            raise UserError("No invoice history data found for this product.")

        # Write each record's data to the corresponding row in the XLS file
        for row, history in enumerate(product.invoice_history_ids, start=1):
            sheet.write(row, 0, history.reference or '')
            sheet.write(row, 1, history.partner_id.name or '')
            sheet.write(row, 2, history.invoice_date.strftime('%Y-%m-%d') if history.invoice_date else '')
            sheet.write(row, 3, history.product_description or '')
            sheet.write(row, 4, history.quantity)
            sheet.write(row, 5, history.unit_price)
            sheet.write(row, 6, history.discount)
            sheet.write(row, 7, history.amount_without_taxes)

        # Save workbook to the output file
        workbook.save(output)
        output.seek(0)

        # Encode the result in base64 for attachment
        file_data = base64.b64encode(output.read()).decode('utf-8')

        # Create an attachment to allow download of the file
        attachment = self.env['ir.attachment'].create({
            'name': 'invoice_history.xls',
            'datas': file_data,
            'type': 'binary',
            'mimetype': 'application/vnd.ms-excel',
        })

        # Return the download action
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }
