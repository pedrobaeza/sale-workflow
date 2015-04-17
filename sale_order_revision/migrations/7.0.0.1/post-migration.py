# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################


def migrate(cr, version):
    if not version:
        # Do it only on first install
        cr.execute("""
            UPDATE sale_order
            SET unrevisioned_name=name
            WHERE unrevisioned_name IS NULL""")
