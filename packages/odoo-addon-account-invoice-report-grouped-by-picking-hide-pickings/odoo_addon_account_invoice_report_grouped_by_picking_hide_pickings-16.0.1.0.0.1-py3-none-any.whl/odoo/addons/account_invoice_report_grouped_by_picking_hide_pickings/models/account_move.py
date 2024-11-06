# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def lines_grouped_by_picking(self):
        res = super().lines_grouped_by_picking()
        to_remove = list(filter(lambda g: g["picking"].hide_on_invoice, res))
        for i in to_remove:
            res.remove(i)
        return res
