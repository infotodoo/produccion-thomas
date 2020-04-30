# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def button_mark_done(self):
        res = super(MrpProduction, self).button_mark_done()
        self.create_move_workcenter()
        return res

    def create_move_workcenter(self):
        am_obj = self.env['account.move']
        for record in self:
            product_id = record.product_id
            journal_id = product_id.categ_id.property_stock_journal
            if not journal_id:
                raise ValidationError("EL producto [%s] %s no tiene un diario asignado en su categoria" % (product_id.default_code, product_id.name))
            if record.routing_id:
                for operation in record.routing_id.operation_ids:
                    line_ids = operation.workcenter_id._prepare_move_line(record.id, record.name)
                    if line_ids:
                        move = {
                            'journal_id': journal_id.id,
                            'line_ids': line_ids,
                            'date': fields.Date.today(),
                            'ref': record.name + ' - ' + operation.name,
                            'type': 'entry'
                        }
                        account_move = am_obj.sudo().create(move)
                        account_move.post()
