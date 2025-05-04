// Get the original Balance Sheet report filters
var original_balance_sheet = frappe.query_reports["Balance Sheet"] || {};
var original_filters = original_balance_sheet.filters || [];

// Create a copy of the original filters
var filters = JSON.parse(JSON.stringify(original_filters));

// Add our custom filter
filters.push({
    "fieldname": "show_usd",
    "label": __("Show USD Values"),
    "fieldtype": "Check",
    "default": 1
});

// Update the report with our extended filters
frappe.query_reports["Balance Sheet"] = {
    "filters": filters,
    
    "formatter": function(value, row, column, data, default_formatter) {
        // Use the original formatter if available
        var original_formatter = original_balance_sheet.formatter || default_formatter;
        
        if (column.fieldname && column.fieldname.includes("_usd")) {
            value = format_currency(value, "USD");
            return value;
        }
        
        return original_formatter(value, row, column, data, default_formatter);
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