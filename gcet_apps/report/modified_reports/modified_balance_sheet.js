frappe.query_reports["Balance Sheet"] = {
    "filters": [
        // Include all the original balance sheet filters here
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company"),
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
        },
        {
            "fieldname": "show_usd",
            "label": __("Show USD Values"),
            "fieldtype": "Check",
            "default": 1
        }
    ],
    
    "formatter": function(value, row, column, data, default_formatter) {
        console.log("Formatting column:", column.fieldname, "Value:", value);
        
        if (column.fieldname && column.fieldname.includes("_usd")) {
            console.log("USD column detected:", column.fieldname);
            value = format_currency(value, "USD");
            return value;
        }
        return default_formatter(value, row, column, data);
    }
};

// Add a simple console log to verify script loading
console.log("Modified Balance Sheet script loaded successfully");

// Add a document ready handler using vanilla JavaScript
document.addEventListener("DOMContentLoaded", function() {
    console.log("Document ready - Balance Sheet");
    
    // Check if we're on the Balance Sheet report page
    if (window.location.href.includes("Balance%20Sheet")) {
        console.log("On Balance Sheet report page");
        
        // Wait for report to render
        setTimeout(function() {
            console.log("Checking report data");
            if (frappe.query_report) {
                console.log("Report object found");
                console.log("Columns:", frappe.query_report.columns);
                console.log("Data sample:", frappe.query_report.data ? frappe.query_report.data.slice(0, 3) : "No data");
            }
        }, 2000);
    }
}); 