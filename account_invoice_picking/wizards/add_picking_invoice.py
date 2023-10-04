from odoo import api, fields, models

class AddPickingToInvoiceWizard(models.TransientModel):
    _name = 'add.picking.to.invoice.wizard'
    _description = 'Wizard to Add Pickings to Invoice'

    invoice_id = fields.Many2one('account.move', string='Invoice')
    picking_ids = fields.Many2many('stock.picking', string='Pickings')

    def button_add_pickings(self):
        # Ambil invoice dari konteks
        invoice = self.env['account.move'].browse(self.invoice_id.id)

        # Tambahkan picking ke invoice
        invoice.write({'picking_ids': [(4, picking.id) for picking in self.picking_ids]})

        # Cari dan tambahkan Sales Order yang terkait
        sale_orders = self.env['sale.order']
        for picking in self.picking_ids:
            if picking.sale_id:
                sale_orders |= picking.sale_id
        if sale_orders:
            invoice.write({'invoice_line_ids.sale_line_ids.order_id': [(4, so.id) for so in sale_orders]})

        return {'type': 'ir.actions.act_window_close'}
