from odoo import api, models

class ParticularReport(models.AbstractModel):
    _name = 'ha.model_particularreport'
    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('ha.views.report_ha')
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render('module.report_name', docargs)