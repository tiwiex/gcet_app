// Wait for document ready
frappe.provide('gcet_apps.balance_sheet');

gcet_apps.balance_sheet = {
    init: function() {
        console.log("Balance Sheet JS loaded");
        
        // Add event listener to check when the report is loaded
        $(document).on('report:refresh', function() {
            console.log("Report refreshed");
            // Check if the USD column exists
            const columns = $('.dt-row-0 .dt-cell');
            let hasUsdColumn = false;
            
            columns.each(function() {
                const cell = $(this);
                const fieldname = cell.attr('data-fieldname');
                if (fieldname === 'amount_usd') {
                    hasUsdColumn = true;
                    cell.show();
                }
            });
            
            console.log("USD column exists:", hasUsdColumn);
        });
        
        // Add event listener for report generation
        $(document).on('report:generate', function() {
            console.log("Report generation started");
        });

        // Add event listener for report data load
        $(document).on('report:data-loaded', function() {
            console.log("Report data loaded");
            const columns = $('.dt-row-0 .dt-cell');
            let hasUsdValues = false;
            
            columns.each(function() {
                const cell = $(this);
                const fieldname = cell.attr('data-fieldname');
                if (fieldname === 'amount_usd') {
                    const value = cell.text().trim();
                    if (value && value !== '0.00') {
                        hasUsdValues = true;
                    }
                }
            });
            
            console.log("USD values found:", hasUsdValues);
        });
    }
};

// Initialize when Frappe is ready
frappe.dom.ready(function() {
    gcet_apps.balance_sheet.init();
});