import frappe
from frappe.utils import getdate, flt
from erpnext.accounts.report.balance_sheet.balance_sheet import execute as original_execute
from frappe import _
import logging
import json
import traceback

# Set up logging
logger = logging.getLogger("balance_sheet_usd")
logger.setLevel(logging.DEBUG)

def execute(filters=None):
    try:
        frappe.log_error("Balance Sheet USD execute called", "BS USD Debug")
        
        # Ensure filters is a dictionary
        if isinstance(filters, str):
            filters = json.loads(filters)
            frappe.log_error("Converted string filters to dict", "BS USD Debug")
        
        if not filters:
            filters = {}
            frappe.log_error("No filters provided, using empty dict", "BS USD Debug")
            
        # Ensure required filters are set
        if "company" not in filters:
            filters["company"] = frappe.defaults.get_user_default("Company")
            frappe.log_error(f"Set default company", "BS USD Debug")
            
        if "periodicity" not in filters:
            filters["periodicity"] = "Yearly"
            frappe.log_error("Set default periodicity: Yearly", "BS USD Debug")
            
        if "period_start_date" not in filters:
            from datetime import datetime, timedelta
            filters["period_start_date"] = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            frappe.log_error("Set default start date", "BS USD Debug")
            
        if "period_end_date" not in filters:
            from datetime import datetime
            filters["period_end_date"] = datetime.now().strftime("%Y-%m-%d")
            frappe.log_error("Set default end date", "BS USD Debug")
            
        # Get exchange rate from filters or default
        exchange_rate = filters.get("usd_exchange_rate", 1500.0)
        frappe.log_error(f"Using USD exchange rate: {exchange_rate}", "BS USD Debug")
            
        # Create a copy of filters without usd_exchange_rate for original_execute
        original_filters = filters.copy()
        if "usd_exchange_rate" in original_filters:
            del original_filters["usd_exchange_rate"]
            
        frappe.log_error("Prepared filters for original execute", "BS USD Debug")
        
        # Get original data
        frappe.log_error("Calling original_execute", "BS USD Debug")
        result = original_execute(original_filters)
        frappe.log_error(f"Original execute returned {len(result)} items", "BS USD Debug")
        
        # Log the structure of the result
        for i, item in enumerate(result):
            if i == 0:  # Columns
                frappe.log_error(f"Result[0] (Columns): {len(item)} items", "BS USD Debug")
                if len(item) > 0:
                    frappe.log_error(f"First column: {item[0]}", "BS USD Debug")
            elif i == 1:  # Data
                frappe.log_error(f"Result[1] (Data): {len(item)} items", "BS USD Debug")
                if len(item) > 0:
                    frappe.log_error(f"First data row: {item[0]}", "BS USD Debug")
            else:
                frappe.log_error(f"Result[{i}]: {type(item)}", "BS USD Debug")
        
        if len(result) >= 2:
            columns, data = result[0], result[1]
            frappe.log_error(f"Columns: {len(columns)}, Data rows: {len(data)}", "BS USD Debug")
            
            # Change the first column's label to something very obvious
            if columns and isinstance(columns[0], dict):
                columns[0]["label"] = "*** USD BALANCE SHEET ***"
            
            # Add USD columns
            new_columns = []
            for col in columns:
                new_columns.append(col)
                # Check if this is a numeric column that should have a USD equivalent
                if isinstance(col, dict) and col.get("fieldtype") in ["Currency", "Float", "Int"] and col.get("fieldname") != "account":
                    usd_col = col.copy()
                    usd_col["fieldname"] = f"{col['fieldname']}_usd"
                    usd_col["label"] = f"{col['label']} (USD)"
                    usd_col["options"] = "Currency"
                    usd_col["currency"] = "USD"
                    new_columns.append(usd_col)
                    frappe.log_error(f"Added USD column: {usd_col['fieldname']} from {col['fieldname']}", "BS USD Debug")
            
            columns = new_columns
            frappe.log_error(f"New columns count: {len(columns)}", "BS USD Debug")
            
            # Add USD values to data
            modified_rows = 0
            for row_idx, row in enumerate(data):
                if isinstance(row, dict):
                    for col in columns:
                        if isinstance(col, dict) and col.get("fieldname") and "_usd" in col.get("fieldname"):
                            original_fieldname = col.get("fieldname").replace("_usd", "")
                            if original_fieldname in row and row.get(original_fieldname) is not None:
                                original_value = flt(row.get(original_fieldname))
                                row[col.get("fieldname")] = original_value / exchange_rate
                                if row_idx < 2:  # Log only first 2 rows for brevity
                                    frappe.log_error(f"Row {row_idx}: {original_fieldname}={original_value} → {col.get('fieldname')}={row[col.get('fieldname')]}", "BS USD Debug")
                                modified_rows += 1
            
            frappe.log_error(f"Modified {modified_rows} data values", "BS USD Debug")
            
            # Return the modified result with all original items
            result_list = list(result)  # Convert tuple to list if needed
            result_list[0] = columns
            result_list[1] = data
            frappe.log_error(f"Returning {len(result_list)} items", "BS USD Debug")
            return tuple(result_list)  # Convert back to tuple if needed
        else:
            frappe.log_error(f"Unexpected result format", "BS USD Debug")
            return result
        
    except Exception as e:
        frappe.log_error(f"Error: {str(e)}\n{traceback.format_exc()}", "BS USD Error")
        frappe.throw(f"Error in Balance Sheet USD: {str(e)}")

def get_usd_exchange_rate(filters=None):
    try:
        # First check if the rate is provided in filters
        if filters and "usd_rate" in filters and filters["usd_rate"]:
            frappe.log_error(f"Using exchange rate from filters", "BS USD Debug")
            return float(filters["usd_rate"])
            
        # Otherwise, get the latest exchange rate from Currency Exchange doctype
        exchange_rate = frappe.db.get_value(
            "Currency Exchange",
            {
                "from_currency": "NGN",
                "to_currency": "USD",
            },
            "exchange_rate",
            order_by="date desc"
        )
        
        if not exchange_rate:
            frappe.log_error("USD Exchange rate not found. Using default.", "BS USD Debug")
            return 1000.0
            
        frappe.log_error(f"Found exchange rate", "BS USD Debug")
        return float(exchange_rate)
    except Exception as e:
        frappe.log_error(f"Error getting exchange rate", "BS USD Debug")
        return 1000.0

def get_columns(filters):
    columns = [{
        "label": "Account",
        "fieldname": "account",
        "fieldtype": "Link",
        "options": "Account",
        "width": 200
    }]
    for label, _, _ in get_period_date_ranges(filters):
        columns.append({"label": f"{label} (₦)", "fieldtype": "Currency", "fieldname": f"{label}_ngn", "width": 120})
        columns.append({"label": f"{label} ($)", "fieldtype": "Float", "fieldname": f"{label}_usd", "width": 120})
    return columns

def get_data(filters, columns):
    accounts = frappe.get_all("Account", filters={
        "company": filters.company,
        "report_type": "Balance Sheet"
    }, fields=["name"])
    data = []
    for acc in accounts:
        row = {"account": acc.name}
        for label, start, end in get_period_date_ranges(filters):
            result = frappe.db.sql("""
                SELECT SUM(debit - credit) FROM `tabGL Entry`
                WHERE account = %s AND posting_date BETWEEN %s AND %s AND docstatus = 1 AND company = %s
            """, (acc.name, start, end, filters.company))
            ngn_val = flt(result[0][0]) if result and result[0][0] else 0
            row[f"{label}_ngn"] = ngn_val
            row[f"{label}_usd"] = ngn_val / flt(filters.usd_rate or 1000)
        data.append(row)
    return data

def get_period_date_ranges(filters):
    from dateutil.relativedelta import relativedelta
    import calendar
    fy_data = frappe.get_doc("Fiscal Year", filters.fiscal_year)
    start_date = getdate(fy_data.year_start_date)
    end_date = getdate(fy_data.year_end_date)
    periodicity = filters.periodicity or "Monthly"

    current = start_date
    periods = []

    while current <= end_date:
        if periodicity == "Monthly":
            label = current.strftime("%b %Y")
            period_end = current.replace(day=calendar.monthrange(current.year, current.month)[1])
        elif periodicity == "Quarterly":
            quarter = (current.month - 1) // 3 + 1
            label = f"Q{quarter} {current.year}"
            period_end = current + relativedelta(months=3, days=-1)
        else:
            label = str(current.year)
            period_end = current.replace(month=12, day=31)
        periods.append((label, current, min(period_end, end_date)))
        current = period_end + relativedelta(days=1)
    return periods