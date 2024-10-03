from odoo import models

class ReportBackendOperations(models.AbstractModel):
    _name = 'report.inventory_report.report_backend_operations'
    _description = 'Backend Operations Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.picking'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'stock.picking',
            'docs': docs,
            'data': data,  # include this for completeness
        }
