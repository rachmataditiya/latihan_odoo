# -*- coding: utf-8 -*-

{
    'name': 'Picking to Invoice',
    'category': 'stock',
    'summary': 'invoice based on stock picking',
    'version': '1.0',
    'license': 'OPL-1',
    'description': """
        membuat invoice dari stock picking dan menyambungkan invoice tersebut dengan so terkait.
    """,
    'depends': ['stock_picking_invoice_link'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_views.xml',
        'wizards/add_picking_wizard.xml',
    ],
    'installable': True,
    'auto_install': True,
    'author': 'Arkana Solusi Digital',
    'website': 'https://www.arkana.co.id',
}
