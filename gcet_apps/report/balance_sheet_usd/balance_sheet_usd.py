import frappe
from frappe.utils import getdate, flt
from erpnext.accounts.utils import get_fiscal_year_data
from erpnext.accounts.report.balance_sheet.balance_sheet import execute as original_execute
from frappe import _
import logging
import json
import traceback

# Set up logging
# logger = logging.getLogger("balance_sheet_usd")
# logger.setLevel(logging.DEBUG)

def execute(filters=None):
    try:
        frappe.log_error(f"Balance Sheet USD execute called with filters: {filters}", "Balance Sheet USD Debug")
        
        # Ensure filters is a dictionary
        if isinstance(filters, str):
            filters = json.loads(filters)
            frappe.log_error(f"Converted string filters to dict: {filters}", "Balance Sheet USD Debug")
        
        if not filters:
            filters = {}
            frappe.log_error("No filters provided, using empty dict", "Balance Sheet USD Debug")
            
        # Ensure required filters are set
        if "company" not in filters:
            filters["company"] = frappe.defaults.get_user_default("Company")
            frappe.log_error(f"Set default company: {filters['company']}", "Balance Sheet USD Debug")
            
        if "periodicity" not in filters:
            filters["periodicity"] = "Yearly"
            frappe.log_error("Set default periodicity: Yearly", "Balance Sheet USD Debug")
            
        if "period_start_date" not in filters:
            from datetime import datetime, timedelta
            filters["period_start_date"] = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            frappe.log_error(f"Set default start date: {filters['period_start_date']}", "Balance Sheet USD Debug")
            
        if "period_end_date" not in filters:
            from datetime import datetime
            filters["period_end_date"] = datetime.now().strftime("%Y-%m-%d")
            frappe.log_error(f"Set default end date: {filters['period_end_date']}", "Balance Sheet USD Debug")
            
        # Get exchange rate from filters or default
        exchange_rate = filters.get("usd_exchange_rate", 1500.0)
        frappe.log_error(f"Using USD exchange rate: {exchange_rate}", "Balance Sheet USD Debug")
            
        # Create a copy of filters without usd_exchange_rate for original_execute
        original_filters = filters.copy()
        if "usd_exchange_rate" in original_filters:
            del original_filters["usd_exchange_rate"]
            
        frappe.log_error(f"Final filters for original execute: {original_filters}", "Balance Sheet USD Debug")
        
        # Get original data
        frappe.log_error("Calling original_execute", "Balance Sheet USD Debug")
        result = original_execute(original_filters)
        frappe.log_error(f"Original execute returned {len(result)} items", "Balance Sheet USD Debug")
        
        if len(result) >= 2:
            columns, data = result[0], result[1]
            frappe.log_error(f"Columns: {len(columns)}, Data: {len(data)}", "Balance Sheet USD Debug")
            
            # Add USD columns
            new_columns = []
            for col in columns:
                new_columns.append(col)
                if isinstance(col, dict) and col.get("fieldname") and col.get("fieldname") != "account":
                    usd_col = col.copy()
                    usd_col["fieldname"] = f"{col['fieldname']}_usd"
                    usd_col["label"] = f"{col['label']} (USD)"
                    usd_col["options"] = "Currency"
                    usd_col["currency"] = "USD"
                    new_columns.append(usd_col)
            
            columns = new_columns
            frappe.log_error(f"New columns count: {len(columns)}", "Balance Sheet USD Debug")
            
            # Add USD values to data
            for row in data:
                if isinstance(row, dict):
                    for col in columns:
                        if isinstance(col, dict) and col.get("fieldname") and "_usd" in col.get("fieldname"):
                            original_fieldname = col.get("fieldname").replace("_usd", "")
                            if row.get(original_fieldname) is not None:
                                row[col.get("fieldname")] = flt(row.get(original_fieldname)) / exchange_rate
            
            frappe.log_error("USD values added to data", "Balance Sheet USD Debug")
            
            # Return the modified result
            if len(result) == 2:
                frappe.log_error("Returning 2 items", "Balance Sheet USD Debug")
                return columns, data
            elif len(result) == 3:
                frappe.log_error("Returning 3 items", "Balance Sheet USD Debug")
                return columns, data, result[2]
            elif len(result) == 4:
                frappe.log_error("Returning 4 items", "Balance Sheet USD Debug")
                return columns, data, result[2], result[3]
            elif len(result) == 5:
                frappe.log_error("Returning 5 items", "Balance Sheet USD Debug")
                return columns, data, result[2], result[3], result[4]
            else:
                frappe.log_error(f"Unexpected result length: {len(result)}", "Balance Sheet USD Debug")
                return result
        else:
            frappe.log_error(f"Unexpected result format: {result}", "Balance Sheet USD Debug")
            return result
        
    except Exception as e:
        frappe.log_error(f"Error in Balance Sheet USD: {str(e)}\n{traceback.format_exc()}", "Balance Sheet USD Error")
        frappe.throw(f"Error in Balance Sheet USD: {str(e)}")

def get_usd_exchange_rate(filters=None):
    try:
        # First check if the rate is provided in filters
        if filters and "usd_rate" in filters and filters["usd_rate"]:
            frappe.log_error(f"Using exchange rate from filters: {filters['usd_rate']}", "Balance Sheet USD Debug")
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
            frappe.log_error("USD Exchange rate not found. Using 1000.0 as default.", "Balance Sheet USD Debug")
            return 1000.0
            
        frappe.log_error(f"Found exchange rate: {exchange_rate}", "Balance Sheet USD Debug")
        return float(exchange_rate)
    except Exception as e:
        frappe.log_error(f"Error getting exchange rate: {str(e)}", "Balance Sheet USD Debug")
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