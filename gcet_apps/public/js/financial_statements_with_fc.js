console.log("Loading Financial Statements with FC report configuration...");

frappe.query_reports["Financial Statements with FC"] = {
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
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -12),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        },
        {
            "fieldname": "secondary_currency",
            "label": __("Secondary Currency"),
            "fieldtype": "Link",
            "options": "Currency",
            "reqd": 1
        },
        {
            "fieldname": "report_type",
            "label": __("Report Type"),
            "fieldtype": "Select",
            "options": "Profit and Loss\nBalance Sheet\nCash Flow",
            "default": "Profit and Loss",
            "reqd": 1
        },
        {
            "fieldname": "period_length",
            "label": __("Period Length"),
            "fieldtype": "Select",
            "options": "Monthly\nQuarterly\nHalf-Yearly\nYearly",
            "default": "Monthly",
            "reqd": 1
        }
    ],

    onload: function(report) {
        try {
            console.log("Report onload triggered");
            
            // Wait for filters to be ready
            setTimeout(() => {
                try {
                    // Set default values
                    const defaults = {
                        company: frappe.defaults.get_user_default("Company"),
                        from_date: frappe.datetime.add_months(frappe.datetime.get_today(), -12),
                        to_date: frappe.datetime.get_today(),
                        report_type: "Profit and Loss",
                        period_length: "Monthly"
                    };

                    Object.entries(defaults).forEach(([key, value]) => {
                        if (value) {
                            frappe.query_report.set_filter_value(key, value);
                        }
                    });

                    // Add export button
                    report.page.add_inner_button(__("Export"), function() {
                        var filters = report.get_values();
                        frappe.set_route("Form", "Financial Statement", "New Financial Statement", {
                            company: filters.company,
                            from_date: filters.from_date,
                            to_date: filters.to_date,
                            secondary_currency: filters.secondary_currency
                        });
                    });
                } catch (err) {
                    console.error("Error in setting default values:", err);
                }
            }, 1000);
        } catch (err) {
            console.error("Error in onload:", err);
        }
    }
};

// Debug logging
$(document).ready(function() {
    try {
        console.log("Document ready");
        console.log("Report configuration:", frappe.query_reports["Financial Statements with FC"]);
    } catch (err) {
        console.error("Error in document ready:", err);
    }
});
