# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013 Agile Business Group sagl (<http://www.agilebg.com>)
#    @author Lorenzo Battistini <lorenzo.battistini@agilebg.com>
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

{
    'name': "Sale order revisions",
    'version': '1.0',
    'category': 'Sale Management',
    'author': 'Agile Business Group, '
              'Akretion, '
              'Camptocamp, '
              'Serv. Tecnol. Avanzados - Pedro M. Baeza, '
              'Odoo Community Association (OCA)',
    'website': 'http://www.agilebg.com',
    'license': 'AGPL-3',
    "depends": ['sale'],
    "description": """
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License

Revisions for sale orders (and quotations)
==========================================

On cancelled orders, you can click on the "New copy of Quotation" button. This
will create a new revision of the quotation, with the same base number and a
'-revno' suffix appended. A message is added in the chatter saying that a new
revision was created.

In the form view, a new tab is added that lists the previous revisions, with
the date they were made obsolete and the user who performed the action.

The old revisions of a sale order are flagged as inactive, so they don't
clutter up searches.

Credits
=======

Contributors
------------

* Lorenzo Battistini <lorenzo.battistini@agilebg.com>
* Raphael Valyi <rvalyi@akretion.com>
* Alexandre Fayolle <alexandre.fayolle@camptocamp.com>
* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
    """,
    "data": [
        'view/sale_order.xml',
        ],
    "test": [
        'test/sale_order.yml',
        ],
    "installable": True
}
