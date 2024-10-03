from odoo import models, fields, api

class AccountMoveCorrectionWizard(models.TransientModel):
    _name = 'account.move.correction.wizard'
    _description = 'Invoice Correction Wizard'

    description = fields.Text(string="Description", required=True)

    def action_post_correction(self):
        # Logic to handle the correction submission
        move_id = self.env.context.get('active_id')
        if move_id:
            move = self.env['account.move'].browse(move_id)
            move.message_post(body=f"Correction: {self.description}")
        return {'type': 'ir.actions.act_window_close'}

class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_open_correction_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move.correction.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('invoice_rivision.view_correction_wizard_form').id,
            'target': 'new',
            'context': {'default_description': ''},
        }
# class AccountMove(models.Model):
#     _inherit = 'account.move'
#
#     correction_ids = fields.One2many(
#         'account.move.correction',
#         'move_id',
#         string="Correction History"
#     )


class AccountMove(models.Model):
    _inherit = 'account.move'

    correction_ids = fields.One2many('account.move.correction', 'move_id', string='Correction History')


class AccountMoveCorrection(models.Model):
    _name = 'account.move.correction'

    move_id = fields.Many2one('account.move', string='Invoice')
    date = fields.Datetime(string='Correction Date', default=fields.Datetime.now)
    user_id = fields.Many2one('res.users', string='Corrected By')
    description = fields.Text(string='Description')
    quantity = fields.Float(string='Quantity')