# Copyright 2024 Roger Sans <roger.sans@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class CrossoveredBudget(models.Model):
    _inherit = "crossovered.budget"

    def assign_budget_lines_dates(self):
        for line in self.crossovered_budget_line:
            line.write({"date_from": self.date_from, "date_to": self.date_to})
