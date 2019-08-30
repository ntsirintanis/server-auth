# Copyright 2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=missing-docstring
from odoo import fields, models


class PartnerUserManagement(models.Model):
    _name = 'partner.user.management'
    _description = "Configuration of user-management by partner-managers."

    name = fields.Char()
    # Fields to limit the application of this configuration.
    category_id = fields.Many2one(
        comodel_name='res.partner.category',
        help="Partner category to which this configuration applies")
    # What can be done with partner / users for this configuration.
    template_user_id = fields.Many2one(
        comodel_name='res.users',
        string='Template for users on partners')
    allow_create_user = fields.Boolean(
        string='Allow partner managers to create users')
    auto_create_user = fields.Boolean(
        string='Create user automatically',
        help="Create user automatically if conditions met.\n"
             " Conditions like right category and email valid.")
    allow_password_reset_mail = fields.Boolean(
        string='Sending of passport reset mail allowed',
        help="Allow partner managers to send password reset mail")
    # Who can manage users (default all partner managers).
    partner_manager_ids = fields.Many2many(
        comodel_name='res.users',
        domain=lambda self: [
            ('groups_id', '=', self.env.ref('base.group_partner_manager').id)],
        help="Users allowed to manage other users for this configuration")
