import frappe
from frappe.model.document import Document
from frappe.core.doctype.report.report import Report

class CustomReport(Report):
    def get_override_module(self):
        if self.report_name == "Balance Sheet":
            return "gcet_apps.gcet_apps.report.modified_reports.modified_balance_sheet"
        elif self.report_name == "Profit and Loss Statement":
            return "gcet_apps.gcet_apps.report.modified_reports.modified_profit_and_loss"
        return None

    def execute(self, filters=None):
        override_module = self.get_override_module()
        if override_module:
            module = frappe.get_module(override_module)
            if hasattr(module, 'execute'):
                return module.execute(filters)
        return super().execute(filters)
