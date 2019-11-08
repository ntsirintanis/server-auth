# Copyright 2013-2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=missing-docstring,protected-access
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _compute_partner_management(self):
        """Selection of applicable partner management.

        Record rules should take care that user is shown only
        a configuration she is entitled to.
        """
        management_model = self.env['partner.user.management']
        for this in self:
            # First try to find for specific category:
            management_domain = [('category_id', 'in', this.category_id.ids)]
            management = management_model.search(management_domain)
            if not management:
                management = management_model.search([])
            if not management:
                this.partner_management_id = False
                this.can_create_user = False
                this.can_sent_password_reset_mail = False
            this.management_id = management
            this.can_create_user = True \
                if management.allow_create_user and not this.user_ids \
                else False
            this.can_sent_password_reset_mail = True \
                if management.allow_password_reset_mail and this.user_ids \
                else False

    partner_management_id = fields.One2many(
        string="Applicable partner management configuration",
        compute='_compute_partner_management',
        help="Active partner mangement will depend on logged in user")
    can_create_user = fields.Boolean(
        string="Can create user now?",
        compute='_compute_partner_management')
    can_sent_password_reset_mail = fields.Boolean(
        string="Can sent password reset mail?",
        compute='_compute_partner_management')

    @api.multi
    def action_create_user(self):
        """Start wizard to create user for partner."""
        self.ensure_one()
        user_model = self.env['res.users']
        user_model.create_for_partner(self.partner_id)

    @api.multi
    def action_show_user(self):
        """Start wizard to create user for partner."""
        self.ensure_one()
        return {
            'name': 'User',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'res.users',
            'domain': [],
            'context': self.env.context,
            'type': 'ir.actions.act_window',
            'target': 'blank',
            'res_id': self.user_ids[0].id}

    @api.model
    def cron_res_partner_user_creation(self):
        """Automatically create users for partners if enabled.

        Users will be created if partner has no user, and this is enabled
        on the company for the partner, or else the company of the current
        user.

        As user-creation is very resource intensive, only 128 users will be
        created at a time.
        """
        partners = self.search([('user_ids', '=', False)], limit=128)
        partners.check_autocreate()

    @api.multi
    def check_autocreate(self):
        user_model = self.env['res.users']
        for this in self:
            if this.user_ids:
                continue
            company = this.company_id or self.env.user.company_id
            if not company.enable_autocreate:
                continue
            login = this._get_login()
            if not login:
                continue
            user_model.create_for_partner(this, login=login)

    @api.multi
    def _get_login(self):
        """Get login name for user."""
        self.ensure_one()
        return self.email or False
