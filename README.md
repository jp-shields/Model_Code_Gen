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
- Also can not understand function, however it does list them as '# def method(self):' at the bottom

This is open source released under the LGPL Version 3
-----------------------------------------------------
See License file for details