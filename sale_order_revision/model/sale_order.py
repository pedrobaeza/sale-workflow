# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    @author Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#    @author Raphaël Valyi <raphael.valyi@akretion.com> (ported to sale from
#    original purchase_order_revision by Lorenzo Battistini)
#    Copyright (c) 2015 Serv. Tecnol. Avanzados (http://www.serviciosbaeza.com)
#                       Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import netsvc
from openerp.osv import fields, orm
from openerp.tools.translate import _


class SaleOrder(orm.Model):
    _inherit = "sale.order"

    _columns = {
        'current_revision_id': fields.many2one(
            'sale.order', 'Current revision', readonly=True),
        'old_revision_ids': fields.one2many(
            'sale.order', 'current_revision_id',
            'Old revisions', readonly=True, context={'active_test': False}),
        'revision_number': fields.integer('Revision'),
        'unrevisioned_name': fields.char('Order Reference', readonly=True),
        'active': fields.boolean('Active'),
        'create_date': fields.datetime('Date created', readonly=True),
        'create_uid':  fields.many2one('res.users', 'Creator', readonly=True),
    }

    _defaults = {
        'active': True,
    }

    _sql_constraints = [
        ('revision_unique',
         'unique(unrevisioned_name, revision_number, company_id)',
         'Order Reference and revision must be unique per Company.'),
    ]

    def copy_quotation(self, cr, uid, ids, context=None):
        if len(ids) > 1:
            raise orm.except_orm(
                _('Error'), _('This only works for 1 SO at a time'))
        ctx = context.copy()
        ctx['new_sale_revision'] = True
        action = super(SaleOrder, self).copy_quotation(
            cr, uid, ids, context=ctx)
        wf_service = netsvc.LocalService("workflow")
        wf_service.trg_delete(uid, 'sale.order', ids[0], cr)
        wf_service.trg_create(uid, 'sale.order', ids[0], cr)
        self.write(cr, uid, ids[0],
                   {'state': 'draft'}, context=context)
        order = self.browse(cr, uid, ids[0], context=context)
        action['res_id'] = ids[0]
        msg = _('New revision created: %s') % order.name
        self.message_post(cr, uid, action['res_id'], body=msg)
        return action

    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default['old_revision_ids'] = []
        if context.get('new_sale_revision'):
            rec = self.browse(cr, uid, id, context=context)
            prev_name = rec.name
            revno = rec.revision_number
            rec.write(
                {'revision_number': revno + 1,
                 'name': '%s-%02d' % (rec.unrevisioned_name, revno + 1)},
                context=context)
            default.update({
                'name': prev_name,
                'revision_number': revno,
                'active': False,
                'state': 'cancel',
                'current_revision_id': id,
                'invoice_ids': []})
            # Call directly Model write, because sale standard copy method
            # mess up some fields, like state or name
            return orm.Model.copy(self, cr, uid, id, default, context=context)
        else:
            default['current_revision_id'] = False
            default['unrevisioned_name'] = False
            default['revision_number'] = 0
        return super(SaleOrder, self).copy(
            cr, uid, id, default=default, context=context)

    def create(self, cr, uid, values, context=None):
        if 'unrevisioned_name' not in values:
            if values.get('name', '/') == '/':
                values['name'] = self.pool['ir.sequence'].next_by_code(
                    cr, uid, 'sale.order', context=context) or '/'
            values['unrevisioned_name'] = values['name']
        return super(SaleOrder, self).create(cr, uid, values, context=context)

