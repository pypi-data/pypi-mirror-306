# Copyright 2021 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Balance Zero",
    "summary": "Generate an accounting entry with the opposite balances.",
    "version": "13.0.1.0.0",
    "category": "Accounting",
    "website": "https://www.sygel.es",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "account",
    ],
    "data": [
        "wizard/account_balance_zero.xml"
    ],
}
