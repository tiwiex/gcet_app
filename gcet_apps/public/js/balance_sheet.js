// Wait for document ready
frappe.ready(function() {
    console.log("Balance Sheet JS loaded");
    
    // Add event listener to check when the report is loaded
    frappe.realtime.on("report-refresh", function() {
        console.log("Report refreshed");
        // Check if the USD column exists
        const columns = document.querySelectorAll('.grid-row .grid-cell');
        let hasUsdColumn = false;
        
        columns.forEach(function(cell) {
            const fieldname = cell.getAttribute('data-fieldname');
            if (fieldname === 'amount_usd') {
                hasUsdColumn = true;
                cell.style.display = 'table-cell';
            }
        });
        
        console.log("USD column exists:", hasUsdColumn);
    });
    
    // Add event listener for report generation
    frappe.realtime.on("report-generate", function() {
        console.log("Report generation started");
    });

    // Add event listener for report data load
    frappe.realtime.on("report-data-loaded", function() {
        console.log("Report data loaded");
        const columns = document.querySelectorAll('.grid-row .grid-cell');
        let hasUsdValues = false;
        
        columns.forEach(function(cell) {
            const fieldname = cell.getAttribute('data-fieldname');
            if (fieldname === 'amount_usd') {
                const value = cell.textContent.trim();
                if (value && value !== '0.00') {
                    hasUsdValues = true;
                }
            }
        });
        
        console.log("USD values found:", hasUsdValues);
    });
});