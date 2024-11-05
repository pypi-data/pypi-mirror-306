# Copyright 2024 Roger Sans <roger.sans@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Budget Propagate Date",
    "version": "15.0.1.0.0",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "category": "Account",
    "summary": "Apply the budget dates to lines.",
    "website": "https://github.com/sygel-technology/sy-account-budgeting",
    "depends": [
        "account_budget",
    ],
    "data": [
        "views/crossovered_budget_view.xml",
    ],
}
