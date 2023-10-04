from odoo import models, api, fields, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    from_invoice = fields.Boolean('From Invoice', default = False)

    def button_add_picking(self):
        if not self.partner_id:
            raise UserError(_("Harap pilih customer terlebih dahulu."))
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
    
    @api.depends("from_invoice", "invoice_line_ids", "invoice_line_ids.move_line_ids")
    def _compute_picking_ids(self):
        for invoice in self:
            invoice.delivery_count = len(invoice.picking_ids)
            if not invoice.from_invoice:
                invoice.picking_ids = invoice.mapped(
                    "invoice_line_ids.move_line_ids.picking_id"
                )