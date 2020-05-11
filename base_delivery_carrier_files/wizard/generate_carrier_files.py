# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Guewen Baconnier
#    Copyright 2012 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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

from odoo import models, fields, api, exceptions, _


class DeliveryCarrierFileGenerate(models.TransientModel):

    _name = 'delivery.carrier.file.generate'

    def _get_picking_ids(self):
        context = self.env.context or {}
        res = False
        if (context.get('active_model', False) == 'stock.picking' and
                context.get('active_ids', False)):
            res = context['active_ids']
        return res

    picking_ids =  fields.Many2many('stock.picking',
                                    string='Delivery Orders',
                                    default=_get_picking_ids)
    recreate =  fields.Boolean(
        'Recreate files',
        help="If this option is used, new files will be generated "
             "for selected picking even if they already had one.\n"
             "By default, delivery orders with existing file will be "
             "skipped.")

    @api.multi
    def action_generate(self):
        """
        Call the creation of the delivery carrier files
        """
        context = self.env.context or {}
        for form in self:
            if not form.picking_ids:
                raise exceptions.except_orm(_('Error'), _('No delivery orders selected'))
    
            picking_obj = self.env['stock.picking']
            picking_ids = [picking.id for picking in form.picking_ids]
            picking_obj.generate_carrier_files(picking_ids,
                                               auto=False,
                                               recreate=form.recreate
                                               )

        return {'type': 'ir.actions.act_window_close'}
