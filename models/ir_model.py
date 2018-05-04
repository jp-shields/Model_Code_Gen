from odoo import models, fields, api
from odoo.http import request

class IrModel(models.Model):
    _inherit = 'ir.model'

    def _addParam(self,xparams):
        xstr = ""
        if xparams["required"]:
            xstr += ",required=True"
        if xparams["searchable"]:
            xstr += ",searchable=True"
        if xparams["manual"]:
            xstr += ",manual=True"
        if xparams["company_dependent"]:
            xstr += ",company_dependent=True"
        if not xparams["store"]:
            xstr += ",store=False"
        if "ondelete" in xparams:
            xstr += ",ondelete=\"" + xparams["ondelete"] + "\""
        if "domain" in xparams and xparams["domain"] != []:
            xstr += ",\n\t\tdomain=" + str(xparams["domain"])
        if "context" in xparams and xparams["context"] != {}:
            xstr += ",\n\t\tcontext=" + str(xparams["context"])
        if "help" in xparams:
            xstr += ",\n\t\thelp=\"" + xparams["help"].replace("\n","\\n").replace("\"","\\""") + "\""
        return xstr

    def repr(self, obj):
        xstr = "class " + obj._name.replace(".","_") + "(models.Model):\n" +\
            "\t_name = '" + obj._name + "'\n" +\
            "\t_description = '" + obj._description + "'\n" +\
            "\t_inherit = " + str(obj._inherit) + "\n" +\
            "\t_inherits = " + str(obj._inherits) + "\n" +\
            "\t_order = '" + str(obj._order) + "'\n\n"

        xfields = obj.fields_get()
        xupfields = ('create_date','create_uid','write_uid','write_date')
        xmailfields = self.env['mail.thread'].fields_get()
        for xf,xv in xfields.items():
            if xf in xupfields and obj._name != "base":
                continue
            if xf in xmailfields and obj._name != "mail.thread" and obj._name != "base":
                continue
            if xv["type"] == "char":
                xstr += "\t" + xf + " = fields.Char(\"" + xv["string"] + "\""+ self._addParam(xv) + ")\n"
            elif xv["type"] == "text":
                xstr += "\t" + xf + " = fields.Text(\"" + xv["string"] + "\""+ self._addParam(xv) + ")\n"
            elif xv["type"] == "html":
                xstr += "\t" + xf + " = fields.Html(\"" + xv["string"] + "\""+ self._addParam(xv) + ")\n"
            elif xv["type"] == "date":
                xstr += "\t" + xf + " = fields.Date(\"" + xv["string"] + "\""+ self._addParam(xv) + ")\n"
            elif xv["type"] == "datetime":
                xstr += "\t" + xf + " = fields.DateTime(\"" + xv["string"] + "\""+ self._addParam(xv) + ")\n"
            elif xv["type"] == "boolean":
                xstr += "\t" + xf + " = fields.Boolean(\"" + xv["string"] + "\""+ self._addParam(xv) + ")\n"
            elif xv["type"] == "integer":
                xstr += "\t" + xf + " = fields.Integer(\"" + xv["string"] + "\""+ self._addParam(xv) + ")\n"
            elif xv["type"] == "float":
                xstr += "\t" + xf + " = fields.Float(\"" + xv["string"] + "\""+ self._addParam(xv) + ")\n"
            elif xv["type"] == "selection":
                xstr += "\t" + xf + " = fields.Selection(" + str(xv["selection"]) + "\n\t\t,string=\"" + xv["string"] + "\""+ self._addParam(xv) + ")\n"
            elif xv["type"] == "many2one":
                xstr += "\t" + xf + " = fields.Many2one(\"" + xv["relation"] + "\",string=\"" + xv["string"] + "\""+ self._addParam(xv) + ")\n"
            elif xv["type"] == "one2many":
                xstr += "\t" + xf + " = fields.One2many(\"" + xv["relation"]
                if "relation_field" in xv:
                    xstr += "\",\"" + xv["relation_field"]
                xstr += "\",string=\"" + xv["string"] + "\""+ self._addParam(xv) + ")\n"
            elif xv["type"] == "many2many":
                iField = self.env['ir.model.fields'].search([("name","=",xf),("model_id","=",obj._name)])
                xstr += "\t" + xf + " = fields.Many2many(\"" + xv["relation"] + "\",\"" + \
                    str(iField[0].relation_table) + "\",\"" + \
                        str(iField[0].column1) + "\",\"" + \
                        str(iField[0].column2) + "\"\n\t\t" + self._addParam(xv) + ")\n"
            else:
                xstr += "\t # type '" + xv["type"] + "' not supported in field '" + xf +"'\n"
                if request.debug:
                    xstr += "\t #  " + str(xv) + "\n\n"
                continue
            if request.debug:
                xstr += "\t #  " + xf + ": " + str(xv) + "\n"
            xstr += "\n"
        for xc in dir(obj):
            if xc.startswith("_"):
                continue
            if xc in xfields:
                continue
            if xc in dir(self.env['mail.thread']):
                continue
            xstr += "\t # def " + str(xc) + "(self):\n"
        return xstr

    @api.multi
    @api.depends('name')
    def _get_repr(self):
        for rec in self:
            rec['x_repr'] = self.repr(self.env[rec.model])
                #self.repr(self.env[rec.name])

    x_repr = fields.Char('repr',compute='_get_repr',store=False,
                         help="Generated based on fields in fields_get in self")