console.log("Multi-Currency Trial Balance report JS loading...");

// Standard JS date utilities
const dateUtils = {
    formatDate(date) {
        if (!date) return '';
        if (typeof date === 'string') date = new Date(date);
        return date.toISOString().split('T')[0];
    },
    
    addMonths(date, months) {
        const newDate = new Date(date);
        newDate.setMonth(newDate.getMonth() + months);
        return newDate;
    },
    
    today() {
        return new Date();
    }
};

// Report configuration
frappe.query_reports["Multi-Currency Trial Balance"] = {
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
            reqd: 1
        },
        {
            fieldname: "to_date",
            label: __("To Date"),
            fieldtype: "Date",
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
            fieldname: "show_zero_balance",
            label: __("Show Zero Balances"),
            fieldtype: "Check",
            default: 0
        }
    ]
};
