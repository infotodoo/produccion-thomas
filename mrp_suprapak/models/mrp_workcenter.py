# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    costs_hour_mod = fields.Float('MOD per hour', help='Workforce cost', default=0.0)
    costs_hour_cif = fields.Float('CIF per hour', help='Indirect manufacturing costs', default=0.0)
    costs_hour_maq = fields.Float('Machine per hour', help='Machinery cost', default=0.0)
    mod_account_id = fields.Many2one('account.account', 'MOD account')
    account_mod_id = fields.Many2one('account.account', 'Counterpart MOD')
    cif_account_id = fields.Many2one('account.account', 'CIF account')
    account_cif_id = fields.Many2one('account.account', 'Counterpart CIF')
    maq_account_id = fields.Many2one('account.account', 'MAQ account')
    account_maq_id = fields.Many2one('account.account', 'Counterpart MAQ')
    # process_account_id = fields.Many2one('account.account', 'Process Product')
    
    @api.onchange('costs_hour_mod', 'costs_hour_cif', 'costs_hour_maq')
    def _onchange_costs(self):
        self.costs_hour = self.costs_hour_mod + self.costs_hour_cif + self.costs_hour_maq

    def _prepare_move_line(self, ids, name):
        line_ids = []
        # credit = 0.00
        partner_id = self.company_id.partner_id.id
        if self.costs_hour_mod and self.mod_account_id and self.account_mod_id:
            time = self._query_workcenter_time(ids)
            line = {
                'name': name + ' - ' + 'Mano de obra',
                'partner_id': partner_id,
                'debit': time * self.costs_hour_mod,
                'credit': 0.00,
                'account_id': self.mod_account_id.id
            }
            line_ids.append((0,0,line))
            line = {
                'name': name + ' - ' + 'Contrapartida MOD',
                'partner_id': partner_id,
                'debit': 0.00,
                'credit': time * self.costs_hour_mod,
                'account_id': self.account_mod_id.id
            }
            line_ids.append((0,0,line))
            # credit += self.costs_hour_mod
        if self.costs_hour_cif and self.cif_account_id and self.account_cif_id:
            line = {
                'name': name + ' - ' + 'Costo indirecto de fabricacion',
                'partner_id': partner_id,
                'debit': time * self.costs_hour_cif,
                'credit': 0.00,
                'account_id': self.cif_account_id.id
            }
            line_ids.append((0,0,line))
            line = {
                'name': name + ' - ' + 'Contrapartida CIF',
                'partner_id': partner_id,
                'debit': 0.00,
                'credit': time * self.costs_hour_cif,
                'account_id': self.account_cif_id.id
            }
            line_ids.append((0,0,line))
            # credit += self.costs_hour_cif
        if self.costs_hour_maq and self.maq_account_id and self.account_maq_id:
            line = {
                'name': name + ' - ' + 'Maquinaria',
                'partner_id': partner_id,
                'debit': time * self.costs_hour_maq,
                'credit': 0.00,
                'account_id': self.maq_account_id.id
            }
            line_ids.append((0,0,line))
            line = {
                'name': name + ' - ' + 'Contrapartida MAQ',
                'partner_id': partner_id,
                'debit': 0.00,
                'credit': time * self.costs_hour_maq,
                'account_id': self.account_maq_id.id
            }
            line_ids.append((0,0,line))
            # credit += self.costs_hour_maq
        '''if credit > 0.00:
            line = {
                'name': name + ' - ' + 'Producto en proceso',
                'partner_id': partner_id,
                'debit': 0.00,
                'credit': credit,
                'account_id': self.process_account_id.id
            }
            line_ids.append((0,0,line))'''
        return line_ids

    def _query_workcenter_time(self, ids):
        query_str = """SELECT sum(t.duration), wc.costs_hour
                    FROM mrp_workcenter_productivity t
                    LEFT JOIN mrp_workorder w ON (w.id = t.workorder_id)
                    LEFT JOIN mrp_workcenter wc ON (wc.id = t.workcenter_id )
                    WHERE t.workorder_id IS NOT NULL AND w.production_id = %s AND wc.id = %s
                    GROUP BY wc.costs_hour"""
        self.env.cr.execute(query_str, (ids, self.id))
        time = 0.00
        for duration, costs_hour in self.env.cr.fetchall():
            time = duration / 60.0
        return time
