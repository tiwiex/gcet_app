frappe.query_reports["Idelta - Invoice Margin Analysis Report"] = {
    "filters": [
        {
            "fieldname": "sales_invoice",
            "label": __("Sales Invoice"),
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "default": frappe.query_report.get_filter_value("sales_invoice") || "",
            "reqd": 1  // Set to mandatory if you want to enforce the filter
        },
        // Additional filters can be added here if needed
    ]
};
