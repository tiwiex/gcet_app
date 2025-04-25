import frappe
from frappe.auth import LoginManager

@frappe.whitelist()
def switch_back(original_user):
    if frappe.session.user == frappe.session.impersonated_user:
        login_manager = LoginManager()
        login_manager.authenticate(user=original_user)
        frappe.local.login_manager.login()
        frappe.db.commit()
        return "switched_back"
