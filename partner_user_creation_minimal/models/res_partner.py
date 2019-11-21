# Copyright 2013-2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=missing-docstring,protected-access
import logging

from odoo import api, models


_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def cron_res_partner_user_creation(self):
        """Automatically create users for partners if enabled from company.

        Users will be created if partner has no user. This functionality
        is applicable to a multi-company setting as well.

        As user-creation is very resource intensive, only 128 users will be
        created at a time.
        """
        companies = self.env['res.company'].search([
            ('minimal_enable_autocreate', '=', True),
        ])
        for company in companies:
            partners = self.search([
                ('user_ids', '=', False),
                ('category_id', '=', company.minimal_category_id.id),
                '|',
                ('company_id', '=', company.id),
                ('company_id', '=', False),
            ], limit=128)
            partners.check_autocreate(company.minimal_template_user_id)

    @api.multi
    def check_autocreate(self, template_user):
        user_model = self.env['res.users']
        for this in self:
            login = this._get_login()
            if not login:
                continue
            _logger.info(
                "Creating user from partner with login %s and ID %d",
                login,
                this.id,
            )
            user_model._create_for_partner(
                this,
                template_user=template_user,
                login=login,
            )

    @api.multi
    def _get_login(self):
        """Get login name for user."""
        self.ensure_one()
        return self.email or False
