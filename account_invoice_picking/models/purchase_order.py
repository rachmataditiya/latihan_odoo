from odoo import models
from odoo.tools import float_compare, float_is_zero

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def get_stock_moves_link_invoice(self):
        moves_linked = self.env["stock.move"]
        to_invoice = self.qty_to_invoice  # Sesuaikan ini sesuai dengan field yang relevan di purchase.order.line
        precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        
        for stock_move in self.move_ids.sorted(
            lambda m: (m.write_date, m.id), reverse=True
        ):
            if (
                stock_move.state != "done"
                or stock_move.scrapped
                or (
                    stock_move.location_dest_id.usage != "supplier"
                    and (
                        stock_move.location_id.usage != "supplier"
                        or not stock_move.to_refund
                    )
                )
            ):
                continue
            
            # Sesuaikan logika di bawah ini sesuai kebutuhan Anda
            if float_is_zero(
                stock_move.product_qty, precision_digits=precision
            ):
                continue
            
            qty_on_hand = min(stock_move.product_qty, to_invoice)
            if float_is_zero(
                qty_on_hand, precision_digits=precision
            ):
                continue
            
            moves_linked |= stock_move
            to_invoice -= qty_on_hand
            
        return moves_linked
    
    def _prepare_account_move_line(self, **optional_values):
        vals = super()._prepare_account_move_line(**optional_values)
        stock_moves = self.get_stock_moves_link_invoice()

        # Invoice returned moves marked as to_refund
        if float_compare(
            self.qty_to_invoice, 0.0, precision_rounding=self.currency_id.rounding
        ) < 0:
            stock_moves = stock_moves.filtered("to_refund")
        
        vals["move_line_ids"] = [(4, m.id) for m in stock_moves]
        return vals