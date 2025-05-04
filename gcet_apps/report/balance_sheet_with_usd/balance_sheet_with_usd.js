// Get the original Balance Sheet report filters
var original_balance_sheet = frappe.query_reports["Balance Sheet"] || {};
var original_filters = original_balance_sheet.filters || [];

// Create a copy of the original filters
var filters = [];
if (Array.isArray(original_filters)) {
    filters = JSON.parse(JSON.stringify(original_filters));
} else {
    // Add default filters if original filters are not available
    filters = [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company"),
            "reqd": 1
        },
        {
            "fieldname": "periodicity",
            "label": __("Periodicity"),
            "fieldtype": "Select",
            "options": [
                { "value": "Monthly", "label": __("Monthly") },
                { "value": "Quarterly", "label": __("Quarterly") },
                { "value": "Half-Yearly", "label": __("Half-Yearly") },
                { "value": "Yearly", "label": __("Yearly") }
            ],
            "default": "Yearly",
            "reqd": 1
        },
        {
            "fieldname": "period_start_date",
            "label": __("Start Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -12),
            "reqd": 1
        },
        {
            "fieldname": "period_end_date",
            "label": __("End Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        }
    ];
}

// Define the report
frappe.query_reports["Balance Sheet with USD"] = {
    "filters": filters,
    
    "formatter": function(value, row, column, data, default_formatter) {
        if (column.fieldname && column.fieldname.includes("_usd")) {
            value = format_currency(value, "USD");
            return value;
        }
        
        // Use the original formatter for non-USD columns
        if (original_balance_sheet.formatter) {
            return original_balance_sheet.formatter(value, row, column, data, default_formatter);
        }
        
        return default_formatter(value, row, column, data);
    }
};

console.log("Balance Sheet with USD script loaded successfully"); 