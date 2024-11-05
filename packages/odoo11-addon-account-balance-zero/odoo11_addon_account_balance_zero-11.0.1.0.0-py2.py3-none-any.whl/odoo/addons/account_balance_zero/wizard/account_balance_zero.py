# Copyright 2021 Valentin Vinagre <valentin.vinagre@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountBalanceZero(models.TransientModel):
    _name = "account.balance.zero"
    _description = "Wizard to generate move of balances to zero"

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        required=True,
        readonly=True,
        default=lambda self: self.env.user.company_id
    )
    partner_id = fields.Many2many(
        comodel_name='res.partner',
        string='Filter Partner',
        domain=['|', ('parent_id', '=', False), ('is_company', '=', True)]
    )
    date_from = fields.Date(
        string="Date From",
        required=True
    )
    date_to = fields.Date(
        string="Date To",
        required=True,
        default=fields.Date.context_today
    )
    filter_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string="Journal",
        domain="[('company_id', '=', company_id)]"
    )
    account_ids = fields.Many2many(
        string="Accounts",
        comodel_name="account.account",
        domain="[('deprecated', '=', False), ('company_id', '=', company_id)]"
    )
    move_state = fields.Selection([
        ('posted', 'Posted'),
        ('all', 'All')
        ],
        string='Move State',
        required=True,
        default='posted',
    )
    dest_journal_id = fields.Many2one(
        comodel_name='account.journal',
        string="Destination Journal",
        domain="[('company_id', '=', company_id)]",
        required=True
    )

    @api.multi
    def calculate(self):
        domain = [
          ('company_id', '=', self.company_id.id),
          ('date', '<=', self.date_to),
          ('date', '>=', self.date_from),
          ('balance', '!=', 0.00)
        ]
        if self.move_state == 'posted':
            domain.append(('move_id.state', '=', 'posted'))
        if self.account_ids:
            domain.append(('account_id', 'in', self.account_ids.ids))
        if self.filter_journal_id:
            domain.append(('journal_id', '=', self.filter_journal_id.id))
        if self.partner_id:
            domain.append(('partner_id', 'in', self.partner_id.ids))

        fields = ['account_id', 'partner_id', 'balance']
        groupby = ['account_id', 'partner_id']

        mls_group = self.env['account.move.line'].read_group(
          domain=domain,
          fields=fields,
          groupby=groupby,
          lazy=False
        )

        data = []
        for ml_g in mls_group:
            data.append((0, 0, {
                'partner_id': ml_g['partner_id'][0] if ml_g['partner_id'] else False,
                'date': self.date_to,
                'company_id': self.company_id.id,
                'account_id': ml_g['account_id'][0],
                'debit': round(-1 * ml_g['balance'], 2) if ml_g['balance'] < 0 else 0.0,
                'credit': round(ml_g['balance'], 2) if ml_g['balance'] > 0 else 0.0,
                'journal_id': self.dest_journal_id.id
            }))

        am = self.env['account.move'].create({
          'company_id': self.company_id.id,
          'date': self.date_to,
          'journal_id': self.dest_journal_id.id,
          'ref': 'Compensation to 0 from %s to %s' % (self.date_from, self.date_to),
          'line_ids': data
        })

        action = self.env.ref('account.action_move_journal_line').read()[0]
        action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
        action['res_id'] = am.id
        return action
