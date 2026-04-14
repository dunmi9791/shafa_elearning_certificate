# -*- coding: utf-8 -*-
{
    'name': 'Shafa eLearning Custom Certificate',
    'version': '18.0.1.0.0',
    'summary': 'Replaces the default Odoo eLearning certificate with the A.Y.M Shafa branded design',
    'description': """
        Custom eLearning Certificate for A.Y.M Shafa Limited.
        - Landscape A4 layout
        - Shafa branded design with logo, verified badge, and signatory details
        - Overrides slide.report_slide_channel_certification template
    """,
    'author': 'A.Y.M Shafa Limited',
    'category': 'eLearning',
    'depends': ['website_slides', 'survey'],
    'data': [
        'report/slide_channel_certification.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}