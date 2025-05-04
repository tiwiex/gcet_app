import frappe
from frappe.model.document import Document
from frappe.core.doctype.report.report import Report
import json
from datetime import datetime, timedelta

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

    def execute_script_report(self, filters):
        # Ensure filters is a dictionary
        if isinstance(filters, str):
            filters = json.loads(filters)
            
        if not filters:
            filters = {}
            
        # For Balance Sheet report, ensure all required filters are set
        if self.name == "Balance Sheet":
            # Ensure periodicity is set
            if "periodicity" not in filters:
                filters["periodicity"] = "Yearly"
                
            # Ensure company is set
            if "company" not in filters:
                filters["company"] = frappe.defaults.get_user_default("Company")
                
            # Ensure dates are set
            if "period_start_date" not in filters:
                # Default to 1 year ago
                filters["period_start_date"] = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
                
            if "period_end_date" not in filters:
                # Default to today
                filters["period_end_date"] = datetime.now().strftime("%Y-%m-%d")
                
            frappe.msgprint(f"Using filters: {filters}")
            
        # Call the parent method with the updated filters
        return super().execute_script_report(filters)
