# -*- coding: utf-8 -*-

{
    'name': 'OVE - Structures',
    'version': '1.0',
    'category': 'InfoSaône',
    'description': """
OVE Gestion des droits liés aux structures
""",
    'author': 'Tony GALMICHE / Asma BOUSSELMI',
    'maintainer': 'InfoSaone',
    'website': 'http://www.infosaone.com',
    'depends': ['base', 'document', 'ove_groupe'],
    'data': ['security/ir.model.access.csv',
             'ove_structure_view.xml'],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
