from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    def button_add_picking(self):
        context = {
            'default_invoice_id': self.id,
            'default_picking_ids': [(6, 0, self.picking_ids.ids)]
        }
        return {
            'name': 'Add Pickings to Invoice',
            'type': 'ir.actions.act_window',
            'res_model': 'add.picking.to.invoice.wizard',  # Ganti dengan nama model wizard Anda
            'view_mode': 'form',
            'view_id': self.env.ref('account_invoice_picking.view_wizard_add_picking_to_invoice_form').id,  # Ganti dengan ID view wizard Anda
            'target': 'new',
            'context': context,
        }