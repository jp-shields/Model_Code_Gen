from odoo import models, fields, api
from odoo.http import request

class IrModel(models.Model):
    _inherit = 'ir.model'


    def repr(self, obj,rec):
        def addParam(xf):
            xstr = ""
            if xf.required:
                xstr += ",required=True"
            if not xf.store:
                xstr += ",store=False"
            if xf.compute:
                xstr += ",compute='_compute_" + xf.name + "'"
            if xf.on_delete:
                xstr += ",ondelete=\"" + str(xf.on_delete) + "\""
            if xf.domain:
                xstr += ",\n\t\tdomain=" + str(xf.domain)
            if "context" in xf and xf["context"] != {}:
                xstr += ",\n\t\tcontext=" + str(xf["context"])
            if xf.help:
                xstr += ",\n\t\thelp=\"" + xf.help.replace("\n", "\\n").replace("\"", "\\""") + "\""
            return xstr

        xupfields = ('create_date', 'create_uid', 'write_uid', 'write_date')
        xmailfields = self.env['mail.thread'].fields_get()
        xstr = "class " + rec.model.replace(".", "_") + "(models.Model):\n" + \
               "\t_name = '" + rec.model + "'\n" + \
               "\t_description = '" + rec.name + "'\n" + \
               "\t_inherit = " + str(obj._inherit) + "\n" + \
               "\t_inherits = " + str(obj._inherits) + "\n" + \
               "\t_order = '" + str(obj._order) + "'\n\n"
        for xf in rec.field_id:
            if xf.name in xupfields and rec.model != "base":
                continue
            if xf.name in xmailfields and rec.model != "mail.thread" and rec.model != "base":
                continue
            if xf.compute:
                xstr += "\tdef _compute_" + xf.name + "(self):\n\t\t" + \
                        str(xf.compute).replace("\n", "\n\t\t") + "\n"
            if xf.ttype == "char":
                xstr += "\t" + xf.name + " = fields.Char(\"" + xf.field_description + "\"" + addParam(xf) + ")\n"
            elif xf.ttype == "text":
                xstr += "\t" + xf.name + " = fields.Text(\"" + xf.field_description + "\"" + addParam(xf) + ")\n"
            elif xf.ttype == "html":
                xstr += "\t" + xf.name + " = fields.Html(\"" + xf.field_description + "\"" + addParam(xf) + ")\n"
            elif xf.ttype == "date":
                xstr += "\t" + xf.name + " = fields.Date(\"" + xf.field_description + "\"" + addParam(xf) + ")\n"
            elif xf.ttype == "datetime":
                xstr += "\t" + xf.name + " = fields.DateTime(\"" + xf.field_description + "\"" + addParam(xf) + ")\n"
            elif xf.ttype == "boolean":
                xstr += "\t" + xf.name + " = fields.Boolean(\"" + xf.field_description + "\"" + addParam(xf) + ")\n"
            elif xf.ttype == "integer":
                xstr += "\t" + xf.name + " = fields.Integer(\"" + xf.field_description + "\"" + addParam(xf) + ")\n"
            elif xf.ttype == "float":
                xstr += "\t" + xf.name + " = fields.Float(\"" + xf.field_description + "\"" + addParam(xf) + ")\n"
            elif xf.ttype == "selection":
                xstr += "\t" + xf.name + " = fields.Selection(" + str(
                    xf.selection) + "\n\t\t,string=\"" + xf.field_description + "\"" + addParam(xf) + ")\n"
            elif xf.ttype == "many2one":
                xstr += "\t" + xf.name + " = fields.Many2one(\"" + xf.relation + "\",string=\"" + xf.field_description + "\"" + addParam(
                    xf) + ")\n"
            elif xf.ttype == "one2many":
                xstr += "\t" + xf.name + " = fields.One2many(\"" + xf.relation
                if xf.relation_field:
                    xstr += "\",\"" + xf.relation_field
                xstr += "\",string=\"" + xf.field_description + "\"" + addParam(xf) + ")\n"
            elif xf.ttype == "many2many":
                xstr += "\t" + xf.name + " = fields.Many2many(\"" + xf.relation + "\",\"" + \
                        str(xf.relation_table) + "\",\"" + \
                        str(xf.column1) + "\",\"" + \
                        str(xf.column2) + "\"\n\t\t" + addParam(xf) + ")\n"
            else:
                xstr += "\t # type '" + xf.ttype + "' not supported in field '" + xf.name + "'\n"
            xstr += "\n"
        for xc in dir(obj):
            if xc.startswith("_"):
                continue
            if xc in obj.fields_get():
                continue
            if xc in dir(self.env['mail.thread']):
                continue
            xstr += "\t # def " + str(xc) + "(self):\n"
        return xstr

    @api.multi
    @api.depends('name')
    def _get_repr(self):
        for rec in self:
            rec['x_repr'] = self.repr(self.env[rec.model],rec)
                #self.repr(self.env[rec.name])

    x_repr = fields.Char('repr',compute='_get_repr',store=False,
                         help="Generated based on fields in fields_get in self")