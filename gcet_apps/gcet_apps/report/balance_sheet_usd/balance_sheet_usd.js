// Log when the script is loaded
console.log("Balance Sheet USD script loading...");

frappe.query_reports["Balance Sheet USD"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company"),
            "reqd": 1
        },
        {
            "fieldname": "usd_exchange_rate",
            "label": __("USD Exchange Rate (₦ → $)"),
            "fieldtype": "Float",
            "default": 1500.0,
            "description": __("Exchange rate for converting NGN to USD (e.g., 1500 means ₦1500 = $1)")
        },
        {
            "fieldname": "periodicity",
            "label": __("Periodicity"),
            "fieldtype": "Select",
            "options": "Monthly\nQuarterly\nHalf-Yearly\nYearly",
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
    ],
    
    "formatter": function(value, row, column, data, default_formatter) {
        console.log("Formatting column:", column.fieldname);
        
        if (column.fieldname && column.fieldname.includes("_usd")) {
            value = format_currency(value, "USD");
            return value;
        }
        
        return default_formatter(value, row, column, data);
    },
    
    "onload": function(report) {
        console.log("Report loaded:", report);
    }
};

console.log("Balance Sheet USD script loaded successfully");