// Wait for jQuery to be loaded
$(document).ready(function() {
    console.log("Balance Sheet JS loaded Fast");
    
    // Add event listener to check when the report is loaded
    $(document).on("report-refresh", function() {
        console.log("Report refreshed");
        // Check if the USD column exists
        const columns = $('.grid-row').find('.grid-cell');
        let hasUsdColumn = false;
        
        columns.each(function() {
            const cell = $(this);
            const fieldname = cell.data('fieldname');
            if (fieldname === 'amount_usd') {
                hasUsdColumn = true;
                cell.show();
            }
        });
        
        console.log("USD column exists:", hasUsdColumn);
    });
    
    // Add event listener for report generation
    $(document).on("report-generate", function() {
        console.log("Report generation started");
    });

    // Add event listener for report data load
    $(document).on("report-data-loaded", function() {
        console.log("Report data loaded");
        const columns = $('.grid-row').find('.grid-cell');
        let hasUsdValues = false;
        
        columns.each(function() {
            const cell = $(this);
            const fieldname = cell.data('fieldname');
            if (fieldname === 'amount_usd') {
                const value = cell.text().trim();
                if (value && value !== '0.00') {
                    hasUsdValues = true;
                }
            }
        });
        
        console.log("USD values found:", hasUsdValues);
    });
});