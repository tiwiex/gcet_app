frappe.query_reports["Idelta - Invoice Margin Analysis Report"] = {
    "filters": [
        {
            "fieldname": "sales_invoice",
            "label": __("Sales Invoice"),
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "default": "",
            "reqd": 0
        }
    ]
};
