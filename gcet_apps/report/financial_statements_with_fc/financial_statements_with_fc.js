frappe.query_reports["Financial Statements with FC"] = $.extend({}, erpnext.financial_statements, {
    filters: [
        {
            fieldname: "company",
            label: __("Company"),
            fieldtype: "Link",
            options: "Company",
            default: frappe.defaults.get_user_default("Company"),
            reqd: 1
        },
        {
            fieldname: "from_date",
            label: __("From Date"),
            fieldtype: "Date",
            default: frappe.datetime.add_months(frappe.datetime.get_today(), -12),
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
            default: frappe.datetime.get_today(),
            reqd: 1
        },
        {
            fieldname: "secondary_currency",
            label: __("Secondary Currency"),
            fieldtype: "Link",
            options: "Currency",
            reqd: 1
        },
        {
            fieldname: "report_type",
            label: __("Report Type"),
            fieldtype: "Select",
            options: "Profit and Loss\nBalance Sheet\nCash Flow",
            default: "Profit and Loss",
            reqd: 1
        },
        {
            fieldname: "period_length",
            label: __("Period Length"),
            fieldtype: "Select",
            options: "Monthly\nQuarterly\nHalf-Yearly\nYearly",
            default: "Monthly",
            reqd: 1
        }
    ]
});

// Add dimensions support like other financial reports
erpnext.utils.add_dimensions('Financial Statements with FC', 10);