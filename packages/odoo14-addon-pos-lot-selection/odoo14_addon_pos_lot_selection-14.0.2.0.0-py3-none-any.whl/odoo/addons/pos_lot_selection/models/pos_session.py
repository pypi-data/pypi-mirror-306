# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class PosSession(models.Model):
    _inherit = "pos.session"

    @api.model
    def open_session_lot_serial_amount(self, product_id, lot, session_id=False):
        qty = 0.0
        domain = [('state', '!=', 'closed')]
        if session_id:
            domain += [('id', '=', session_id)]
        sessions = self.search(domain, limit=1)
        if sessions:
            lines = sessions.mapped('order_ids').mapped('lines').filtered(
                lambda a: a.product_id.id == product_id and a.pack_lot_ids and a.pack_lot_ids[0].lot_name == lot
            )
            if lines:
                qty = sum(lines.mapped('qty'))
        return qty
