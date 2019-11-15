# Copyright 2013-2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=missing-docstring
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    minimal_template_user_id = fields.Many2one(
        comodel_name="res.users",
        string="User template",
    )
    minimal_enable_autocreate = fields.Boolean(
        string="Enable autocreate",
        help="When set users will be automatically created if possible.",
    )
    minimal_category_id = fields.Many2one(
        comodel_name="res.partner.category",
        string="Partner category",
        help="Create users from partners in this category")
