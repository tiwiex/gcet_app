import frappe

def setup_report():
    # Check if report exists
    if frappe.db.exists("Report", "Balance Sheet USD"):
        # Update the report
        report = frappe.get_doc("Report", "Balance Sheet USD")
        report.module = "GCET Apps"
        report.reference_report = "Balance Sheet"
        report.report_type = "Script Report"
        report.is_standard = "No"
        report.disabled = 0
        report.report_script_module = "gcet_apps.report.balance_sheet_usd.balance_sheet_usd"
        report.save()
        frappe.db.commit()
        print("Report updated successfully")
    else:
        print("Report not found")

# Run this function
setup_report()