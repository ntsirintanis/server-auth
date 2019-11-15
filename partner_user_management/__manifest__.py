# Copyright 2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Create customer user account",
    "summary": "Create user from partner",
    "category": "Tools",
    "version": "11.0.0.0.0",
    "author": "Odoo Community Association (OCA),Therp BV",
    "license": "AGPL-3",
    "website": 'https://github.com/oca/server-auth',
    "depends": [
        'base',
    ],
    "data": [
        'data/ir_cron.xml',
        'security/ir.model.access.csv',
        'views/res_company.xml',
        ],
    "installable": True,
}
