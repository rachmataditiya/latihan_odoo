from odoo import api, fields, models

class AddPickingToInvoiceWizard(models.TransientModel):
    _name = 'add.picking.to.invoice.wizard'
    _description = 'Wizard to Add Pickings to Invoice'

    invoice_id = fields.Many2one('account.move', string='Invoice')
    picking_ids = fields.Many2many('stock.picking', string='Pickings')

    def button_add_pickings(self):
        # Ambil invoice dari konteks
        invoice = self.env['account.move'].browse(self.invoice_id.id)
        picking_vals = [(4, picking.id) for picking in self.picking_ids]
        invoice_line_vals = [(5, 0, 0)]
        invoice_lines_to_sale_order_line = {}

        for picking in self.picking_ids:
            sale_order = picking.sale_id  
            for move in picking.move_ids_without_package:
                product = move.product_id
                quantity = move.product_uom_qty
                price_unit = 0.0

                # Dapatkan harga dari sales order
                for line in sale_order.order_line:
                    if line.product_id == product:
                        price_unit = line.price_unit
                        invoice_lines_to_sale_order_line[product.id] = line.id
                        break

                invoice_line_vals.append((0, 0, {
                    'product_id': product.id,
                    'quantity': quantity,
                    'price_unit': price_unit,
                    'name': product.name,
                    'move_line_ids': [(4, move.id)],  # tambahkan ini untuk link ke stock.move
                }))

        update_vals = {
            'picking_ids': picking_vals,
            'invoice_line_ids': invoice_line_vals,
            'from_invoice': True,
        }

        if picking_vals or invoice_line_vals:
            invoice.write(update_vals)

        # Update invoice_ids field in related stock.picking records
        for picking in self.picking_ids:
            picking.write({'invoice_ids': [(6, 0, invoice.ids)]})
            for line in invoice.invoice_line_ids:
                if line.product_id.id in invoice_lines_to_sale_order_line:
                    line.write({
                        'sale_line_ids': [(6,0, [invoice_lines_to_sale_order_line[line.product_id.id]])]
                        })
        return True

    
    def _get_domain_for_pickings(self):
        self.ensure_one()
        invoice = self.env["account.move"].browse(self._context.get("active_id", False))
        domain = [
            ('partner_id', '=', invoice.partner_id.id),
            ('state', '=', 'done'),
            ('invoice_ids', '=', False)
        ]
        return domain

    @api.onchange('picking_ids')
    def _onchange_picking_ids(self):
        domain = self._get_domain_for_pickings()
        return {'domain': {'picking_ids': domain}}