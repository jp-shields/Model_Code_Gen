# -*- coding: utf-8 -*-
{
    'name': 'Model_Code_Gen',
    'version': '11.0.9.0',
    'sequence': 5,
    'summary': 'View Python Code to generate Model',
    'category': 'Studio',
    'author': 'Joe Shields',
    'depends': [
        'base','base_setup', "mail",
    ],
    'data': [
        'views/ir_model_views.xml',
        'menu/model_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'images': [
        'static/description/icon.png',
    ],
    'website':'https://github.com/jp-shields/Model_Code_Gen'
}
