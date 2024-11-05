# Copyright 2020 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def _check_balanced(self):
        overwritten = True


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    _sql_constraints = [
        (
            'check_credit_debit',
            'CHECK(TRUE=TRUE)',
            'Wrong credit or debit value in accounting entry !'
        )
    ]
