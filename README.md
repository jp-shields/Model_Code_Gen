Model Code Gen
==============

View Python Code to Generate Model
----------------------------------

- This tool adds a menu item "Models" to your ODOO instance
- From there you can see all the models in you instance (same as Settings / Technical / Database structure / Models)
- Open a model to see the attributes including a new page tab "Code"
- This tab contains a calculated field "repr" with attempts to generate the python code to generate the current model

**Note:** This does not look at actual python files for base models:

- as such can not read the many2many field correctly on base models
- Also can not understand functions in base models

Convert Custom Models / Fields to Base Models / Fields
------------------------------------------------------

- Pull up a custom module to view the python code it would need to create it
- ODOO Studio customizations can be converted to python

    **Still a work in progress**
See [Github project for details](https://github.com/jp-shields/Model_Code_Gen)

Install:
--------

- Download the zip file from See [Github](https://github.com/jp-shields/Model_Code_Gen) 
- Enable developer mode in ODOO (on settings dashboard)
- Go to Apps / Import Module to upload the Zip

This is open source released under the LGPL Version 3
-----------------------------------------------------
See License file for details